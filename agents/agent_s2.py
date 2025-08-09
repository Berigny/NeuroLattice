import os
from neuro_lattice.llm_interface import with_brand_context

def respond(context, brand_data):  # reflective critique
    provider = os.environ.get("S2_PROVIDER", "codex")
    return with_brand_context(provider, f"S2 (ethical, social-moral, linguistic): {context}", brand_data)
