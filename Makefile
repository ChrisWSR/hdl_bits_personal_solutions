.PHONY: test init lint clean

PIP := $(shell command -v pip3 || command -v pip)
PYTHON := $(shell command -v python3 || command -v python)

test:   ## Run all tests with pytest & cocotb
	$(PYTHON) -m pytest tests/ -v --tb=short

report: ## Run all tests and write JUnit XML report
	$(PYTHON) -m pytest tests/ -v --tb=short --junitxml=_generated/report.xml

test-one: ## Usage: make test-one FILE=basics/03_and_gate.v
	$(PYTHON) -m pytest tests/ -v --tb=short -k "$(FILE)"

list:   ## Show collected tests without running
	$(PYTHON) -m pytest tests/ --collect-only -q

init:   ## Generate per-directory tests.yaml files
	$(PYTHON) run_tests.py --init

lint:   ## Lint all Verilog files with Verilator (if installed)
	@which verilator >/dev/null 2>&1 || { echo "verilator not found"; exit 1; }
	@find . -name '*.v' -not -path './_generated/*' -exec verilator --lint-only {} + 2>&1 || true

clean:  ## Remove generated files, sim_build dirs, and caches
	rm -rf _generated/
	find . -name sim_build -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name .pytest_cache -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name tests.yaml -not -path './_generated/*' -exec rm {} +

help:   ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'
