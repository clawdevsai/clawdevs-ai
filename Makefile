PYTHON ?= python

.PHONY: help test clean

help:
	@echo "make test   - executa a suite"
	@echo "make check-runtime-stack - valida OpenClaw + Ollama"
	@echo "make clean  - remove caches Python"

test:
	@$(PYTHON) -m pytest -q

check-runtime-stack:
	@$(PYTHON) -m app.runtime.check_stack

clean:
	@cmd /c "for /d /r %d in (__pycache__) do @if exist \"%d\" rd /s /q \"%d\"" || true
	@cmd /c "if exist .pytest_cache rd /s /q .pytest_cache" || true
