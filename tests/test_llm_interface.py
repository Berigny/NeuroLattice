import pytest
import subprocess
import json
from unittest.mock import patch, mock_open
from neuro_lattice.llm_interface import run_codex, codex_with_brand_context

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
    mock_run.assert_called_once_with(
        ['codex', 'test prompt'],
        capture_output=True,
        text=True,
        check=True
    )

@patch('subprocess.run')
def test_run_codex_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=['codex', 'test prompt'],
        stderr='Codex error message'
    )
    result = run_codex('test prompt')
    assert result == '[ERROR] Codex CLI failed: Codex error message'
    mock_run.assert_called_once_with(
        ['codex', 'test prompt'],
        capture_output=True,
        text=True,
        check=True
    )

@patch('neuro_lattice.llm_interface.run_codex')
@patch('builtins.open', new_callable=mock_open)
def test_codex_with_brand_context(mock_file_open, mock_run_codex):
    mock_brand_data = {"brand_identity_kernel": {"key": "value"}}
    mock_file_open.return_value.read.return_value = json.dumps(mock_brand_data)
    mock_run_codex.return_value = 'Contextualized Codex output'

    prompt = 'My specific task'
    result = codex_with_brand_context(prompt, 'test_brand_signature.json')

    expected_context = f"""You are a brand agent. Here is the brand's identity context:\n\n{json.dumps(mock_brand_data, indent=2)}\n\nNow complete the following task with this tone, structure, and memory:\n\n{prompt}\n"""

    mock_file_open.assert_called_once_with('test_brand_signature.json', 'r')
    mock_run_codex.assert_called_once_with(expected_context)
    assert result == 'Contextualized Codex output'
