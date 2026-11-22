# CleanSlate Lite

CleanSlate Lite is the simplest way to try the product. It provides the same core profiling, cleanup and validation rules as the full edition, with a local Streamlit interface. It does not require Docker, PostgreSQL, FastAPI, Kubernetes or Helm.

## Requirements
- Windows 10/11, macOS or a modern Linux distribution
- Python 3.11 or 3.12 (64-bit recommended)
- Internet access only to install Python packages the first time
- Recommended: 4 GB RAM minimum; 8 GB for larger spreadsheets
- Approximately 1–2 GB free disk space for Python, packages and temporary files (actual use varies)

## Setup

Run commands from the repository root:

```bash
python --version
python -m venv .venv-lite
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv-lite\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
.venv-lite\Scripts\activate.bat
```

**macOS/Linux**
```bash
source .venv-lite/bin/activate
```

Install only the Lite dependencies and start the application:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-lite.txt
python -m streamlit run editions/lite/app.py
```

Open the local URL printed in the terminal, normally http://localhost:8501.

## Test Lite without launching the UI

With the Lite virtual environment activated:

```bash
python -m unittest discover -s editions/lite/tests -p "test_*.py" -v
```

Expected result: 3 tests pass.

## Features
- CSV and XLSX upload
- Preview first 100 rows
- Missing, unique and duplicate profiling
- Normalize column names, trim text and optionally remove exact duplicates
- Email, integer, number/range, date and category validation
- Download profile and validation JSON
- Download cleaned CSV and XLSX

## Notes
Files are processed by the local Streamlit process. The app does not send uploaded data to a CleanSlate-hosted service. Input files are read into memory; very large files may exceed available RAM. The Lite edition has no API, database-backed history, authentication or Kubernetes deployment.
