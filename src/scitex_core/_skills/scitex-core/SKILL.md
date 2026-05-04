---
name: scitex-core
description: |
  [WHAT] Foundation layer bundling 10 standalone utility modules — `logging`, `errors`, `sh`, `path`, `str`, `dict`, `types`, `dt`, `parallel`, `repro` — imported by every other SciTeX package.
  [WHEN] Wanting one install for logging + path + dict + sh + repro helpers instead of depending on 10 separate scitex-* leaves, or looking up which submodule lives where.
  [HOW] `import scitex_core` then `scitex_core.<submodule>` — no `scitex.core` umbrella alias.
tags: [scitex-core]
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  http: 0
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

* [01_installation](01_installation.md) — pip install + smoke verify
* [02_quick-start](02_quick-start.md) — representative one-liners per submodule
* [03_python-api](03_python-api.md) — the 10 bundled submodules + per-submodule skill links

### Conventions

* [20_conventions](20_conventions.md) — Import style, logging defaults, shadowed stdlib names

## Environment

- [21_env-vars.md](21_env-vars.md) — SCITEX_* env vars read by scitex-core at runtime

## Legacy / detail (kept for context)

- [10_quick-start](10_quick-start.md) — original quick-start
- [11_python-api-std](11_python-api-std.md) — `errors`, `logging`, `sh`, `path`, `str` legacy listing
- [12_python-api-data](12_python-api-data.md) — `dict`, `types`, `dt`, `parallel`, `repro` legacy listing
