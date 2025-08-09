import pytest
import subprocess
import json
from unittest.mock import patch, mock_open
from neuro_lattice.llm_interface import run_codex, codex_with_brand_context
import os
import shlex

class MockCompletedProcess:
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

@patch('subprocess.run')
def test_run_codex_success(mock_run):
    mock_run.return_value = MockCompletedProcess(stdout='Codex output success', stderr='', returncode=0)
    result = run_codex('test prompt')
    assert result == 'Codex output success'
    cmd = f'script -q /dev/null codex {shlex.quote("test prompt")}'
    mock_run.assert_called_once_with(
        cmd, shell=True,
        capture_output=True, text=True, check=False, timeout=120,
        env={**os.environ, "TERM":"xterm-256color"}
    )

@patch('subprocess.run')
def test_run_codex_failure(mock_run):
    mock_run.return_value = MockCompletedProcess(stdout='', stderr='Codex error message', returncode=1)
    result = run_codex('test prompt')
    assert result == '[CODEX_ERROR] Codex error message'
    cmd = f'script -q /dev/null codex {shlex.quote("test prompt")}'
    mock_run.assert_called_once_with(
        cmd, shell=True,
        capture_output=True, text=True, check=False, timeout=120,
        env={**os.environ, "TERM":"xterm-256color"}
    )

@patch('subprocess.run')
def test_run_codex_timeout(mock_run):
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="codex", timeout=120)
    result = run_codex('test prompt')
    assert result == '[CODEX_ERROR] Timeout while waiting for Codex.'

@patch('neuro_lattice.llm_interface.run_codex')
def test_codex_with_brand_context(mock_run_codex):
    mock_brand_data = {"brand_identity_kernel": {"key": "value"}}
    mock_run_codex.return_value = 'Contextualized Codex output'

    prompt = 'My specific task'
    result = codex_with_brand_context(prompt, mock_brand_data)

    expected_context = f"""You are a brand agent. Here is the brand's identity context:

{json.dumps(mock_brand_data, indent=2)}

Now complete the following task with this tone, structure, and memory:

{prompt}
"""
    mock_run_codex.assert_called_once_with(expected_context)
    assert result == 'Contextualized Codex output'