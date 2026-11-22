# CleanSlate Production Edition — setup and test guide

This edition includes the FastAPI service, Streamlit UI, optional PostgreSQL processing history, container build and Helm deployment starter.

## Option A: Run the complete local stack with Docker Compose (recommended)

### Host requirements
- Windows 10/11 + Docker Desktop with WSL2, macOS + Docker Desktop, or Linux + Docker Engine
- Docker Compose v2 (the `docker compose` command)
- Internet access to pull images and Python dependencies
- 8 GB RAM recommended and about 5 GB free disk space

You do not need to install Python, PostgreSQL, FastAPI or Streamlit separately on the host for this route.

### Start
From the repository root:

```bash
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env` instead. Edit `.env` and set a strong local `POSTGRES_PASSWORD`.

```bash
docker compose config
docker compose up --build
```

Open:
- API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health
- Streamlit UI: http://localhost:8501

### Functional smoke test
1. Open the UI and upload `sample_data/customers.csv`.
2. Confirm row/column counts and duplicate count appear.
3. Enable column normalization and whitespace trimming.
4. Enable duplicate removal and run cleanup.
5. Download the cleaned CSV and confirm the duplicate row is removed.
6. Use the validation expander or API docs to validate the Email column.
7. Call `GET /api/v1/history` in the API docs and confirm job metadata is stored.

Example API profile test using curl:

```bash
curl -F "file=@sample_data/customers.csv" http://localhost:8000/api/v1/profile
```

### Stop
```bash
docker compose down
```

To remove the local PostgreSQL data volume as well (destructive):
```bash
docker compose down -v
```

## Option B: Native Python development (without containers)
- Python 3.11+
- PostgreSQL 15/16 if you want processing history; without `DATABASE_URL`, history is disabled
- Install: `python -m pip install -e ".[dev]"`
- Run API: `uvicorn cleanslate.main:app --reload`
- Run UI in another terminal: `streamlit run src/cleanslate/ui/app.py`

## Automated tests
With the full development dependencies installed:

```bash
python -m compileall -q src tests
python -m pytest -v
```

The tests cover the engine and selected API behavior. They do not replace the Compose smoke test above.

## Optional Kubernetes / Helm deployment
Kubernetes is not required for local evaluation. For a cluster deployment:
1. Install kubectl and Helm 3.
2. Build and publish the API image to a registry accessible by the cluster.
3. Update `deploy/helm/cleanslate/values.yaml` with the image repository and tag.
4. Provision PostgreSQL separately and configure the deployment's `DATABASE_URL` using Kubernetes Secrets (the current starter chart needs extending to inject this secret).
5. Configure Ingress/TLS, authentication, resource policies and monitoring before exposing it.

Validate chart rendering:
```bash
helm lint deploy/helm/cleanslate
helm template cleanslate deploy/helm/cleanslate
```

The current Helm chart is a starter for the API only; it does not install PostgreSQL or provide a production-ready ingress/security configuration.
