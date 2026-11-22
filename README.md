# CleanSlate

**A data quality and cleanup workbench for CSV and Excel files.**

CleanSlate is available in two editions. Choose the one that matches your machine and what you want to evaluate.

## Choose your edition

| | CleanSlate Lite | CleanSlate Production |
|---|---|---|
| Best for | Trying the core product quickly | API, database and deployment workflows |
| Install | Python packages only | Docker Compose recommended |
| UI | Streamlit | Streamlit |
| Core features | Profile, clean, validate | Profile, clean, validate |
| Exports | CSV and XLSX | CSV through API; UI cleanup download |
| API | No | FastAPI |
| Processing history | No database | Optional PostgreSQL |
| Docker | Not required | Required for Compose route |
| Helm/Kubernetes | Not required | Optional, only for cluster deployment |

**New to CleanSlate? Start with Lite.** It does not require Docker, PostgreSQL, Helm or Kubernetes.

## System requirements

See [System requirements](docs/system-requirements.md) for operating-system notes, RAM/disk guidance and optional tools.

### Lite
- Windows 10/11, macOS or Linux
- Python 3.11 or 3.12 (64-bit recommended)
- Internet access for initial package installation
- 4 GB RAM minimum recommended; 8 GB preferred for larger workbooks
- No Docker, PostgreSQL, FastAPI, Helm or Kubernetes

### Production — local Compose
- Windows 10/11 with Docker Desktop + WSL2, macOS with Docker Desktop, or Linux with Docker Engine
- Docker Compose v2
- 8 GB RAM recommended and about 5 GB free disk space
- No host Python or PostgreSQL installation required for the Compose route

### Kubernetes
Helm 3, kubectl and a reachable Kubernetes cluster are needed only for an actual Kubernetes deployment. They are not required for local testing.

## Run CleanSlate Lite

From the repository root:

```bash
python -m venv .venv-lite
```

Activate it:

**Windows PowerShell:** `.\.venv-lite\Scripts\Activate.ps1`

**Windows CMD:** `.venv-lite\Scripts\activate.bat`

**macOS/Linux:** `source .venv-lite/bin/activate`

Install and launch:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-lite.txt
python -m streamlit run editions/lite/app.py
```

Open http://localhost:8501. Full guide: [Lite setup and tests](editions/lite/README.md).

### Test Lite

```bash
python -m unittest discover -s editions/lite/tests -p "test_*.py" -v
```

This test command uses Python's built-in unittest runner; it does not need pytest.

## Run CleanSlate Production

The easiest complete local setup uses Docker Compose. You need Docker Desktop/Engine and Compose v2.

1. Copy `.env.example` to `.env` (PowerShell: `Copy-Item .env.example .env`).
2. Edit `.env` and set a strong local `POSTGRES_PASSWORD`.
3. Validate and start:

```bash
docker compose config
docker compose up --build
```

Open:
- Streamlit UI: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

Full instructions and manual test cases: [Production setup and test guide](docs/setup-production.md).

### Test Production

With the full development dependencies installed in a Python 3.11+ environment:

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src tests
python -m pytest -v
```

For the database-backed integration smoke test, start Compose and verify that `GET /api/v1/history` returns processing metadata after profiling or cleaning a file in the UI.

## Features

- Dataset profiling: row/column counts, data types, missing values, distinct values and exact duplicates
- Cleanup: normalize column names, trim text and optionally remove exact duplicate rows
- Validation: email, integer, number/range, date and category rules
- CSV/XLSX input
- Lite: cleaned CSV/XLSX download and JSON profile/validation downloads
- Production: FastAPI endpoints, Streamlit UI and optional PostgreSQL processing metadata

## API overview (Production)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health check |
| POST | /api/v1/profile | Dataset profile |
| POST | /api/v1/clean | Clean and download CSV |
| POST | /api/v1/validate | Apply JSON validation rules |
| GET | /api/v1/history | Recent processing metadata |

## Project structure

- `src/cleanslate`: Production API, engine, UI and database
- `editions/lite`: standalone lightweight UI, engine and tests
- `requirements-lite.txt`: minimal Lite dependencies
- `tests`: Production tests
- `sample_data`: sample dataset
- `docs`: system requirements, setup, architecture and product notes
- `deploy/helm`: optional Kubernetes starter chart

## Important limitations

The application currently reads complete files into memory. It is designed for local evaluation and small-to-medium datasets, not anonymous public uploads at internet scale. Production exposure requires authentication/authorization, rate limiting, TLS, secret management, audit logging, resource controls and load testing. The Helm chart is a starter and does not provision PostgreSQL or configure a complete production ingress/security layer.

## License

MIT. See [LICENSE](LICENSE).
