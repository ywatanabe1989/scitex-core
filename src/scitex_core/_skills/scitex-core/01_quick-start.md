---
name: quick-start
description: Quick Start — see file body for details.
tags: [scitex-core, scitex-package]
---

# Quick Start

`scitex-core` exports ten sub-modules. Import what you need:

```python
from scitex_core import logging, errors, sh, path, repro, dict as sdict, dt, parallel, types
from scitex_core import str as sstr  # shadows builtin; alias to taste
```

## Logging

```python
from scitex_core import logging
logger = logging.getLogger(__name__)
logger.success("parsed 1200 rows")
logger.fail("db unreachable")
```

## Safe shell execution

```python
from scitex_core.sh import sh
out = sh(["git", "rev-parse", "HEAD"], return_as="str")
```

List-form only (shell-injection-safe). `return_as="dict"` gives a
`ShellResult` with `stdout`, `stderr`, `returncode`.

## Reproducibility ID + timestamp

```python
from scitex_core.repro import gen_id, gen_timestamp
run_id = gen_id()
ts = gen_timestamp()
```

## DotDict

```python
from scitex_core.dict import DotDict
cfg = DotDict({"lr": 1e-3, "opt": {"name": "adam"}})
cfg.opt.name  # "adam"
```

## Parallel runner

```python
from scitex_core.parallel import run
results = run(func, iterable, n_jobs=4)
```

Full symbol lists: [02_python-api-std.md](02_python-api-std.md),
[03_python-api-data.md](03_python-api-data.md).
