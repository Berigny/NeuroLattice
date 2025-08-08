def trace_modal_input(modal_name, event_key, kernel):
    modal = kernel["brand_identity_kernel"]["modal_domains"][modal_name]
    outputs = modal["outputs"]
    prime = outputs.get(event_key)
    return prime
