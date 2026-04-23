# scitex-core

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-200%2B%20tests-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](CHANGELOG.md)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

Core infrastructure for the SciTeX ecosystem.

## Problem and Solution


| # | Problem | Solution |
|---|---------|----------|
| 1 | **10 separate scitex-* utility packages for dev tooling** -- `pip install scitex-str`, `scitex-dict`, `scitex-path`, ... gets tedious | **Bundled foundation** -- `import scitex_core` exposes `logging`, `errors`, `sh`, `path`, `str`, `dict`, `types`, `dt`, `parallel`, `repro` in one install |

## Overview

`scitex-core` provides shared utilities used across all SciTeX packages:

- **logging**: Enhanced logging with colored output and file support
- **errors**: Common error classes with rich context
- **sh**: Safe shell command execution
- **str**: String utilities including ANSI color formatting
- **path**: File path and directory utilities
- **repro**: Reproducibility utilities (ID generation, random state management)
- **types**: Shared type definitions and validators

## Installation

```bash
pip install scitex-core
```

## Usage

### Logging

```python
from scitex_core import logging

logger = logging.getLogger(__name__)
logger.info("Hello from scitex-core!")
logger.success("Operation completed")
```

### Path Utilities

```python
from scitex_core import path

# Find files
py_files = path.find_file("/home/user/project", "*.py")

# Get current script path
script_path = path.this_path()

# Find git repository root
git_root = path.find_git_root()

# Clean and normalize paths
cleaned = path.clean("path/with/../spaces ")
```

### Reproducibility

```python
from scitex_core.repro import RandomStateManager, gen_id

# Random state management
rng_manager = RandomStateManager(seed=42)
data_gen = rng_manager("data")
data = data_gen.random(100)

# Verify reproducibility
rng_manager.verify(data, "my_data")

# Generate unique IDs
exp_id = gen_id()  # "2025Y-11M-10D-12h30m45s_aB3xY9z2"
```

### Type Definitions

```python
from scitex_core.types import ArrayLike, is_array_like, is_list_of_type

def process_data(data: ArrayLike) -> None:
    if is_array_like(data):
        print("Valid array-like data")

numbers = [1, 2, 3, 4]
if is_list_of_type(numbers, int):
    print("All elements are integers")
```

## Packages Using scitex-core

- `scitex-writer` - Academic writing and LaTeX compilation
- `scitex-scholar` - Research paper management
- `scitex-io` - Scientific data I/O
- `scitex` - Main package

## Development

```bash
# Clone repository
git clone https://github.com/ywatanabe1989/scitex-core

# Install in editable mode
cd scitex-core
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest --cov=src/scitex_core --cov-report=html tests/

# Quick test (no dependencies)
python3 tests/simple_runner.py
```

## Testing

The project has comprehensive test coverage:

- **161+ test methods** across 30+ test classes
- **3 test modules**: errors, sh, logging
- **Multiple test runners**: pytest, simple_runner.py, run_tests.sh

See [tests/README.md](tests/README.md) for detailed testing documentation.

### Quick Test

```bash
# No installation required
python3 tests/simple_runner.py
```

### Full Test Suite

```bash
# Install dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Generate coverage report
./tests/run_tests.sh -c -h
open htmlcov/index.html
```

## License

MIT License - see LICENSE file for details.
