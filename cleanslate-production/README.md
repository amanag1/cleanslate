# CleanSlate Production

The advanced edition includes a FastAPI service, Streamlit UI, optional PostgreSQL processing history, Docker Compose deployment and a starter Helm chart.

## Requirements

Recommended local route: Windows 10/11 with Docker Desktop + WSL2, macOS with Docker Desktop, or Linux with Docker Engine; Docker Compose v2; internet access for image/package downloads; 8 GB RAM and about 5 GB free disk.

You do not need host-installed Python, PostgreSQL, FastAPI or Streamlit when using Docker Compose.

## Run with Docker Compose

Run these commands from this folder (`cleanslate-production`).

1. Copy `.env.example` to `.env` (PowerShell: `Copy-Item .env.example .env`; macOS/Linux: `cp .env.example .env`).
2. Set a strong local `POSTGRES_PASSWORD` in `.env`.
3. Validate and start:

```bash
docker compose config
docker compose up --build
```

Open the Streamlit UI at http://localhost:8501, API docs at http://localhost:8000/docs, and health endpoint at http://localhost:8000/health.

## Functional smoke test

1. Upload `sample_data/customers.csv` in the UI.
2. Check row/column counts, missing values and duplicates.
3. Enable column normalization, whitespace trimming and duplicate removal.
4. Run cleanup, download the CSV and inspect the result.
5. Try email validation from the UI or API docs.
6. Open `GET /api/v1/history` and confirm processing metadata is recorded when database configuration is enabled.

Example API request:

```bash
curl -F "file=@sample_data/customers.csv" http://localhost:8000/api/v1/profile
```

Stop the stack with `docker compose down`. To also delete the local PostgreSQL data volume (destructive), run `docker compose down -v`.

## Automated tests

For tests without Docker, install Python 3.11+ and run from this folder:

```bash
python -m venv .venv
```

Activate it (Windows PowerShell: `.venv\\Scripts\\Activate.ps1`; macOS/Linux: `source .venv/bin/activate`), then:

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src tests
python -m pytest -v
```

These tests cover selected engine and API behavior. They do not replace the Compose smoke test.

## Optional Kubernetes / Helm

Kubernetes is not needed for local evaluation. For cluster deployment, install Helm 3 and kubectl, build and publish the API image, update `deploy/helm/cleanslate/values.yaml`, provision PostgreSQL separately, and configure the database URL through Kubernetes Secrets. The current chart is an API-only starter and needs secret injection, ingress/TLS, authentication, resource policies and monitoring before production exposure.

Validate chart rendering:

```bash
helm lint deploy/helm/cleanslate
helm template cleanslate deploy/helm/cleanslate
```

## Contents

- `src/cleanslate`: API, engine, UI, services and database integration
- `tests`: Production tests
- `deploy/helm`: starter Helm chart
- `docs`: architecture, requirements, runbook and validation notes
- `sample_data`: sample CSV
- `Dockerfile`, `compose.yaml`, `.env.example`: local container stack
- `pyproject.toml`: Python package and development dependencies

## Limitations

The application reads complete files into memory. Do not expose it to anonymous public uploads without authentication, authorization, rate limits, TLS, secret management, audit logging, resource limits and load testing.
