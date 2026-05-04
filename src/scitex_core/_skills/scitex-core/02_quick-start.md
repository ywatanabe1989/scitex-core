---
description: |
  [TOPIC] scitex-core Quick start
  [DETAILS] Representative one-liners from each bundled submodule — logging, path, sh, str, dict.
tags: [scitex-core-quick-start]
---

# Quick Start

## Logging with SUCCESS / FAIL levels

```python
from scitex_core import logging

log = logging.getLogger(__name__)
log.success("trained 10 epochs")
log.fail("dataset missing — aborting")
```

## Path helpers

```python
from scitex_core import path

repo = path.find_git_root()
out  = path.mk_spath("results.csv")     # script_out/<session>/results.csv
```

## Safe shell

```python
from scitex_core import sh

result = sh.sh(["git", "status", "--porcelain"], return_as="dict")
print(result["stdout"])
```

## Dict + str helpers

```python
from scitex_core import dict as d, str as s

cfg = d.DotDict({"a": {"b": 1}})
print(cfg.a.b)

s.printc("ok", c="green")
```

## Reproducibility

```python
from scitex_core import repro

session_id = repro.gen_id()             # short, unique, time-prefixed
repro.fix_seeds(42)                     # numpy + random + torch (if present)
```

## Next

- [11_python-api-std](11_python-api-std.md) — `errors`, `logging`, `sh`, `path`, `str` legacy details
- [12_python-api-data](12_python-api-data.md) — `dict`, `types`, `dt`, `parallel`, `repro` legacy details
- [20_conventions](20_conventions.md) — import style, shadowed stdlib names
- [21_env-vars](21_env-vars.md) — `SCITEX_*` env vars
