# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

cfdb-vars is a Python package that separates variable metadata from the main `cfdb` package, allowing variables to be added independently. Uses Hatchling as the build backend and UV as the package manager. Python >=3.10, no runtime dependencies.

## Commands

```bash
# Setup
uv sync

# Testing
uv run pytest
uv run pytest --cov --cov-report=xml
uv run pytest cfdb_vars/tests/test_specific.py::test_name  # single test

# Linting & formatting
uv run ruff check .
uv run ruff check --fix .
uv run black --check --diff .
uv run black .
uv run mypy --install-types --non-interactive cfdb_vars

# Documentation
uv run mkdocs build
uv run mkdocs serve
```

## Code Style

- Line length: 120
- Black with `skip-string-normalization` (prefer single quotes)
- Target: Python 3.10
- No relative imports (enforced by ruff `ban-relative-imports = "all"`)
- Ruff rule F401 (unused imports) is unfixable — do not auto-remove unused imports
- Tests relax rules: PLR2004 (magic values), S101 (assert), TID252 (relative imports)

## Architecture

- `cfdb_vars/__init__.py` — package entry point, single source for `__version__`
- `cfdb_vars/tests/` — pytest test suite with `conftest.py` for fixtures
- Version is read by Hatchling from `__version__` in `__init__.py`
- Publishing: git tags trigger CI to build and publish to PyPI via `uv publish`
