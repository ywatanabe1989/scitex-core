---
description: |
  [TOPIC] Environment Variables
  [DETAILS] SCITEX_* env vars read by scitex-core at import/runtime; follow SCITEX_<MODULE>_* convention.
tags: [scitex-core-env-vars]
---

# scitex-core — Environment Variables

| Variable | Purpose | Default | Type |
|---|---|---|---|
| `SCITEX_CORE_LOG_LEVEL` | Logging level for the scitex-core bootstrap logger (before scitex-logging attaches). | `INFO` | string (`DEBUG`/`INFO`/`WARNING`/`ERROR`) |
| `SCITEX_LOG_FORMAT` | Shared log-format selector (consumed by scitex-core + scitex-logging). | `plain` | string |
| `SCITEX_LOGGING_LEVEL` | Ecosystem-wide fallback log level if the core-specific var is unset. | `INFO` | string |

## Notes

- `SCITEX_CORE_LOG_LEVEL` takes precedence over `SCITEX_LOGGING_LEVEL`.
- No opt-in feature flags; no secrets.

## Audit

```bash
grep -rhoE 'SCITEX_[A-Z0-9_]+' $HOME/proj/scitex-core/src/ | sort -u
```
