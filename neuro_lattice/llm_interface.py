import subprocess
import json

def run_codex(prompt: str) -> str:
    """
    Runs a prompt using the local Codex CLI and returns the output as a string.
    Assumes `codex` is installed and authenticated on this machine.
    """
    try:
        result = subprocess.run(
            ["codex", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] Codex CLI failed: {e.stderr.strip()}"

def codex_with_brand_context(prompt: str, brand_data: dict) -> str:
    
    
    # Prime Codex with brand identity first
    context = f"""You are a brand agent. Here is the brand's identity context:

{json.dumps(brand_data, indent=2)}

Now complete the following task with this tone, structure, and memory:

{prompt}
"""
    return run_codex(context)
