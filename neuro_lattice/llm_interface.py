import os
import sys
import subprocess
import shlex
import json
import pty

try:
    import pexpect  # type: ignore
except Exception:
    pexpect = None

def _run_once(prompt: str, use_pty: bool, inject_cursor_reply: bool=False) -> tuple[int, str, str]:
    """Run the codex CLI once, optionally under a pseudo‑TTY.

    Returns (returncode, stdout, stderr).
    """
    base_cmd = f"codex {shlex.quote(prompt)}"
    # Some CLIs try to query cursor position via DSR (ESC[6n).
    # When headless, inject a plausible reply "ESC[1;1R" via stdin.
    if inject_cursor_reply:
        # Use a shell to construct the pipeline safely
        pipeline = f"printf '\033[1;1R' | {base_cmd}"
    else:
        pipeline = base_cmd

    env = {
        **os.environ,
        "TERM": (os.environ.get("TERM", "xterm-256color") if use_pty else "dumb"),
        "NO_COLOR": "0" if use_pty else "1",
        "CLICOLOR": "1" if use_pty else "0",
        # Hint CLIs to avoid fancier TUI behavior.
        "CI": os.environ.get("CI", "1"),
        "CODEX_NONINTERACTIVE": os.environ.get("CODEX_NONINTERACTIVE", "1"),
    }

    if use_pty:
        try:
            master, slave = pty.openpty()
            # The pipeline is now just the base command, no shell injection
            pipeline = base_cmd
            process = subprocess.Popen(
                pipeline,
                shell=True,
                stdin=slave,
                stdout=slave,
                stderr=slave,
                close_fds=True,
                env=env,
                text=True
            )

            # If injecting, write the reply directly to the master fd
            if inject_cursor_reply:
                os.write(master, b'\033[1;1R')

            os.close(slave)

            output = []
            while True:
                try:
                    data = os.read(master, 1024)
                    if not data:
                        break
                    output.append(data.decode())
                except OSError:
                    break
            
            process.wait(timeout=120)
            rc = process.returncode
            out = "".join(output)
            err = "" 
            os.close(master)
            return rc, out.strip(), err.strip()

        except Exception as e:
            return 1, "", str(e)
    else:
        cmd = pipeline
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

def _run_codex_pexpect(prompt: str, timeout: int = 120) -> tuple[int, str, str]:
    """Run Codex via pexpect (PTY), better for server contexts.

    Returns (rc, stdout, stderr_message).
    """
    if pexpect is None:
        return 127, "", "pexpect not available"

    # Construct command via a shell to reuse quoting behavior
    cmd = f"codex {shlex.quote(prompt)}"

    env = {
        **os.environ,
        # Present a terminal; disable color/TUI as much as possible
        "TERM": os.environ.get("TERM", "xterm-256color"),
        "CI": os.environ.get("CI", "1"),
        "NO_COLOR": os.environ.get("NO_COLOR", "1"),
        "CLICOLOR": os.environ.get("CLICOLOR", "0"),
        "CODEX_NONINTERACTIVE": os.environ.get("CODEX_NONINTERACTIVE", "1"),
    }
    child = None
    try:
        # Use bash -lc so PATH and shell quoting work as in a user terminal
        child = pexpect.spawn(
            "/bin/bash",
            ["-lc", cmd],
            env=env,
            encoding="utf-8",
            timeout=timeout,
        )
        child.delaybeforesend = 0

        # Accumulate output and dynamically respond to cursor position queries (ESC[6n)
        output_parts: list[str] = []
        # Patterns: DSR request, EOF, or TIMEOUT
        patterns = [r"\x1b\[6n", pexpect.EOF, pexpect.TIMEOUT]
        while True:
            i = child.expect(patterns)
            if i == 0:
                # DSR request detected; collect prior output and inject a plausible reply
                if child.before:
                    output_parts.append(child.before)
                try:
                    child.send("\x1b[1;1R")
                except Exception:
                    pass
                continue
            if i == 1:  # EOF
                if child.before:
                    output_parts.append(child.before)
                break
            if i == 2:  # TIMEOUT
                raise pexpect.TIMEOUT

        output = "".join(output_parts)
        rc = child.exitstatus if child.exitstatus is not None else (child.signalstatus or 0)
        # Filter benign notices
        if "Update available" in output:
            output = "\n".join(
                line for line in output.splitlines() if "Update available" not in line
            )
        return rc or 0, output.strip(), ""
    except pexpect.TIMEOUT:
        if child is not None:
            try:
                child.close(force=True)
            except Exception:
                pass
        return 124, "", "Timeout while waiting for Codex (pexpect)."
    except Exception as e:
        if child is not None:
            try:
                child.close(force=True)
            except Exception:
                pass
        return 1, "", str(e)


