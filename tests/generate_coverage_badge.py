#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/generate_coverage_badge.py

"""
Generate coverage badge for README.md

Usage:
    python3 tests/generate_coverage_badge.py

This script:
1. Runs pytest with coverage
2. Parses the coverage percentage
3. Updates README.md with the badge

Requires: pytest, pytest-cov
"""

import subprocess
import re
import sys
import os


def get_badge_color(coverage):
    """Get badge color based on coverage percentage."""
    if coverage >= 90:
        return "brightgreen"
    elif coverage >= 75:
        return "green"
    elif coverage >= 60:
        return "yellowgreen"
    elif coverage >= 40:
        return "yellow"
    elif coverage >= 20:
        return "orange"
    else:
        return "red"


def run_coverage():
    """Run pytest with coverage and return coverage percentage."""
    print("Running tests with coverage...")

    try:
        result = subprocess.run(
            ["pytest", "--cov=src/scitex_core", "--cov-report=term-missing", "tests/"],
            capture_output=True,
            text=True,
            check=False
        )

        # Parse coverage from output
        output = result.stdout + result.stderr

        # Look for pattern like "TOTAL    1234    567    54%"
        match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)

        if match:
            coverage = int(match.group(1))
            print(f"Coverage: {coverage}%")
            return coverage
        else:
            print("Could not parse coverage from output")
            print("Output:", output[-500:])  # Print last 500 chars
            return None

    except FileNotFoundError:
        print("Error: pytest not found. Install with: pip install pytest pytest-cov")
        return None
    except Exception as e:
        print(f"Error running coverage: {e}")
        return None


def generate_badge_url(coverage):
    """Generate shields.io badge URL."""
    color = get_badge_color(coverage)
    return f"https://img.shields.io/badge/coverage-{coverage}%25-{color}.svg"


def update_readme(coverage):
    """Update README.md with coverage badge."""
    readme_path = "README.md"

    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found")
        return False

    with open(readme_path, 'r') as f:
        content = f.read()

    badge_url = generate_badge_url(coverage)
    badge_markdown = f"[![Coverage]({badge_url})](tests/)"

    # Replace existing coverage badge or add new one
    if "[![Coverage]" in content:
        # Replace existing badge
        content = re.sub(
            r'\[!\[Coverage\]\([^\)]+\)\]\([^\)]+\)',
            badge_markdown,
            content
        )
        print("Updated existing coverage badge")
    else:
        # Add badge after other badges
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('[!['):
                # Add after last badge line
                if i + 1 < len(lines) and not lines[i + 1].startswith('[!['):
                    lines.insert(i + 1, badge_markdown)
                    break
        content = '\n'.join(lines)
        print("Added new coverage badge")

    with open(readme_path, 'w') as f:
        f.write(content)

    print(f"README.md updated with coverage: {coverage}%")
    return True


def main():
    """Main function."""
    print("=" * 60)
    print("Coverage Badge Generator for scitex-core")
    print("=" * 60)
    print()

    # Run coverage
    coverage = run_coverage()

    if coverage is None:
        print("\nFailed to calculate coverage.")
        print("\nNote: This may be due to dependency issues.")
        print("See tests/TEST_IMPLEMENTATION_STATUS.md for details.")
        sys.exit(1)

    # Update README
    if update_readme(coverage):
        print("\n✓ Success! README.md updated with coverage badge.")
        print(f"\nCoverage: {coverage}% ({get_badge_color(coverage)})")
    else:
        print("\n✗ Failed to update README.md")
        sys.exit(1)


if __name__ == "__main__":
    main()

# EOF
