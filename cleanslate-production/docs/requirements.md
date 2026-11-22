# MVP Requirements

## Supported input
- CSV (UTF-8-compatible files)
- Excel .xlsx (first worksheet in MVP)

## Profile
- Total row and column counts
- Exact duplicate-row count
- Per-column dtype, missing count and percentage, and distinct count

## Cleanup controls
- Normalize column labels to lowercase snake_case
- Trim leading/trailing whitespace in string cells
- Optional exact duplicate-row removal

## Outputs
- Cleaned CSV download
- Profiling JSON response from API

## Explicit exclusions for MVP
- No automatic fuzzy corrections
- No inferred replacement of missing values
- No AI-generated transformations
- No cloud storage or account system