def run_codex(prompt: str) -> str:
    """Invoke codex robustly in non-/interactive contexts.

    Order of attempts:
    1) pexpect PTY (preferred for servers) unless FORCE_SUBPROCESS=1
    2) subprocess with PTY injection helpers
    """
    # Prefer pexpect unless explicitly disabled
    if os.environ.get("FORCE_SUBPROCESS") != "1":
        rc, out, err = _run_codex_pexpect(prompt)
        if rc == 0 and out:
            return out
        if rc == 0 and not out:
            return "[WARN] Codex returned empty output"
        # If pexpect path failed, capture message and fall back
        last_err = err or out
    else:
        last_err = ""

    try:
        # Fallback to subprocess strategy
        force_pty = os.environ.get("FORCE_PTY") == "1"

        rc, out, err = _run_once(prompt, use_pty=bool(force_pty), inject_cursor_reply=True)

        if "Update available" in err and rc == 0:
            err = ""

        combined = f"{err}\n{out}".lower()
        has_codex_error_marker = "[codex_error]" in combined
        tty_issue = (
            "cursor position" in combined
            or "could not be read" in combined
            or ("tty" in combined and "error" in combined)
        )

        if rc == 0 and out and not has_codex_error_marker and not tty_issue:
            return out

        if not force_pty and (tty_issue or has_codex_error_marker):
            rc2, out2, err2 = _run_once(prompt, use_pty=False, inject_cursor_reply=True)
            if "Update available" in err2 and rc2 == 0:
                err2 = ""
            comb2 = f"{err2}\n{out2}".lower()
            if rc2 == 0 and out2 and "[codex_error]" not in comb2:
                return out2
            rc3, out3, err3 = _run_once(prompt, use_pty=True, inject_cursor_reply=True)
            if "Update available" in err3 and rc3 == 0:
                err3 = ""
            comb3 = f"{err3}\n{out3}".lower()
            if rc3 == 0 and out3 and "[codex_error]" not in comb3:
                return out3
            err = err3 or err2 or err
            out = out3 or out2 or out
            rc = rc3 or rc2 or rc

        if rc != 0:
            msg = err or out or last_err or "Codex returned non-zero exit"
            return f"[CODEX_ERROR] {msg}"

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
    use_stdin = os.environ.get("GEMINI_USE_STDIN") == "1"

    # Minimize TUI features similar to Codex handling
    env = {
        **os.environ,
        "TERM": os.environ.get("TERM", "xterm-256color"),
        "CI": os.environ.get("CI", "1"),
        "NO_COLOR": os.environ.get("NO_COLOR", "1"),
        "CLICOLOR": os.environ.get("CLICOLOR", "0"),
    }

    # Two modes:
    # 1) Arg mode (default): gemini <args> "<prompt>"
    # 2) STDIN mode (opt-in): printf "<prompt>" | gemini <args>
    if use_stdin:
        cmd = f"printf %s {shlex.quote(prompt)} | {gemini_cmd} {gemini_args}".strip()
    else:
        cmd = f"{gemini_cmd} {gemini_args} {shlex.quote(prompt)}".strip()

    try:
        rc, out, err = _run_cli(cmd, env=env)
        if rc == 0 and out:
            return out
        if rc != 0:
            # Fallback: if arg mode failed, try stdin mode once
            if not use_stdin:
                alt_cmd = f"printf %s {shlex.quote(prompt)} | {gemini_cmd} {gemini_args}".strip()
                rc2, out2, err2 = _run_cli(alt_cmd, env=env)
                if rc2 == 0 and out2:
                    return out2
                return f"[GEMINI_ERROR] {err2 or err or out2 or out or 'Gemini returned non-zero exit'}"
            return f"[GEMINI_ERROR] {err or out or 'Gemini returned non-zero exit'}"
        return "[WARN] Gemini returned empty output"
    except subprocess.TimeoutExpired:
        return "[GEMINI_ERROR] Timeout while waiting for Gemini."


def with_brand_context(provider: str, prompt: str, brand_data: dict) -> str:
    provider = (provider or "codex").lower()
    if provider == "codex":
        return codex_with_brand_context(prompt, brand_data)
    if provider in ("gemini", "google", "vertex"):  # accept aliases
        context = f"""You are a brand agent. Here is the brand's identity context:\n\n{json.dumps(brand_data, indent=2)}

Now complete the following task with this tone, structure, and memory:\n\n{prompt}\n"""
        return run_gemini(context)
    if provider in ("mock", "dummy"):
        return f"[MOCK/{provider.upper()}] {prompt[:160]}…"
    return f"[LLM_ERROR] Unknown provider '{provider}'."
