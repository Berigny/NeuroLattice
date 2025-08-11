SHELL := /bin/bash

.PHONY: help venv install api ui stop ports clean dev check smoke restart

VENV ?= venv
LOGDIR ?= logs
API_LOG := $(LOGDIR)/api.log
UI_LOG  := $(LOGDIR)/ui.log

help:
	@echo "Available targets:"
	@echo "  make venv     - Create Python venv ($(VENV))"
	@echo "  make install  - Upgrade pip and install requirements into venv"
	@echo "  make api      - Run FastAPI mediator (uvicorn --reload)"
	@echo "  make ui       - Run Streamlit UI"
	@echo "  make stop     - Stop any running uvicorn/streamlit processes"
	@echo "  make ports    - Force-free default ports 8000/8501 (macOS)"
	@echo "  make clean    - Remove venv"
	@echo "  make dev      - Start API+UI in background and tail logs"
	@echo "  make check    - Verify env: pexpect present, codex on PATH"
	@echo "  make smoke    - Run mock smoke test (no external CLIs)"
	@echo "  make restart  - Stop + start API and UI (no tail)"

$(VENV)/bin/activate: 
	@test -d $(VENV) || python3 -m venv $(VENV)

venv: $(VENV)/bin/activate
	@echo "Venv ready at $(VENV)"

install: venv
	. $(VENV)/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt

api: venv
	$(VENV)/bin/uvicorn agents.mediator_server:app --reload

ui: venv
	$(VENV)/bin/streamlit run ui/app.py

stop:
	pkill -f "uvicorn|streamlit" || true

ports:
	lsof -ti:8000,8501 | xargs kill -9 2>/dev/null || true

clean:
	rm -rf $(VENV)

dev: venv
	@mkdir -p $(LOGDIR)
	@echo "Stopping any previous uvicorn/streamlit processes..."
	- pkill -f "uvicorn|streamlit" || true
	@echo "Freeing ports 8000/8501 if occupied..."
	- lsof -ti:8000,8501 | xargs kill -9 2>/dev/null || true
	@echo "Starting API (uvicorn) → $(API_LOG)"
	@nohup $(VENV)/bin/uvicorn agents.mediator_server:app --reload > $(API_LOG) 2>&1 &
	@sleep 1
	@echo "Starting UI (streamlit) → $(UI_LOG)"
	@nohup $(VENV)/bin/streamlit run ui/app.py > $(UI_LOG) 2>&1 &
	@sleep 2
	@echo "Tailing logs (Ctrl-C stops tail; services keep running). Use 'make stop' to stop services."
	@tail -f $(API_LOG) $(UI_LOG)

restart: venv
	@mkdir -p $(LOGDIR)
	@echo "Restarting API and UI (background) ..."
	- pkill -f "uvicorn|streamlit" || true
	- lsof -ti:8000,8501 | xargs kill -9 2>/dev/null || true
	@nohup $(VENV)/bin/uvicorn agents.mediator_server:app --reload > $(API_LOG) 2>&1 &
	@sleep 1
	@nohup $(VENV)/bin/streamlit run ui/app.py > $(UI_LOG) 2>&1 &
	@sleep 1
	@echo "API: http://127.0.0.1:8000  UI: http://127.0.0.1:8501"
	@echo "Logs → $(API_LOG), $(UI_LOG). Tail with: tail -f $(API_LOG) $(UI_LOG)"

check: venv
	@echo "Checking Python and dependencies in $(VENV) ..."
	@. $(VENV)/bin/activate && python --version
	@. $(VENV)/bin/activate && python -c "import pexpect; print('pexpect: OK')" || (echo "pexpect: MISSING (run 'make install')" && exit 1)
	@echo "Checking codex CLI on PATH ..."
	@which codex >/dev/null 2>&1 && echo "codex: FOUND ($$(which codex))" || echo "codex: NOT FOUND (install/login separately)"

smoke: venv
	@echo "Running mock smoke test (S1=mock, S2=gemini mock) ..."
	@. $(VENV)/bin/activate && \
	  export S1_PROVIDER=mock S2_PROVIDER=gemini GEMINI_MOCK=1 && \
	  python scripts/smoke_dual_cli.py
