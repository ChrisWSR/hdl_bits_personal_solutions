#!/usr/bin/env python3
"""HDLbits test runner — entry point.

Usage:
    python3 run_tests.py                        # run all tests (via pytest)
    python3 run_tests.py -k and_gate            # run matching tests
    python3 run_tests.py --init                 # generate tests.yaml files
    python3 run_tests.py --dry-run              # preview (legacy)
    python3 run_tests.py --verbose              # detailed output (legacy)
"""

import sys

if "--init" in sys.argv:
    from hdlb_test.cli import cmd_init
    cmd_init()
    sys.exit(0)

if "--dry-run" in sys.argv or "--verbose" in sys.argv:
    print(
        "Use 'pytest tests/ --collect-only -q' to list tests. "
        "Legacy --dry-run/--verbose flags are replaced by pytest's -v/--tb=long."
    )
    sys.exit(0)

import pytest

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    sys.exit(pytest.main(args))
