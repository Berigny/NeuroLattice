def trace_modal_input(modal_name, event_key, kernel, kind="outputs"):
    modal = kernel["brand_identity_kernel"]["modal_domains"][modal_name]
    table = modal.get(kind, {})
    prime = table.get(event_key)
    return prime