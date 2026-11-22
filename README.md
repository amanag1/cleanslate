# CleanSlate

**A practical data quality and cleanup workbench for CSV and Excel files.**

CleanSlate helps analysts inspect datasets, apply explicit cleanup operations, validate business rules and download a cleaned copy. It keeps transformations deterministic and does not overwrite the source upload.

## What it does
- Profile row/column counts, data types, missing values, distinct values and exact duplicate rows
- Normalize column labels to lowercase snake_case, resolving collisions safely
- Trim leading/trailing whitespace from text cells
- Optionally remove exact duplicate rows
- Validate columns against email, integer, number/range, date and category rules
- Export cleaned CSV files
- Provide a Streamlit analyst interface and FastAPI endpoints
- Optionally persist processing metadata in PostgreSQL

## Quick start

Python 3.11+ is required.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn cleanslate.main:app --reload
```

Open http://127.0.0.1:8000/docs for API documentation.

To launch the UI in a second terminal:

```bash
streamlit run src/cleanslate/ui/app.py
```

## Run with containers

Copy .env.example to .env, change local credentials, and run:

```bash
docker compose up --build
```

- API: http://localhost:8000/docs
- Streamlit: http://localhost:8501

The included Compose credentials are for local evaluation only. Replace them before any shared deployment.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health check |
| POST | /api/v1/profile | Dataset profile |
| POST | /api/v1/clean | Clean and download CSV |
| POST | /api/v1/validate | Apply JSON validation rules |
| GET | /api/v1/history | Recent processing metadata |

## Validation example

Send the uploaded file as multipart form data and pass a JSON string in the `rules` field:

```json
{
  "Email": {"type": "email", "required": true},
  "Age": {"type": "number", "min": 18, "max": 110}
}
```

See [validation rules](docs/validation-rules.md) for details.

## Project layout
- `src/cleanslate/engine`: reusable profiling, cleaning and validation logic
- `src/cleanslate/api`: HTTP endpoints
- `src/cleanslate/ui`: Streamlit interface
- `src/cleanslate/database`: optional SQLAlchemy persistence
- `tests`: unit and API tests
- `deploy/helm`: Kubernetes Helm chart
- `sample_data`: sample customer dataset

## Limitations and production checklist
The MVP reads CSV and XLSX (first worksheet) files into memory. It is intended for local evaluation and small-to-medium datasets, not untrusted public uploads at internet scale. Before production exposure, add authentication/authorization, rate limiting, malware scanning where appropriate, TLS/Ingress, secrets management, structured audit logging, resource limits and load testing. The Helm chart deploys the API; PostgreSQL must be provisioned separately.

## Development
Run `pytest` from the repository root. GitHub Actions runs tests on pushes and pull requests.

## License
MIT. See [LICENSE](LICENSE).
