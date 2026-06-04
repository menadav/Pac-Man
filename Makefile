PYTHON   ?= python3
PIP      ?= $(PYTHON) -m pip
CONFIG   ?= config.json
ENTRY    ?= pac_man.py

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
             --disallow-untyped-defs --check-untyped-defs

.PHONY: all install run debug clean lint lint-strict package help

all: run

help:
	@echo "Objetivos disponibles:"
	@echo "  install      Instala las dependencias"
	@echo "  run          Lanza el juego (CONFIG=$(CONFIG))"
	@echo "  debug        Lanza el juego dentro de pdb"
	@echo "  clean        Borra cachés y artefactos"
	@echo "  lint         flake8 . y mypy . con los flags requeridos"
	@echo "  lint-strict  flake8 . y mypy . --strict"
	@echo "  package      Genera un binario autonomo con PyInstaller"

install:
	@echo "[install] Instalando dependencias..."
	$(PIP) install --upgrade pip
	$(PIP) install ./src/map/mazegenerator-00001-py3-none-any
	$(PIP) install -e .

run:
	$(PYTHON) $(ENTRY) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(ENTRY) $(CONFIG)

clean:
	@echo "[clean] Borrando cachés..."
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	@rm -rf build dist *.egg-info src/*.egg-info

lint:
	flake8 .
	mypy . $(MYPY_FLAGS) --exclude build

lint-strict: install
	flake8 .
	mypy . --strict --exclude build

package:
	$(PIP) install pyinstaller
	pyinstaller pacman.spec
