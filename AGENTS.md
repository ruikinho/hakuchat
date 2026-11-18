# AGENTS.md

## Repo shape
- Single-file Python script: `weather.py`
- No git repo, no `requirements.txt`, no `pyproject.toml`, no package manager config, no tests, no lint/typecheck config, no CI

## Running
1. Install dependency: `pip install openai`
2. Set env var: `OPEN_ROUTER_UUS` (read directly via `os.environ["OPEN_ROUTER_UUS"]` — no `.env` loading, no fallback)
3. Run: `python weather.py`

## Behavior
- Calls OpenRouter (`base_url="https://openrouter.ai/api/v1"`), model `nvidia/nemotron-3.5-super-vl:free`
- Sends a `get_current_temperature` function tool definition; prints any tool calls the model returns (does not execute the tool itself)

## Conventions
- Env var name `OPEN_ROUTER_UUS` is taken verbatim from `weather.py:24`; do not "fix" it to something like `OPENROUTER_API_KEY` without confirming intent — there are no tests to catch a mismatch.
- No formal verification step exists; `python weather.py` is the only executable check.
