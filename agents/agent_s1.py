import os
from neuro_lattice.llm_interface import with_brand_context

def respond(context, brand_data):  # fast proposal
    provider = os.environ.get("S1_PROVIDER", "codex")
    return with_brand_context(provider, f"S1 (fast, visual/somatic): {context}", brand_data)
