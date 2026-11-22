# Local runbook

## API
1. Create and activate a Python 3.11+ virtual environment.
2. Install with pip install -e ".[dev]".
3. Run uvicorn cleanslate.main:app --reload.
4. Open /docs on localhost port 8000.

## Streamlit UI
Run streamlit run src/cleanslate/ui/app.py from the repository root.

## Compose
Copy .env.example to .env, replace all local credentials, then run docker compose up --build. The local Compose configuration includes PostgreSQL, API and Streamlit UI. API docs are on port 8000; UI is on port 8501.

## Tests
Run pytest. CI runs the same suite on pushes and pull requests.

## Kubernetes
Build and publish an image, configure deploy/helm/cleanslate/values.yaml with its registry path and tag, then install the chart with Helm. Configure secrets, ingress/TLS and persistent database infrastructure separately; the chart does not provision PostgreSQL.
