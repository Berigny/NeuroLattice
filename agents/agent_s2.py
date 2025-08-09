from neuro_lattice.llm_interface import codex_with_brand_context

def respond(context, brand_data):  # reflective critique
    return codex_with_brand_context(f"S2 (ethical, social-moral, linguistic): {context}", brand_data)
