# agents/mediator_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Literal
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from cli_agent.actions.load_kernel import load_brand_kernel
from cli_agent.actions.trace_modal import trace_modal_input
from cli_agent.actions.evaluate_resonance import evaluate_resonance
import os
from neuro_lattice.llm_interface import with_brand_context

app = FastAPI(title="NeuroLattice Mediator")

# ---- Simple models ----
class SessionReq(BaseModel):
    prompt: str
    modal: str = "visual"
    event: str = "amplify_brand_colours"
    event_kind: Literal["inputs","outputs"] = "outputs"
    turns: int = 6
    strain_threshold: float = 0.25

class TurnMsg(BaseModel):
    turn: int
    speaker: str
    text: str
    strain: float
    prime: int
    resonance: List[str]

class SessionResp(BaseModel):
    messages: List[TurnMsg]
    stopped_on_strain: bool = False

# ---- Helpers ----
def is_composite(n: int) -> bool:
    if n is None: return False
    return n not in (2,3,5,7,11,13,17,19)

def strain_score(prime: int, resonance: list[str]) -> float:
    base = 0.30
    if is_composite(prime): base -= 0.02
    if any(r.startswith("S1-") for r in resonance): base -= 0.06
    if any(r.startswith("S2-") for r in resonance): base -= 0.06
    return max(0.01, base)

# ---- Routes ----
@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True}

@app.get("/kernel")
def kernel_meta():
    k = load_brand_kernel()
    domains = k["brand_identity_kernel"]["modal_domains"]
    return {
        "modal_names": list(domains.keys()),
        "events": {
            m: {
                "inputs":  list(domains[m].get("inputs", {}).keys()),
                "outputs": list(domains[m].get("outputs", {}).keys())
            }
            for m in domains
        }
    }

@app.post("/session", response_model=SessionResp)
def run_session(req: SessionReq) -> SessionResp:
    kernel = load_brand_kernel()
    prime = trace_modal_input(req.modal, req.event, kernel, kind=req.event_kind)
    if prime is None:
        # Handle case where event is not found
        prime = 0 # or some default value
    resonance = evaluate_resonance(prime, kernel["brand_identity_kernel"]["resonance_map"])

    messages: List[TurnMsg] = []

    # Resolve providers from env (defaults: both codex)
    s1_provider = os.environ.get("S1_PROVIDER", "codex")
    s2_provider = os.environ.get("S2_PROVIDER", "codex")

    # Turn 1: S1 proposes
    seed = f"(Prime={prime}, Resonance={resonance})\n{req.prompt}"
    s1_text = with_brand_context(s1_provider, f"S1: Propose an on-brand concept.\n{seed}", kernel)
    s1_strain = strain_score(prime, resonance)
    messages.append(TurnMsg(turn=1, speaker="S1", text=s1_text, strain=s1_strain, prime=prime, resonance=resonance))

    # Subsequent turns alternate S2 critique ↔ S1 revision
    speaker = "S2"
    for t in range(2, req.turns + 1):
        last = messages[-1].text
        role = "Critique & refine (ethical, relational, clarity)" if speaker == "S2" else "Revise proposal (concise, concrete, visual tokens)"
        prompt = f'''{role}.\nBRAND CONTEXT: {req.modal}/{req.event}, Prime={prime}, Resonance={resonance}\nLAST MESSAGE ({messages[-1].speaker}): {last}\nRespond with one short paragraph + 3 bullet improvements.'''
        provider = s2_provider if speaker == "S2" else s1_provider
        text = with_brand_context(provider, prompt, kernel)
        s = strain_score(prime, resonance)
        msg = TurnMsg(turn=t, speaker=speaker, text=text, strain=s, prime=prime, resonance=resonance)
        messages.append(msg)

        if s > req.strain_threshold:
            return SessionResp(messages=messages, stopped_on_strain=True)

        speaker = "S1" if speaker == "S2" else "S2"

    return SessionResp(messages=messages, stopped_on_strain=False)
