# Validation rules

Send a JSON object mapping column names to rule definitions to POST /api/v1/validate.

Supported types:
- email: basic email-format check
- integer: numeric values with no fractional component
- number: numeric values, optionally constrained by min and max
- date: parseable date values
- category: values included in an allowed list

Any rule may set required: true to flag missing or blank values.

Example:
```json
{
  "Email": {"type": "email", "required": true},
  "Age": {"type": "number", "min": 18, "max": 110},
  "Status": {"type": "category", "allowed": ["Active", "Inactive"]}
}
```
