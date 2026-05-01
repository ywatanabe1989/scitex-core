# scitex-core

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-core.svg)](https://pypi.org/project/scitex-core/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-core.svg)](https://pypi.org/project/scitex-core/)
[![Tests](https://github.com/ywatanabe1989/scitex-core/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-core/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-core/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-core/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-core/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-core)
[![Docs](https://readthedocs.org/projects/scitex-core/badge/?version=latest)](https://scitex-core.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Bundled foundation utilities (logging, errors, sh, path, str, dict, types, dt, parallel, repro) for the SciTeX ecosystem.</b></p>

<p align="center">
  <a href="https://scitex-core.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-core</code>
</p>

---

## Problem and Solution

| # | Problem | Solution |
|---|---------|----------|
| 1 | **10 separate scitex-* utility packages for dev tooling** — `pip install scitex-str`, `scitex-dict`, `scitex-path`, ... gets tedious | **Bundled foundation** — `import scitex_core` exposes `logging`, `errors`, `sh`, `path`, `str`, `dict`, `types`, `dt`, `parallel`, `repro` in one install |

## Installation

```bash
pip install scitex-core
```

## Quick Start

```python
from scitex_core import logging, path, repro

logger = logging.getLogger(__name__)
logger.info("Hello from scitex-core!")

git_root = path.find_git_root()
exp_id   = repro.gen_id()
```

## 1 Interfaces

<details>
<summary><strong>Python API</strong></summary>

<br>

```python
# Logging
from scitex_core import logging
logger = logging.getLogger(__name__)
logger.info("Hello"); logger.success("Done")

# Path
from scitex_core import path
path.find_file("/home/user/project", "*.py")
path.this_path()
path.find_git_root()

# Reproducibility
from scitex_core.repro import RandomStateManager, gen_id
rng = RandomStateManager(seed=42)
data = rng("data").random(100)
rng.verify(data, "my_data")

# Types
from scitex_core.types import ArrayLike, is_array_like, is_list_of_type
is_list_of_type([1, 2, 3], int)

# Datetime
from scitex_core.dt import linspace
import datetime
linspace(datetime.datetime(2026, 1, 1), datetime.datetime(2026, 1, 2),
         n_samples=24)

# Parallel
from scitex_core.parallel import run
run(my_func, [(arg1,), (arg2,)], n_jobs=4)

# Dict
from scitex_core.dict import DotDict
d = DotDict({"a": {"b": 1}})
d.a.b  # 1
```

</details>

## Status

Foundation package — used by `scitex-writer`, `scitex-scholar`,
`scitex-io`, and the umbrella `scitex` distribution.

## Part of SciTeX

`scitex-core` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[core]` to use as
`scitex.core` (Python).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
