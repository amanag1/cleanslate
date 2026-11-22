# System requirements and edition selection

## CleanSlate Lite
For users who want to try the data quality features without infrastructure.

Required:
- Windows 10/11, macOS or Linux
- Python 3.11 or 3.12, 64-bit recommended
- Internet access for initial pip installation
- 4 GB RAM minimum recommended; 8 GB preferred for larger files
- About 1–2 GB free disk space as a planning estimate

Installed Python packages: pandas, openpyxl and Streamlit. No Docker, PostgreSQL, FastAPI, Kubernetes, Helm or Node.js.

## CleanSlate Production (local development)
Required:
- Windows 10/11 with WSL2 for Docker Desktop, macOS or Linux
- Docker Engine/Desktop with Docker Compose v2
- Internet access to pull the Python and PostgreSQL images
- 8 GB RAM recommended; 4 GB may work for small test files
- About 5 GB free disk space recommended for images, dependencies and database volume

The Compose stack runs API, Streamlit UI and PostgreSQL. The user does not need to install Python, PostgreSQL or Streamlit directly on the host when using Compose.

Alternative native Python setup requires Python 3.11+, pip and PostgreSQL 15/16 if database history is desired.

## Kubernetes deployment (optional)
Only needed when deploying the API to a Kubernetes cluster:
- kubectl compatible with the target cluster
- Helm 3
- Access to a Kubernetes cluster
- A built and published container image
- PostgreSQL provisioned separately, plus secrets/configuration

Helm and kubectl are not required to run the application locally with Docker Compose or Lite.

## Testing
- Lite tests use Python's built-in unittest framework and only the Lite requirements.
- Full tests use pytest and the development dependencies in pyproject.toml.
- Compose integration requires Docker Compose and a working Docker daemon.
- Helm validation requires Helm; cluster deployment additionally requires kubectl and a cluster.
