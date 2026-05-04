---
description: |
  [TOPIC] scitex-core Python API
  [DETAILS] The 10 bundled submodules — logging, errors, sh, path, str, dict, types, dt, parallel, repro — and how to reach each.
tags: [scitex-core-python-api]
---

# Python API

`scitex-core` re-exports 10 standalone foundation submodules under a
single namespace:

```python
import scitex_core

scitex_core.logging      # enhanced logging + warnings + SciTeXError hierarchy
scitex_core.errors       # exception hierarchy (alias of logging.errors)
scitex_core.sh           # safe subprocess wrapper (list-only)
scitex_core.path         # find_file / find_git_root / get_spath / symlink helpers
scitex_core.str          # printc / color_text / latex / format_axis_label / grep
scitex_core.dict         # DotDict, safe_merge, flatten, ...
scitex_core.types        # ArrayLike, ColorLike, is_array_like, ...
scitex_core.dt           # datetime helpers
scitex_core.parallel     # parallel-execution helpers
scitex_core.repro        # gen_id, fix_seeds, reproducibility helpers
```

## Recommended import style

For one or two helpers, import the submodule:

```python
from scitex_core import logging, path
log = logging.getLogger(__name__)
```

For deep usage of one submodule, prefer its dedicated standalone:

```python
import scitex_logging         # same module, smaller dep footprint
import scitex_path
```

## Per-submodule API

Each bundled submodule is itself published standalone with its own
`_skills/` documentation:

| Submodule | Standalone package | Skill |
|---|---|---|
| `logging`  | `scitex-logging`     | `_skills/scitex-logging/` |
| `path`     | `scitex-path`        | `_skills/scitex-path/`    |
| `str`      | `scitex-str`         | `_skills/scitex-str/`     |
| `dict`     | `scitex-dict`        | `_skills/scitex-dict/`    |
| `types`    | `scitex-types`       | `_skills/scitex-types/`   |
| `sh`       | `scitex-sh`          | `_skills/scitex-sh/`      |
| `dt`       | `scitex-dt`          | `_skills/scitex-dt/`      |
| `parallel` | `scitex-parallel`    | `_skills/scitex-parallel/`|
| `repro`    | `scitex-repro`       | `_skills/scitex-repro/`   |
| `errors`   | (in scitex-logging)  | `_skills/scitex-logging/` |

Refer to those skills for the full per-submodule public API. The
legacy condensed listings live at:

- [11_python-api-std.md](11_python-api-std.md) — std-grouped summary
- [12_python-api-data.md](12_python-api-data.md) — data-grouped summary

## No `scitex.core` umbrella

`scitex-core` is not exposed as `scitex.core`. Always
`import scitex_core` directly.
