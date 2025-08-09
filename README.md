# NeuroLattice — Brand Identity Kernel (Multimodal, Ethical, On-Brand)

NeuroLattice is a **brand identity engine** that lets you generate and review **on-brand experiences** (copy, UI hints, tone, visuals) without drifting off brand or getting rigid.

It does this by:

* Grounding every decision in a **prime-weighted brand kernel** (your identity memory).
* Running two cooperating agents:

  * **System 1 (S1)** — fast, sensory, proposal-oriented.
  * **System 2 (S2)** — reflective, relational, ethical, corrective.
* Mediating the conversation through a **Centroid/Blueprint** that minimises ethical/brand strain.

Think of it as a **living design system** that can talk, design, and self-correct.

---

## Why this is useful

* **On-brand by design**: Everything routes through the **brand\_identity\_kernel.json** (your colours, voice, values, constraints, prime weights).
* **No brittle style guides**: S1 keeps novelty alive; S2 prevents chaos. The mediator balances both.
* **Ethical from the ground up**: Outputs are gated by a **strain score** (coherence & ethics).
* **Multimodal**: Six “faces” (visual, auditory, linguistic, kinaesthetic, emotional, symbolic), each with **8 nodes (4 in / 4 out)**.
* **Pluggable LLM**: Start with **Codex CLI** (low friction). Later swap in **local models** (Ollama/Mistral) with one flag.

---

## Repository layout

```
neuro_lattice/
├─ cli.py                         # top-level CLI (trace/session commands)
├─ agents/
│  ├─ mediator.py                 # S1 <-> S2 turn-taking, strain, logs
│  ├─ agent_s1.py                 # fast proposals (visual/somatic bias)
│  └─ agent_s2.py                 # ethical critique (social/linguistic)
├─ cli_agent/
│  └─ actions/
│     ├─ load_kernel.py
│     ├─ trace_modal.py
│     └─ evaluate_resonance.py
├─ neuro_lattice/
│  ├─ llm_interface.py            # Codex wrapper (+ optional local fallback)
│  └─ config/llm.toml             # LLM config (binary path, timeouts, etc.)
├─ memory/
│  └─ brand_identity_kernel.json  # prime-weighted brand identity memory
└─ logs/
   └─ lattice_events.log          # session logs (optional)
```

---

## Prerequisites

* Python **3.11+** (pyenv recommended)
* VS Code (recommended)
* **Codex CLI** installed & authenticated (or a local LLM via Ollama)

Quick checks:

```bash
python --version
which codex && codex --version
```

---

## Install & set up

```bash
# Install deps
pip install -r requirements.txt  # (or: pip install networkx numpy rich)

# Configure LLM
cp neuro_lattice/config/llm.example.toml neuro_lattice/config/llm.toml
# edit values if needed (codex binary path, timeouts, brand JSON path)
```

Codex auth:

```bash
codex login
codex "ping"
```

---

## First run (quick smoke test)

### 1) Trace a modal event

```bash
python cli.py trace --modal visual --event amplify_brand_colours
```

You should see the prime and its resonance node (e.g. `Prime [26] → S1-N1`).

### 2) Run a full S1 ⇄ S2 session

```bash
python agents/mediator.py --prompt "Homepage hero headline + subcopy for spring value event; inclusive, accessible." --modal visual --event amplify_brand_colours --turns 6
```

This will alternate S1 → S2, record messages, and stop if **strain** exceeds the threshold.

Check the bus/log:

```bash
cat /tmp/lattice_bus.jsonl
```

---
## Streamlit UI

This project includes a Streamlit UI for interacting with the NeuroLattice agent.

### UI Setup

1.  **Install UI dependencies**:
    ```bash
    pip install streamlit httpx
    ```

2.  **Run the FastAPI server**:
    ```bash
    uvicorn agents.mediator_server:app --reload
    ```

3.  **Run the Streamlit app**:
    ```bash
    streamlit run ui/app.py
    ```

---

