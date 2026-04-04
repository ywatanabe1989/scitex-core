# Coverage Report for scitex-core

## How to Generate Coverage

### Method 1: Using pytest directly

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=src/scitex_core --cov-report=html --cov-report=term-missing tests/

# Open HTML report
open htmlcov/index.html
```

### Method 2: Using test runner script

```bash
./tests/run_tests.sh -c -h
```

### Method 3: Generate coverage badge

```bash
python3 tests/generate_coverage_badge.py
```

This will:
1. Run pytest with coverage
2. Calculate coverage percentage
3. Update README.md with badge

## Expected Coverage

Based on the test implementation, we should achieve:

### Module Coverage Goals

| Module | Files | Test Files | Expected Coverage |
|--------|-------|------------|-------------------|
| `errors.py` | 1 | 1 | 95%+ |
| `sh/` | 4 | 3 | 90%+ |
| `logging/` | 9 | 4 | 85%+ |

### Overall Coverage Goal: **90%+**

## Current Test Statistics

- **Total test methods**: 161+
- **Test classes**: 30+
- **Test files**: 14
- **Lines of test code**: 2,500+

## Coverage Breakdown

### errors.py
- ✓ All error classes (15+)
- ✓ All warning functions (3)
- ✓ All validation helpers (3)
- ✓ Error hierarchy
- ✓ Context and suggestions

### sh module
- ✓ Security validation (validate_command, quote)
- ✓ Type definitions (ShellResult, CommandInput, ReturnFormat)
- ✓ Main functions (sh, sh_run)
- ✓ Timeout handling
- ✓ Streaming output
- ⚠ Execute functions (requires fixing scitex dependency)

### logging module
- ✓ Custom levels (SUCCESS, FAIL)
- ✓ Logger class (SciTeXLogger)
- ✓ Configuration functions
- ✓ Tee functionality
- ⚠ Full integration (requires fixing scitex dependency)

## Known Issues Affecting Coverage

### 1. External Dependencies

The following files have `scitex` package dependencies that prevent full test execution:

- `src/scitex_core/sh/_execute.py` - Uses `scitex.str.color_text()`

**Impact**: ~10% of code cannot be fully tested until dependency is removed.

**Fix**: Replace with standalone color implementation or remove coloring.

### 2. Import Issues

Some tests use skip markers when imports fail:

```python
@pytest.mark.skipif(not MODULE_AVAILABLE, reason="Dependencies not available")
```

This ensures tests pass in CI but skips actual testing of those modules.

## How to Achieve 90%+ Coverage

### Step 1: Fix Dependencies

```bash
# Replace scitex.str.color_text() in _execute.py with:
# Option 1: Standalone ANSI color codes
# Option 2: colorama (add to dependencies)
# Option 3: Remove colors (simplest)
```

### Step 2: Run Full Test Suite

```bash
pip install -e ".[dev]"
pytest --cov=src/scitex_core --cov-report=html tests/
```

### Step 3: Identify Gaps

```bash
# Check coverage report
open htmlcov/index.html

# Find uncovered lines
pytest --cov=src/scitex_core --cov-report=term-missing tests/
```

### Step 4: Add Missing Tests

Focus on:
- Error paths and exception handling
- Edge cases in sh streaming
- Logging handler integration
- File I/O operations

## CI/CD Integration

### GitHub Actions (Recommended)

Copy `.github/workflows/tests.yml.template` to `.github/workflows/tests.yml` to enable:

- ✓ Automatic testing on push/PR
- ✓ Multi-Python version testing (3.8-3.12)
- ✓ Coverage calculation
- ✓ Codecov integration
- ✓ Automatic badge updates

### Codecov Integration

1. Sign up at https://codecov.io
2. Add repository
3. Badge will be available at:
   ```markdown
   [![codecov](https://codecov.io/gh/USERNAME/scitex-core/branch/master/graph/badge.svg)](https://codecov.io/gh/USERNAME/scitex-core)
   ```

## Coverage Best Practices

1. **Test first** - Write tests for new features
2. **Test edge cases** - Include error conditions
3. **Test integrations** - Module interactions
4. **Regular checks** - Run coverage locally before commits
5. **Monitor trends** - Track coverage over time

## Manual Coverage Check

```bash
# Run coverage
pytest --cov=src/scitex_core tests/

# View report
coverage report

# Detailed report
coverage report -m

# HTML report
coverage html
open htmlcov/index.html
```

## Target Coverage by Release

- **v1.0.0**: 85%+ (current state after dependency fix)
- **v1.1.0**: 90%+ (add integration tests)
- **v2.0.0**: 95%+ (comprehensive edge case coverage)

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure coverage doesn't decrease
3. Run `pytest --cov` before committing
4. Add tests for all public APIs
5. Include docstring examples

---

Last updated: 2025-11-10
Target coverage: 90%+
Current blockers: scitex dependency in _execute.py

# EOF
