SHELL := /bin/bash

.PHONY: help venv install api ui stop ports clean dev

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
