"""Cocotb test module loaded by the simulator for each module under test.

Reads test vectors from a JSON file (path in ``HDLBITS_TESTS`` env var)
and applies them to the DUT. Supports both combinational and sequential
(clocked) modules.
"""

from __future__ import annotations

import json
import os
from typing import Any

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def _sig(dut: cocotb.handle.ModifiableObject, name: str) -> Any:  # noqa: ANN401
    """Access a DUT signal by name, safely handling Python keywords like ``in``."""
    return getattr(dut, name)


@cocotb.test()
async def run_tests(dut: cocotb.handle.ModifiableObject) -> None:
    json_path = os.environ.get("HDLBITS_TESTS")
    clk_name = os.environ.get("HDLBITS_CLK") or None

    if os.environ.get("WAVES"):
        cocotb.simulator.dump_on("dump.vcd")
        dut._log.info("Waveform dump enabled: dump.vcd")

    if not json_path:
        raise RuntimeError("HDLBITS_TESTS env var is not set")

    with open(json_path) as f:
        data: dict[str, Any] = json.load(f)

    ports: dict[str, dict[str, Any]] = data["ports"]
    tests: list[dict[str, int]] = data.get("tests", [])
    sequence: list[dict[str, int]] | None = data.get("sequence")
    expected: dict[str, list[int]] | None = data.get("expected")

    inputs = {n: p for n, p in ports.items() if p["dir"] == "input"}
    outputs = {n: p for n, p in ports.items() if p["dir"] == "output"}
    has_clk = clk_name is not None

    if has_clk:
        cocotb.start_soon(Clock(_sig(dut, clk_name), 10, unit="ns").start())

    # ── Sequential mode (multi-cycle sequences) ──────────────────────
    if sequence is not None:
        check_after_cycle = bool(expected)
        for i, step in enumerate(sequence):
            for name in inputs:
                if has_clk and name == clk_name:
                    continue
                _sig(dut, name).value = step.get(name, 0)

            if has_clk:
                await RisingEdge(_sig(dut, clk_name))

            await Timer(1, unit="ns")

            if check_after_cycle:
                for out_name, expected_values in expected.items():
                    if i < len(expected_values):
                        expected_val = expected_values[i]
                        actual = int(_sig(dut, out_name).value)
                        assert actual == expected_val, (
                            f"{out_name}[cycle {i}]={actual} (expected {expected_val})"
                        )
        return

    # ── Combinational / flat-vector mode ─────────────────────────────
    for test in tests:
        for name in inputs:
            if has_clk and name == clk_name:
                continue
            _sig(dut, name).value = test.get(name, 0)

        if has_clk:
            await RisingEdge(_sig(dut, clk_name))

        await Timer(1, unit="ns")

        for name in outputs:
            if name in test:
                expected_val = test[name]
                actual = int(_sig(dut, name).value)
                assert actual == expected_val, f"{name}={actual} (expected {expected_val})"
