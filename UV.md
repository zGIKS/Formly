UV (Astral) — quick guide for FORMLY

This project supports being managed with `uv` (Astral). Recommended flow:

1. Install `uv` (Linux/macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Pin Python version (optional):

```bash
# pin to 3.11 (example). This writes `.python-version` used by `uv venv`
uv python pin 3.11
```

3. Create virtual environment for the project:

```bash
uv venv
source .venv/bin/activate
```

4. Install dependencies from `requirements.txt` (locked, pip-style):

```bash
uv pip sync requirements.txt
```

5. Run project scripts with `uv run` (isolated):

```bash
uv run python scripts/init_db.py
uv run uvicorn src.asgi:app --reload
```

6. Useful commands:

- `uv add <pkg>` — add a dependency and install it
- `uv lock` — create/update the lockfile
- `uv sync` — ensure the environment matches the lockfile

Notes
- `uv` has a global cache and can be significantly faster than pip for installs.
- If you prefer not to install `uv`, the classic `python -m venv` + `pip install -r requirements.txt` still works.

