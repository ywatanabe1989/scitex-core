#!/bin/bash
# -*- coding: utf-8 -*-
# File: ./tests/run_tests.sh
#
# Test runner for scitex-core
# Usage: ./tests/run_tests.sh [options]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
COVERAGE=false
VERBOSE=false
SPECIFIC_TEST=""
HTML_REPORT=false
MARKERS=""

# Print usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -c, --coverage      Run with coverage report"
    echo "  -v, --verbose       Run in verbose mode"
    echo "  -h, --html          Generate HTML coverage report"
    echo "  -t, --test FILE     Run specific test file"
    echo "  -m, --marker MARK   Run tests with specific marker"
    echo "  --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                  # Run all tests"
    echo "  $0 -c               # Run with coverage"
    echo "  $0 -c -h            # Run with coverage and HTML report"
    echo "  $0 -t test_errors   # Run specific test file"
    echo "  $0 -v               # Run in verbose mode"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--html)
            HTML_REPORT=true
            COVERAGE=true  # HTML report requires coverage
            shift
            ;;
        -t|--test)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        -m|--marker)
            MARKERS="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Print header
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  SciTeX-Core Test Suite${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Install with: pip install pytest pytest-cov"
    exit 1
fi

# Build pytest command
PYTEST_CMD="pytest"

# Add verbose flag
if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add coverage options
if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=src/scitex_core --cov-report=term-missing"

    if [ "$HTML_REPORT" = true ]; then
        PYTEST_CMD="$PYTEST_CMD --cov-report=html"
    fi
fi

# Add marker filter
if [ -n "$MARKERS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m $MARKERS"
fi

# Add specific test file
if [ -n "$SPECIFIC_TEST" ]; then
    PYTEST_CMD="$PYTEST_CMD tests/$SPECIFIC_TEST"
else
    PYTEST_CMD="$PYTEST_CMD tests/"
fi

# Print configuration
echo -e "${YELLOW}Configuration:${NC}"
echo "  Coverage: $COVERAGE"
echo "  Verbose: $VERBOSE"
echo "  HTML Report: $HTML_REPORT"
if [ -n "$SPECIFIC_TEST" ]; then
    echo "  Test File: $SPECIFIC_TEST"
fi
if [ -n "$MARKERS" ]; then
    echo "  Markers: $MARKERS"
fi
echo ""

# Run tests
echo -e "${BLUE}Running tests...${NC}"
echo "Command: $PYTEST_CMD"
echo ""

if $PYTEST_CMD; then
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✓ All tests passed!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [ "$HTML_REPORT" = true ]; then
        echo ""
        echo -e "${BLUE}HTML coverage report generated: htmlcov/index.html${NC}"
    fi

    exit 0
else
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ✗ Tests failed!${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi

# EOF
