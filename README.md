# scitex-core

Core infrastructure for the SciTeX ecosystem.

## Overview

`scitex-core` provides shared utilities used across all SciTeX packages:

- **logging**: Enhanced logging with colored output and file support
- **errors**: Common error classes with rich context
- **sh**: Safe shell command execution
- **types**: Shared type definitions

## Installation

```bash
pip install scitex-core
```

## Usage

```python
from scitex_core import logging

logger = logging.getLogger(__name__)
logger.info("Hello from scitex-core!")
logger.success("Operation completed")
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
pytest
```

## License

MIT License - see LICENSE file for details.
