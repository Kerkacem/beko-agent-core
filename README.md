Self-building agent scaffold

Setup
-----

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Environment
-----------

- Set `GROQ_API_KEY` environment variable if you want live Groq calls.

Quick run
---------

- Neural health check:

```powershell
python beko_v5_neural.py
```

- Run self-agent UI:

```powershell
python beko_self_agent.py
```

Development
-----------

- Tests: `pytest -q`
- Add model weights to `models/` and document training in `docs/`.
