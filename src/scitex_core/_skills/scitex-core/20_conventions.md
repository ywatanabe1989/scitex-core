---
description: |
  [TOPIC] Conventions
  [DETAILS] Import style, logging defaults, shadowed stdlib names (str/dict).
tags: [scitex-core-conventions]
---

# Conventions

Rules every consumer of `scitex-core` should follow.

## Import style

Re-exported from both `scitex_core` and (via the umbrella package)
`scitex.core`. Docs across the ecosystem use:

```python
import scitex
scitex.core.logging.getLogger(__name__)
```

In first-party code, import the sub-module directly:

```python
from scitex_core import logging as sx_logging
from scitex_core import sh
```

## Names that shadow stdlib

`scitex_core.str` and `scitex_core.dict` shadow Python builtins. If you
`from scitex_core import str`, alias it (`sstr`) so the builtin remains
accessible.

## Environment variables

Per ecosystem rule (see `general/16_environment-variables.md`) every
env var is prefixed `SCITEX_CORE_*`. Examples:

* `SCITEX_CORE_LOG_LEVEL` — default level for the auto-configured root logger.

Never read bare `SCITEX_*` variables from this package.

## Logging auto-configure

Importing `scitex_core.logging` configures the root logger with console
+ rotating-file output the first time. Call `configure(...)` explicitly
if you need different behavior; multiple calls are idempotent.

## Safe shell (no shell=True)

`scitex_core.sh.sh` refuses string commands. Always pass a list. For
pipes, chain `subprocess.Popen` yourself — this is deliberate, not an
oversight.

## No CLI, no MCP

`scitex-core` is a pure library. It intentionally exposes neither a
`[project.scripts]` entry point nor an MCP server; higher-level packages
compose its utilities behind their own interfaces.
