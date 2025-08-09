from neuro_lattice.llm_interface import codex_with_brand_context

def respond(context, brand_data):  # fast proposal
    return codex_with_brand_context(f"S1 (fast, visual/somatic): {context}", brand_data)
