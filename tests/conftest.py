"""Shared fixtures and module discovery for cocotb-based HDLbits tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = REPO_ROOT / "_generated"


def discover_modules() -> list[tuple[str, dict[str, Any]]]:
    """Yield ``(rel_path, spec)`` tuples for every module with test vectors."""
    from hdlb_test.loader import load_all_specs

    specs = load_all_specs(REPO_ROOT)
    result: list[tuple[str, dict[str, Any]]] = []
    for rel_path, spec in sorted(specs.items()):
        has_tests = bool(spec.get("tests"))
        has_sequence = bool(spec.get("sequence"))
        if has_tests or has_sequence:
            result.append((rel_path, spec))
    return result


_modules = list(discover_modules())


@pytest.fixture(scope="module")
def generated_dir() -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return GENERATED_DIR


def get_module_ids() -> list[str]:
    return [f"{rel_path}:{spec.get('module', 'top_module')}" for rel_path, spec in _modules]
