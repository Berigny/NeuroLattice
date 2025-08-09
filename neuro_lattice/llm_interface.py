import os
import sys
import subprocess
import shlex
import json

def run_codex(prompt: str) -> str:
    # Default to non-interactive invocation so UIs (e.g., Streamlit) don't trip
    # CLIs that attempt cursor reads or advanced TTY features.
    base_cmd = f'codex {shlex.quote(prompt)}'

    # Only opt-in to PTY if explicitly requested and stdout is a TTY.
    # Forcing a PTY in headless contexts causes cursor read timeouts.
    use_pty = bool(os.environ.get("FORCE_PTY")) and sys.stdout.isatty()
    cmd = f'script -q /dev/null {base_cmd}' if use_pty else base_cmd
    try:
        # In non-interactive contexts, reduce terminal features to avoid
        # cursor queries and ANSI noise.
        env = {
            **os.environ,
            "TERM": "dumb" if not use_pty else os.environ.get("TERM", "xterm-256color"),
            "NO_COLOR": "1",
            "CLICOLOR": "0",
        }

        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True, check=False, timeout=120,
            env=env,
        )
        out = (result.stdout or "").strip()
        err = (result.stderr or "").strip()

        # Ignore benign update notices in stderr
        if "Update available" in err and result.returncode == 0:
            err = ""

        if result.returncode != 0:
            return f"[CODEX_ERROR] {err or out or 'Codex returned non-zero exit'}"
        return out or "[WARN] Codex returned empty output"
    except subprocess.TimeoutExpired:
        return "[CODEX_ERROR] Timeout while waiting for Codex."

def codex_with_brand_context(prompt: str, brand_data: dict) -> str:


    # Prime Codex with brand identity first
    context = f"""You are a brand agent. Here is the brand's identity context:

{json.dumps(brand_data, indent=2)}

Now complete the following task with this tone, structure, and memory:

{prompt}
"""
    return run_codex(context)
