#!/usr/bin/env python3
"""Smoke test: S1 via Codex mock, S2 via Gemini mock.

Runs the FastAPI session logic directly and prints the transcript.
This does not require network or real CLIs when MOCK envs are set.
"""
import os
import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.mediator_server import run_session, SessionReq


def main() -> None:
    # Force mock providers for deterministic, offline test
    os.environ.setdefault("S1_PROVIDER", "mock")
    os.environ.setdefault("S2_PROVIDER", "gemini")
    os.environ.setdefault("GEMINI_MOCK", "1")

    req = SessionReq(
        prompt="Homepage hero headline + subcopy for spring value event; inclusive, accessible.",
        modal="visual",
        event="amplify_brand_colours",
        event_kind="outputs",
        turns=4,
        strain_threshold=0.9,
    )

    resp = run_session(req)
    print("Transcript")
    for m in resp.messages:
        reso = ", ".join(m.resonance)
        print(f"Turn {m.turn} – {m.speaker}\nStrain: {m.strain:.2f} · Prime: {m.prime} · Resonance: {reso}\n\n{m.text}\n")


if __name__ == "__main__":
    main()
