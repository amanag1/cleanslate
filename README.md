# CleanSlate

**Data Quality & Cleanup Engine** for CSV and Excel files.

CleanSlate helps analysts and small teams inspect datasets, apply predictable cleanup rules, and export cleaner files without modifying their original data.

## MVP features
- Upload CSV or Excel (.xlsx) files
- Profile columns: data types, missing values, unique values, duplicate rows
- Normalize column names
- Trim whitespace in text cells
- Remove exact duplicate rows (optional)
- Download cleaned CSV
- API-first backend built with FastAPI

## Run locally
Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
uvicorn cleanslate.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.

## API endpoints
- `GET /health` — service health
- `POST /api/v1/profile` — upload a file and return a data profile
- `POST /api/v1/clean` — upload and apply cleanup options; returns cleaned CSV

## Safety
CleanSlate does not overwrite uploaded files. Cleaning behavior is explicit and deterministic. The current MVP is intended for local development and small-to-medium files; production deployment needs additional upload limits, authentication, and storage controls.

## License
MIT. See [LICENSE](LICENSE).
