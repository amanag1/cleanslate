# User Guide (MVP)

## Start the API
Install the package in editable mode and launch Uvicorn. Visit the interactive API docs at `/docs`.

## Profile a file
Use `POST /api/v1/profile` with a CSV or XLSX upload. The response describes dataset size, duplicate rows, and column-level missingness and uniqueness.

## Clean a file
Use `POST /api/v1/clean`. Choose whether to normalize column names, trim text whitespace, and remove exact duplicate rows. The endpoint returns a CSV download.

The original upload is not modified.
