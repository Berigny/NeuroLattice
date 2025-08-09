import json
import pathlib
from neuro_lattice.llm_interface import codex_with_brand_context

BUS = pathlib.Path("/tmp/lattice_bus.jsonl")

def post(msg):
    mode = "a" if BUS.exists() else "w"
    with BUS.open(mode) as f:
        f.write(json.dumps(msg) + "\n")

def run_interactive(systems, modals, brand_data, turns=3):
    from agents import agent_s1, agent_s2
    
    system_map = {'1': agent_s1, '2': agent_s2}
    
    s1_id, s2_id = systems
    s1 = system_map[s1_id]
    s2 = system_map[s2_id]

    BUS.unlink(missing_ok=True)

    prompt = input("Enter the initial prompt for the interactive session: ")

    for turn in range(1, turns + 1):
        s1_prompt = f"System {s1_id} (propose): Based on the context of {modals}, {prompt}"
        s1_response = s1.respond(s1_prompt, brand_data)
        post({"turn": turn, "system": s1_id, "action": "propose", "response": s1_response})
        print(f"\nSystem {s1_id} (propose):\n{s1_response}")

        s2_prompt = f"System {s2_id} (critique): Critique the following proposal from System {s1_id}:\n{s1_response}"
        s2_response = s2.respond(s2_prompt, brand_data)
        post({"turn": turn, "system": s2_id, "action": "critique", "response": s2_response})
        print(f"\nSystem {s2_id} (critique):\n{s2_response}")

        s1_revise_prompt = f"System {s1_id} (revise): Revise your proposal based on the critique from System {s2_id}:\nCritique: {s2_response}\nOriginal proposal: {s1_response}"
        s1_revised_response = s1.respond(s1_revise_prompt, brand_data)
        post({"turn": turn, "system": s1_id, "action": "revise", "response": s1_revised_response})
        print(f"\nSystem {s1_id} (revise):\n{s1_revised_response}")

        prompt = s1_revised_response

    print("\n=== INTERACTIVE SESSION COMPLETE ===")
    print(BUS.read_text())