# Architecture

CleanSlate separates transport, ingestion, transformation and persistence.

- FastAPI exposes profile, clean, validate and history endpoints.
- The engine contains deterministic dataframe operations independent of HTTP.
- The file service validates file extension and enforces a configurable upload limit.
- The history service stores processing metadata only when PostgreSQL is configured.
- Streamlit provides a local analyst interface using the same engine functions.
- Uploaded file contents are not persisted.

## Deployment considerations
Compose is intended for local evaluation. Replace local-only credentials before use beyond a developer machine. Production requires authentication, TLS, secret management, throttling, resource quotas, observability and a deliberate file-storage policy. The Helm chart currently deploys the API only.
