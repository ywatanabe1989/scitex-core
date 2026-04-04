# Quick Start Guide - Testing scitex-core

## Option 1: Quick Test (No Installation)

Run the basic test suite without installing any dependencies:

```bash
python3 tests/simple_runner.py
```

This will test:
- Module imports
- Basic functionality
- Type definitions
- Validation helpers

## Option 2: Full Test Suite

### Step 1: Install Dependencies

```bash
# Install scitex-core with dev dependencies
pip install -e '.[dev]'
```

This installs:
- pytest>=7.0
- pytest-cov
- black>=22.0
- mypy>=0.950

### Step 2: Run Tests

```bash
# Simple run
pytest tests/

# Verbose output
pytest tests/ -v

# With coverage
pytest --cov=src/scitex_core tests/

# HTML coverage report
pytest --cov=src/scitex_core --cov-report=html tests/
```

### Step 3: Use Test Runner Script

```bash
# Make executable (if not already)
chmod +x tests/run_tests.sh

# Run all tests
./tests/run_tests.sh

# Run with coverage
./tests/run_tests.sh -c

# Run with coverage and HTML report
./tests/run_tests.sh -c -h

# Run specific test file
./tests/run_tests.sh -t test_errors.py

# Run in verbose mode
./tests/run_tests.sh -v
```

## Running Specific Tests

```bash
# Test a specific module
pytest tests/test_errors.py
pytest tests/scitex_core/sh/
pytest tests/scitex_core/logging/

# Test a specific class
pytest tests/test_errors.py::TestSciTeXError

# Test a specific method
pytest tests/test_errors.py::TestSciTeXError::test_basic_error

# Run tests matching a pattern
pytest tests/ -k "error"
pytest tests/ -k "security"
```

## Viewing Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src/scitex_core --cov-report=html tests/

# Open in browser
xdg-open htmlcov/index.html  # Linux
open htmlcov/index.html      # macOS
```

## Known Issues

### Missing Dependencies Error

If you see errors about missing `scitex` module, this is expected. The scitex-core
source files have dependencies on the full `scitex` package that need to be removed:

**Files to fix:**
- `src/scitex_core/sh/_execute.py` - Remove `scitex.str.color_text()` calls
- Replace with standalone implementation or plain output

### No pytest Found

```bash
# Check if pytest is installed
python3 -m pytest --version

# If not found, install it
pip install pytest pytest-cov

# Or install all dev dependencies
pip install -e '.[dev]'
```

## Test Organization

```
tests/
├── test_errors.py              # Error classes and helpers
├── scitex_core/
│   ├── sh/                     # Shell command execution
│   │   ├── test__security.py   # Security validation
│   │   ├── test__types.py      # Type definitions
│   │   └── test__init__.py     # Main sh functions
│   └── logging/                # Logging functionality
│       ├── test_levels.py      # Custom log levels
│       ├── test_logger.py      # Logger classes
│       ├── test_config.py      # Configuration
│       └── test_tee.py         # Tee functionality
```

## Continuous Integration

For CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Install dependencies
  run: pip install -e '.[dev]'

- name: Run tests with coverage
  run: pytest --cov=src/scitex_core --cov-report=xml tests/

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Tips

1. **Run tests before committing:**
   ```bash
   pytest tests/ -v
   ```

2. **Check coverage:**
   ```bash
   pytest --cov=src/scitex_core --cov-report=term-missing tests/
   ```

3. **Run specific test suites:**
   ```bash
   # Only errors
   pytest tests/test_errors.py -v

   # Only sh module
   pytest tests/scitex_core/sh/ -v

   # Only logging
   pytest tests/scitex_core/logging/ -v
   ```

4. **Debug failing tests:**
   ```bash
   # Stop on first failure
   pytest tests/ -x

   # Print output
   pytest tests/ -s

   # Full traceback
   pytest tests/ --tb=long
   ```

## Getting Help

- See `tests/README.md` for detailed testing guide
- See `TEST_IMPLEMENTATION_STATUS.md` for test coverage details
- Run `./tests/run_tests.sh --help` for runner options

# EOF
