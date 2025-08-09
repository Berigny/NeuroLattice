#!/usr/bin/env python3
"""Smoke test without FastAPI import: S1=Codex(mock) vs S2=Gemini(mock).

Validates the turn-taking and provider split using core helpers only.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli_agent.actions.load_kernel import load_brand_kernel
from cli_agent.actions.trace_modal import trace_modal_input
from cli_agent.actions.evaluate_resonance import evaluate_resonance
from neuro_lattice.llm_interface import with_brand_context


def main() -> None:
    os.environ.setdefault("S1_PROVIDER", "mock")
    os.environ.setdefault("S2_PROVIDER", "gemini")
    os.environ.setdefault("GEMINI_MOCK", "1")

    kernel = load_brand_kernel()
    modal = "visual"
    event = "amplify_brand_colours"
    prime = trace_modal_input(modal, event, kernel, kind="outputs") or 0
    resonance = evaluate_resonance(prime, kernel["brand_identity_kernel"]["resonance_map"])

    turns = 4
    speaker = "S1"
    prompt = "Homepage hero headline + subcopy for spring value event; inclusive, accessible."

    messages = []
    seed = f"(Prime={prime}, Resonance={resonance})\n{prompt}"
    s1_text = with_brand_context(os.environ.get("S1_PROVIDER", "codex"), f"S1: Propose an on-brand concept.\n{seed}", kernel)
    messages.append({"turn": 1, "speaker": "S1", "text": s1_text})

    speaker = "S2"
    for t in range(2, turns + 1):
        last = messages[-1]["text"]
        role = (
            "Critique & refine (ethical, relational, clarity)"
            if speaker == "S2"
            else "Revise proposal (concise, concrete, visual tokens)"
        )
        p = (
            f"{role}.\nBRAND CONTEXT: {modal}/{event}, Prime={prime}, Resonance={resonance}\n"
            f"LAST MESSAGE ({messages[-1]['speaker']}): {last}\n"
            f"Respond with one short paragraph + 3 bullet improvements."
        )
        provider = os.environ.get("S2_PROVIDER", "codex") if speaker == "S2" else os.environ.get("S1_PROVIDER", "codex")
        text = with_brand_context(provider, p, kernel)
        messages.append({"turn": t, "speaker": speaker, "text": text})
        speaker = "S1" if speaker == "S2" else "S2"

    print("Transcript")
    for m in messages:
        print(f"Turn {m['turn']} – {m['speaker']}\n\n{m['text']}\n")


if __name__ == "__main__":
    main()

