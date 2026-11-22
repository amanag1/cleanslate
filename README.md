# CleanSlate

A local data quality and cleanup workbench for CSV and Excel files.

This repository contains **two separately packaged editions**. Choose one folder and follow the README inside it.

## Choose your edition

| | CleanSlate Lite | CleanSlate Production |
|---|---|---|
| Folder | `cleanslate-lite/` | `cleanslate-production/` |
| Intended use | Quickly try the product on a personal computer | API, database, container and deployment workflows |
| Interface | Streamlit | Streamlit + FastAPI |
| Core workflow | Profile, clean, validate | Profile, clean, validate |
| Input | CSV and XLSX | CSV and XLSX |
| Output | CSV, XLSX and JSON reports | CSV through API and UI downloads |
| Database/history | No database | Optional PostgreSQL processing history |
| Minimum setup | Python 3.11+ | Docker Desktop/Engine + Compose v2 |
| Kubernetes | Not required | Optional Helm starter chart |

## Which should I choose?

- **Choose Lite** if you want to test CleanSlate without Docker, PostgreSQL, Helm or Kubernetes. Start here: [CleanSlate Lite guide](cleanslate-lite/README.md).
- **Choose Production** if you want to run the API, PostgreSQL-backed history and containerized stack. Start here: [CleanSlate Production guide](cleanslate-production/README.md).

The editions are self-contained: each folder has its own dependencies, application code, sample data, tests and setup documentation. You do not need to install or run both.

## Quick start

### Lite

```bash
cd cleanslate-lite
python -m venv .venv
```

Activate the environment (Windows PowerShell: `.venv\\Scripts\\Activate.ps1`; macOS/Linux: `source .venv/bin/activate`), then:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501.

Run Lite tests from inside `cleanslate-lite`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Production

```bash
cd cleanslate-production
```

Copy `.env.example` to `.env`, set a local `POSTGRES_PASSWORD`, then:

```bash
docker compose config
docker compose up --build
```

Open the UI at http://localhost:8501 and API docs at http://localhost:8000/docs. See the Production README for automated tests, smoke tests and optional Helm instructions.

## Hardware and software requirements

- Lite: Python 3.11/3.12, 4 GB RAM minimum recommended (8 GB preferred), and internet for initial package installation.
- Production Compose: Docker Desktop/Engine with Compose v2; 8 GB RAM and about 5 GB free disk recommended.
- Helm 3 and kubectl are required only when deploying to a Kubernetes cluster.

## Scope and limitations

Both editions currently load complete files into memory and are intended for local evaluation and small-to-medium datasets. The Production edition is not yet hardened for anonymous public internet uploads. Before public exposure, add authentication/authorization, rate limiting, TLS, secret management, audit logging, resource controls and load testing. The Helm chart is a starter and does not provision PostgreSQL or a complete ingress/security layer.

## Repository-wide files

- `.github/workflows/ci.yml`: independent Lite and Production test jobs
- `LICENSE`: MIT license
- `CHANGELOG.md`: release history
