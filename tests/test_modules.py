"""Parameterized pytest tests that run each HDLbits module via cocotb."""

from __future__ import annotations

import json
import os

import pytest
from cocotb_test.simulator import run

from hdlb_test.parser import parse_ports

from .conftest import REPO_ROOT, GENERATED_DIR, _modules


def _write_test_json(
    src_stem: str,
    ports: dict,
    spec: dict,
) -> str:
    """Write test vectors to a JSON file for the cocotb test module."""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    data: dict = {"ports": ports}
    if spec.get("tests"):
        data["tests"] = spec["tests"]
    if spec.get("sequence"):
        data["sequence"] = spec["sequence"]
    if spec.get("expected"):
        data["expected"] = spec["expected"]
    path = GENERATED_DIR / f"{src_stem}_tests.json"
    with open(path, "w") as f:
        json.dump(data, f)
    return str(path)


@pytest.mark.parametrize(
    "rel_path,spec",
    _modules,
    ids=[f"{p}:{s.get('module', 'top_module')}" for p, s in _modules],
)
def test_module(rel_path: str, spec: dict, generated_dir: str) -> None:
    src_path = REPO_ROOT / rel_path
    module_name = spec.get("module", "top_module")
    clk = spec.get("clk")

    ports = parse_ports(src_path, module_name)
    if ports is None:
        pytest.fail(f"Cannot parse ports for {rel_path}")

    test_json = _write_test_json(src_path.stem, ports, spec)

    extra_env: dict[str, str] = {
        "HDLBITS_TESTS": test_json,
        "HDLBITS_CLK": clk or "",
    }
    if os.environ.get("WAVES"):
        extra_env["WAVES"] = "1"

    try:
        run(
            verilog_sources=[str(src_path)],
            toplevel=module_name,
            module="hdlb_test.cocotb_tb",
            extra_env=extra_env,
            sim_build=str(GENERATED_DIR / f"sim_{src_path.stem}"),
            timescale="1ns/1ps",
            force_compile=True,
        )
    except SystemExit as e:
        pytest.fail(str(e))
