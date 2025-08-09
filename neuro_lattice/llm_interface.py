import os
import sys
import subprocess
import shlex
import json

def _run_once(prompt: str, use_pty: bool, inject_cursor_reply: bool=False) -> tuple[int, str, str]:
    """Run the codex CLI once, optionally under a pseudo‑TTY.

    Returns (returncode, stdout, stderr).
    """
    base_cmd = f"codex {shlex.quote(prompt)}"
    # Some CLIs try to query cursor position via DSR (ESC[6n).
    # When headless, inject a plausible reply "ESC[1;1R" via stdin.
    if inject_cursor_reply:
        # Use a shell to construct the pipeline safely
        pipeline = f"printf '\\033[1;1R' | {base_cmd}"
    else:
        pipeline = base_cmd

    # Wrap in a PTY when requested. Use bash -lc to support the pipeline.
    if use_pty:
        cmd = f"script -q /dev/null bash -lc {shlex.quote(pipeline)}"
    else:
        cmd = pipeline

    # In non-interactive contexts, reduce terminal features to avoid
    # cursor queries and ANSI noise; still allow colors under PTY.
    env = {
        **os.environ,
        "TERM": (os.environ.get("TERM", "xterm-256color") if use_pty else "dumb"),
        "NO_COLOR": "0" if use_pty else "1",
        "CLICOLOR": "1" if use_pty else "0",
        # Hint CLIs to avoid fancier TUI behavior.
        "CI": os.environ.get("CI", "1"),
        "CODEX_NONINTERACTIVE": os.environ.get("CODEX_NONINTERACTIVE", "1"),
    }

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
        env=env,
    )
    out = (result.stdout or "").strip()
    err = (result.stderr or "").strip()
    return result.returncode, out, err


def run_codex(prompt: str) -> str:
    """Invoke codex robustly in non-interactive contexts.

    Strategy:
    - First attempt without a PTY and with TERM=dumb to minimize TUI behavior.
    - If the CLI reports a cursor/TTY error, retry under a pseudo‑TTY wrapper.
    - Respect FORCE_PTY=1 to always use a PTY on first attempt.
    """
    try:
        force_pty = bool(os.environ.get("FORCE_PTY"))

        # First attempt
        rc, out, err = _run_once(prompt, use_pty=force_pty or False, inject_cursor_reply=False)

        # Treat known benign notices
        if "Update available" in err and rc == 0:
            err = ""

        combined = f"{err}\n{out}".lower()
        has_codex_error_marker = "[codex_error]" in combined
        # Detect cursor/TTY-related issues to retry under PTY
        tty_issue = (
            "cursor position" in combined
            or "could not be read" in combined
            or "tty" in combined and "error" in combined
        )

        # If return code is OK but output carries an error marker, treat as error
        if rc == 0 and out and not has_codex_error_marker and not tty_issue:
            return out

        if not force_pty and (tty_issue or has_codex_error_marker):
            # First try injecting a cursor reply without PTY
            rc2, out2, err2 = _run_once(prompt, use_pty=False, inject_cursor_reply=True)
            if "Update available" in err2 and rc2 == 0:
                err2 = ""
            comb2 = f"{err2}\n{out2}".lower()
            if rc2 == 0 and out2 and "[codex_error]" not in comb2:
                return out2
            # Last resort: PTY + injected reply
            rc3, out3, err3 = _run_once(prompt, use_pty=True, inject_cursor_reply=True)
            if "Update available" in err3 and rc3 == 0:
                err3 = ""
            comb3 = f"{err3}\n{out3}".lower()
            if rc3 == 0 and out3 and "[codex_error]" not in comb3:
                return out3
            # Fall back to most informative error seen
            err = err3 or err2 or err
            out = out3 or out2 or out
            rc = rc3 or rc2 or rc

        if rc != 0:
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


# ---- Gemini integration (CLI or mock) ----
def _run_cli(cmd: str, env: dict | None = None, timeout: int = 120) -> tuple[int, str, str]:
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
        env=env or os.environ.copy(),
    )
    return result.returncode, (result.stdout or "").strip(), (result.stderr or "").strip()


def run_gemini(prompt: str) -> str:
    """Invoke a Gemini CLI if available, else fall back to mock.

    Set GEMINI_CMD to the executable if needed (default: 'gemini').
    Set GEMINI_ARGS to additional args (e.g., model selection).
    Set GEMINI_MOCK=1 to force a mock response for testing.
    """
    if os.environ.get("GEMINI_MOCK") == "1":
        return f"[S2/GEMINI MOCK] {prompt[:140]}…"

    gemini_cmd = os.environ.get("GEMINI_CMD", "gemini")
    gemini_args = os.environ.get("GEMINI_ARGS", "").strip()

    # Minimize TUI features similar to Codex handling
    env = {
        **os.environ,
        "TERM": os.environ.get("TERM", "xterm-256color"),
        "CI": os.environ.get("CI", "1"),
        "NO_COLOR": os.environ.get("NO_COLOR", "1"),
        "CLICOLOR": os.environ.get("CLICOLOR", "0"),
    }

    # Simple pass-through invocation: gemini <args> "<prompt>"
    cmd = f"{gemini_cmd} {gemini_args} {shlex.quote(prompt)}".strip()

    try:
        rc, out, err = _run_cli(cmd, env=env)
        if rc == 0 and out:
            return out
        if rc != 0:
            return f"[GEMINI_ERROR] {err or out or 'Gemini returned non-zero exit'}"
        return "[WARN] Gemini returned empty output"
    except subprocess.TimeoutExpired:
        return "[GEMINI_ERROR] Timeout while waiting for Gemini."


def with_brand_context(provider: str, prompt: str, brand_data: dict) -> str:
    provider = (provider or "codex").lower()
    if provider == "codex":
        return codex_with_brand_context(prompt, brand_data)
    if provider in ("gemini", "google", "vertex"):  # accept aliases
        context = f"""You are a brand agent. Here is the brand's identity context:\n\n{json.dumps(brand_data, indent=2)}\n\nNow complete the following task with this tone, structure, and memory:\n\n{prompt}\n"""
        return run_gemini(context)
    if provider in ("mock", "dummy"):
        return f"[MOCK/{provider.upper()}] {prompt[:160]}…"
    return f"[LLM_ERROR] Unknown provider '{provider}'."
