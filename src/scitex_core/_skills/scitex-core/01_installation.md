---
description: |
  [TOPIC] scitex-core Installation
  [DETAILS] pip install scitex-core (single install for the 10 standalone foundation modules); smoke verify by importing one of the bundled submodules.
tags: [scitex-core-installation]
---

# Installation

## Standard

```bash
pip install scitex-core
```

Bundles 10 standalone utility modules: `logging`, `errors`, `sh`,
`path`, `str`, `dict`, `types`, `dt`, `parallel`, `repro`. One install
gives you the full foundation layer used by every other SciTeX package.

## Verify

```bash
python -c "import scitex_core; print(scitex_core.__version__)"
python -c "from scitex_core import logging, path, dict, sh, str as s, types, repro; print('ok')"
```

## Editable install (development)

```bash
git clone https://github.com/ywatanabe1989/scitex-core
cd scitex-core
pip install -e '.[dev]'
```

## Note: no `scitex.core` umbrella alias

Unlike most leaf packages, this one does **not** ship as a submodule of
the `scitex` umbrella. Always import as `scitex_core`:

```python
import scitex_core
from scitex_core import logging, path
```

The individual sub-modules (`scitex_logging`, `scitex_path`, ...) are
also published as separate packages — depend on those instead if you
need just one.
