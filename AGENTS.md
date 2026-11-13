# Agent guidance

- This is a small `uv`-managed Python 3.12 project; use `uv run ...` rather than relying on a global interpreter. The required version is recorded in `.python-version` and `pyproject.toml`.
- The installable package is `src/python_ia`; its console entry point is `python-ia`, mapped to `python_ia:main` in `pyproject.toml`. Verify it with `uv run python-ia`.
- `app.py` is the repository-root FastAPI Cloud discovery entry point; the package entry point remains `src/python_ia/main.py`.
- There are currently no test, lint, typecheck, or formatter configurations; do not assume those commands exist. For a lightweight syntax check, use `uv run python -m compileall app.py src`.
- `uv_build` is the configured build backend, and dependencies are declared in `pyproject.toml`; update that file when adding runtime dependencies.