## Everyday usage (VS Code friendly)

### Generate with brand context (Codex)

```bash
python cli.py session \
  --prompt "Onboarding email copy for click-and-collect; friendly, concise." \
  --modal linguistic \
  --event write_in_voice \
  --turns 6
```

### Interactive steering mid-session

You can enable an interactive pause in `mediator.py` to type guidance between turns. Great for workshops.

### From a brief file

```bash
python agents/mediator.py --prompt "$(cat briefs/receipt_email.txt)"
```

(Or add `--brief path/to.json` if you wire the loader.)

---

## How it stays on brand (in plain English)

1. **Brand kernel** (JSON) encodes your identity:
   colours, tone, behaviours, and **prime composites** per modality.
2. Each request is tagged with **modal** + **event** → resolves to a **composite prime**.
3. The **resonance map** ties that prime to core nodes (System 1 & 2) — your ethical/brand anchors.
4. S1 proposes; S2 critiques; the **mediator** watches **strain**.

   * Low strain: ship the idea.
   * High strain: compress, rest, and revise.

---

## Configuring the brand kernel

Edit `memory/brand_identity_kernel.json`:

* Update **brand colours**, **tone rules**, **modal inputs/outputs**, **resonance\_map**.
* Keep numbers as **primes or prime composites** for traceability.
* Smaller primes = **harder to shift** (core identity). Larger composites = **more adaptive**.

Tip: keep a human-readable **“voice & tone”** snippet in the JSON so the LLM wrapper can inject it cleanly.

---

## LLM backends

Default: **Codex CLI**

* Config: `neuro_lattice/config/llm.toml`
* Limit prompt size with `max_chars` to avoid cost/noise.
* Fallback to **Ollama** by toggling a flag (see `llm_interface.py`).

---

## Commands (cheat sheet)

```bash
# Help
python cli.py --help
python cli.py trace --help
python cli.py session --help

# Trace a single modal event → prime & resonance
python cli.py trace --modal visual --event amplify_brand_colours

# Run a multi-turn S1<->S2 session
python cli.py session --prompt "Product page microcopy for eco-relaunch" --modal linguistic --event write_in_voice --turns 6
```

---

## VS Code tips

* **Python: Select Interpreter** → choose your pyenv 3.11 environment.
* **Run & Debug**: add a launch config to call `cli.py session …`.
* **Black/ruff**: add a formatter to keep diffs tidy.
* **Tasks**: create `tasks.json` to run a default session with one key.

---

## Ongoing use & ops

* **Before big campaigns**: run a session per modality (visual, linguistic, symbolic) to check coherence.
* **Design reviews**: paste proposed copy/layout into `--prompt`, then capture S2’s improvement bullets.
* **Accessibility**: keep WCAG rules in the wrapper prompt; S2 will enforce them.
* **Governance**: log `/tmp/lattice_bus.jsonl` and `logs/lattice_events.log` for audit.

---

## Troubleshooting

* `invalid choice: 'are'` → You typed a sentence without a subcommand. Use `session --prompt "…"` or add a `chat` command.
* `codex not found` → Install Codex CLI or set `codex.binary` in `llm.toml`.
* `auth failed` → `codex login` again; restart terminal.
* Empty/odd outputs → check `max_chars`, shrink brand JSON excerpt, and confirm your prompt is concrete.

---

## Roadmap

* [ ] Local model router (Ollama) as first-class backend
* [ ] Figma plugin (live visual lint using resonance/strain)
* [ ] Drift dashboard (coherence index over time)
* [ ] Team ritual templates (brand council, weekly coherence check)
* [ ] Tokenised brand assets (colour/type tokens auto-generated with explanations)

---

## Licence / Safety

* Keep brand IP & values confidential.
* This system **respects accessibility and ethical constraints by default** — do not remove the safety rules from the LLM wrapper.

---

**Questions?**
Ping the mediator with a `session` run and read the suggestions at the end — it’s designed to *tell you* how to improve the brand artefact and the system itself.
