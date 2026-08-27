PYTHON ?= python3
TECTONIC ?= tectonic
SOURCE_DATE_EPOCH ?= 1787702400
export SOURCE_DATE_EPOCH

.PHONY: install test reproduce figures tables paper all

install:
	$(PYTHON) -m pip install -r requirements-lock.txt
	$(PYTHON) -m pip install --no-deps --no-build-isolation -e .

test:
	$(PYTHON) -m pytest

reproduce:
	$(PYTHON) scripts/reproduce_2012_channel.py

figures:
	$(PYTHON) scripts/build_figures.py

tables:
	$(PYTHON) scripts/build_tables.py

paper: figures tables
	@command -v $(TECTONIC) >/dev/null 2>&1 || { echo "Tectonic 0.17.0 is required; no PDF was produced" >&2; exit 127; }
	$(TECTONIC) --keep-logs --outdir paper paper/main.tex

all: test reproduce figures tables paper
