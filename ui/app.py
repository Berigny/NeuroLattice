# ui/app.py
import streamlit as st
import httpx

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="NeuroLattice – Brand Session", layout="wide")
st.title("NeuroLattice — S1 ↔ S2 Brand Session")

# ---- Load kernel metadata for dropdowns ----
with st.sidebar:
    st.header("Backend")
    api_url = st.text_input("Mediator URL", API)
    if st.button("Check health"):
        try:
            r = httpx.get(f"{api_url}/health", timeout=5)
            st.success(r.json())
        except Exception as e:
            st.error(f"Health check failed: {e}")

    st.header("Kernel")
    try:
        meta = httpx.get(f"{api_url}/kernel", timeout=10).json()
        modals = meta["modal_names"]
        events = meta["events"]
    except Exception as e:
        st.error(f"Failed to load kernel metadata: {e}")
        st.stop()

colL, colR = st.columns([2,1])

with colL:
    prompt = st.text_area("Brief / Task", "Homepage hero headline + subcopy for spring value event; inclusive, accessible.", height=150)
    modal = st.selectbox("Modal face", modals, index=modals.index("visual") if "visual" in modals else 0)

    evt_kind = st.radio("Event type", ["outputs", "inputs"], horizontal=True)
    evt_list = events[modal][evt_kind]
    event = st.selectbox("Event", evt_list, index=0)

    turns = st.slider("Turns", 1, 12, 6, 1)
    threshold = st.slider("Strain threshold", 0.0, 1.0, 0.25, 0.01)

    if st.button("Run session"):
        with st.spinner("Running S1 ↔ S2…"):
            try:
                payload = {"prompt": prompt, "modal": modal, "event": event, "event_kind": evt_kind, "turns": turns, "strain_threshold": threshold}
                resp = httpx.post(f"{api_url}/session", json=payload, timeout=120)
                data = resp.json()
            except Exception as e:
                st.error(f"Request failed: {e}")
                st.stop()

        msgs = data["messages"]
        stopped = data["stopped_on_strain"]

        st.subheader("Transcript")
        for m in msgs:
            badge = "" if m["strain"] <= threshold else ""
            st.markdown(f"**Turn {m['turn']} – {m['speaker']}**  {badge}  \n*Strain:* `{m['strain']:.2f}`  · *Prime:* `{m['prime']}`  · *Resonance:* `{', '.join(m['resonance'])}`")
            st.write(m["text"])
            st.divider()

        if stopped:
            st.warning("Session stopped due to strain exceeding threshold. Consider compressing novelty or revising constraints.")

with colR:
    st.subheader("Tips")
    st.markdown("""
- Use **outputs** events for generation (e.g., `amplify_brand_colours`, `write_in_voice`).
- If strain is high immediately, lower novelty in your brief or choose a different event.
- Keep prompts concrete; S2 will enforce ethics/accessibility.
""")
