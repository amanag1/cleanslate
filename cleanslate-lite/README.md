# CleanSlate Lite

The lightweight edition lets you try data profiling, cleanup and validation without Docker, PostgreSQL, FastAPI, Helm or Kubernetes.

## Requirements

- Windows 10/11, macOS or modern Linux
- Python 3.11 or 3.12 (64-bit recommended)
- Internet access for initial package installation
- 4 GB RAM minimum recommended; 8 GB preferred for larger workbooks
- About 1–2 GB free disk space as a planning estimate

## Install and run

Run commands from this folder (`cleanslate-lite`):

```bash
python --version
python -m venv .venv
```

Activate the environment:
- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- Windows CMD: `.venv\\Scripts\\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Install and launch:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed in the terminal, normally http://localhost:8501.

## Run tests

From this folder, with the virtual environment active:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Try the sample file

Upload `sample_data/customers.csv` through the UI.

## Features

- CSV and XLSX upload and preview
- Missing, unique and duplicate profiling
- Normalize column names, trim text and optionally remove exact duplicate rows
- Email, integer, number/range, date and category validation
- Download profile and validation JSON
- Download cleaned CSV and XLSX

Files are processed locally by the Streamlit process. The app does not send uploaded data to a CleanSlate-hosted service. Files are read into memory, so very large workbooks may exceed available RAM. Lite has no API, database-backed history or authentication.
