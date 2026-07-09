#!/usr/bin/env python3
"""HDLbits test runner — entry point.

Usage:
    python3 run_tests.py                        # run all tests (via pytest)
    python3 run_tests.py -k and_gate            # run matching tests
    python3 run_tests.py --init                 # generate tests.yaml files
"""

import sys
from pathlib import Path

if "--init" in sys.argv:
    from hdlb_test.loader import init_specs
    REPO_ROOT = Path(__file__).resolve().parent
    created = init_specs(REPO_ROOT)
    print(f"Wrote {len(created)} tests.yaml files.")
    for p in created:
        print(f"  {p.relative_to(REPO_ROOT)}")
    sys.exit(0)

import pytest

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    sys.exit(pytest.main(args))
