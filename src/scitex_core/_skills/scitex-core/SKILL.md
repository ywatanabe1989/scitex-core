---
name: scitex-core
description: Foundation layer for the SciTeX ecosystem — imported by every other SciTeX package. Bundles 10 standalone utility modules under one roof: `scitex_core.logging` (stdlib-logging + SUCCESS/FAIL levels + SciTeXError hierarchy), `scitex_core.errors` (shortcut to `logging`'s exception tree), `scitex_core.sh` (safe shell-exec with timeout/capture), `scitex_core.path` (find_file/find_git_root/symlink helpers/session paths), `scitex_core.str` (colored prints, LaTeX fallback, grep/parse/replace), `scitex_core.dict` (`DotDict`, `safe_merge`, `flatten`), `scitex_core.types` (`ArrayLike`, `ColorLike`, runtime predicates), `scitex_core.dt` (datetime/timestamp utilities), `scitex_core.parallel` (one-shot `run(func, args)` thread-pool with tqdm), `scitex_core.repro` (`RandomStateManager`, `gen_ID`, `hash_array`). No umbrella `scitex.core` alias — always import directly as `scitex_core.<submodule>`. No CLI, no MCP tools. Drop-in replacement for an in-house monorepo "utils" package that cobbles together `logging` + `pathlib` + `subprocess` + `hashlib` + `concurrent.futures` wrappers, and for depending on each scitex-* leaf package individually when you just want one install. Use whenever the user asks to "use scitex_core utilities", "avoid depending on 10 separate scitex-* packages", "get logging + path + dict helpers from one import", understand which submodule lives where, or mentions scitex_core, SciTeX foundation layer, shared utility package.
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
tags: [scitex-core, scitex-package]
---

# scitex-core

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

Foundation layer. Every other SciTeX package imports from here. Keep
examples small — the surface is deliberately boring.

## Installation & import

`pip install scitex-core` installs the standalone:

```python
import scitex_core
```

This package does not ship as a submodule of the `scitex` umbrella.

## Sub-skills

### Core

* [01_quick-start](01_quick-start.md) — Representative imports
* [02_python-api-std](02_python-api-std.md) — `errors`, `logging`, `sh`, `path`, `str`
* [03_python-api-data](03_python-api-data.md) — `dict`, `types`, `dt`, `parallel`, `repro`

### Conventions

* [20_conventions](20_conventions.md) — Import style, logging defaults, shadowed stdlib names


## Environment

- [21_env-vars.md](21_env-vars.md) — SCITEX_* env vars read by scitex-core at runtime
