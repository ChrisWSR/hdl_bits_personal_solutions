"""Verilog port-list parser."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _parse_width(width_spec: str | None) -> int:
    """Return bit width from a Verilog range string like '[7:0]'."""
    if not width_spec:
        return 1
    try:
        parts = width_spec.split(":")
        lo = int(parts[1].strip())
        hi = int(parts[0].strip())
        return abs(hi - lo) + 1
    except (ValueError, IndexError):
        return 1


def _parse_one_decl(text: str, cur_dir: str) -> tuple[str, str, int, str, bool] | None:
    """Try to parse a single port declaration from text.

    Returns (name, direction, width, rest, has_width) or None.
    ``has_width`` is True when an explicit width range was found.
    """
    pat = re.compile(
        r"^\s*"
        r"(?:(wire|reg|logic|tri)\s+)?"
        r"(?:signed\s+)?"
        r"(?:\[([^\]]+)\]\s+)?"
        r"(\w+)"
        r"(.*)"
    )
    m = pat.match(text)
    if not m:
        return None
    width_spec = m.group(2)
    width = _parse_width(width_spec)
    name = m.group(3)
    rest = m.group(4)
    return name, cur_dir, width, rest.strip(), width_spec is not None


def _parse_ports_block(port_block: str) -> dict[str, dict[str, Any]]:
    """Parse a cleaned port-list string into a port dict.

    Handles multiple direction keywords on a single line:
      input a, b, output c
    as well as multi-line declarations.
    """
    ports: dict[str, dict[str, Any]] = {}
    cur_dir = "input"
    cur_width = 1

    text = port_block.strip()
    while text:
        text = text.strip()

        dm = re.match(r"^(input|output|inout)\b", text)
        if dm:
            cur_dir = dm.group(1)
            text = text[dm.end():].strip()
            continue

        if text.startswith(","):
            text = text[1:].strip()
            continue

        result = _parse_one_decl(text, cur_dir)
        if result is None:
            text = text[1:].strip()
            continue

        name, direction, width, rest, has_width = result
        if has_width:
            cur_width = width
        if name and name not in (
            "input", "output", "inout", "wire", "reg", "logic", "tri",
        ):
            ports[name] = {"dir": direction, "width": cur_width}
        text = rest

    return ports


def parse_ports(source_path: str | Path, module_name: str = "top_module") -> dict[str, dict[str, Any]] | None:
    """Parse a Verilog file and return port info for *module_name*.

    Returns a dict:
        {name: {"dir": "input"|"output", "width": int}, ...}

    Returns None if the module is not found.
    """
    text = Path(source_path).read_text(errors="replace")

    pat = re.compile(
        r"\bmodule\s+" + re.escape(module_name) + r"\s*\((.*?)\)\s*[;]",
        re.DOTALL,
    )
    m = pat.search(text)
    if not m:
        return None

    port_block = m.group(1)

    port_block = re.sub(r"//.*", "", port_block)
    port_block = re.sub(r"/\*.*?\*/", "", port_block, flags=re.DOTALL)
    port_block = re.sub(r"\s+", " ", port_block)

    ports = _parse_ports_block(port_block)
    return ports if ports else None
