# CleanSlate Lite — setup and test guide

See [the Lite edition README](../editions/lite/README.md) for OS-specific activation commands.

Short version from the repository root:

```bash
python -m venv .venv-lite
# Activate the environment for your operating system
python -m pip install -r requirements-lite.txt
python -m streamlit run editions/lite/app.py
```

Open http://localhost:8501. Upload `sample_data/customers.csv` and try profile, cleanup, validation and exports.

Run Lite tests:

```bash
python -m unittest discover -s editions/lite/tests -p "test_*.py" -v
```

Lite does not require Docker, PostgreSQL, FastAPI, Helm or Kubernetes.
