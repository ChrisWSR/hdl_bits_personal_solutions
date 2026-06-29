"""Load and initialize per-directory tests.yaml files."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, field_validator

from .parser import parse_ports


class PortSpec(BaseModel):
    inputs: list[str]
    outputs: list[str]


class ModuleSpec(BaseModel):
    module: str = "top_module"
    ports: PortSpec | None = None
    clk: str | None = None
    tests: list[dict[str, int]] | None = None
    sequence: list[dict[str, int]] | None = None
    expected: dict[str, list[int]] | None = None

    @field_validator("tests")
    @classmethod
    def tests_not_empty(cls, v: list[dict[str, int]] | None) -> list[dict[str, int]] | None:
        if v is not None and not v:
            raise ValueError("tests list cannot be empty")
        return v

    @field_validator("sequence")
    @classmethod
    def sequence_not_empty(cls, v: list[dict[str, int]] | None) -> list[dict[str, int]] | None:
        if v is not None and not v:
            raise ValueError("sequence list cannot be empty")
        return v


def load_all_specs(root_dir: str | Path) -> dict[str, dict[str, Any]]:
    """Scan *root_dir* for ``tests.yaml`` files and load test specs.

    Returns a dict mapping relative ``.v`` file paths to their spec dicts::

        {"basics/03_and_gate.v": {"module": "and_gate", "tests": [...]}}

    Validates each spec against :class:`ModuleSpec` on load. Raises
    ``pydantic.ValidationError`` on invalid YAML.
    """
    specs: dict[str, dict[str, Any]] = {}
    for tests_yaml in sorted(Path(root_dir).rglob("tests.yaml")):
        dir_path = tests_yaml.parent
        with open(tests_yaml) as f:
            data = yaml.safe_load(f)
        if not data:
            continue
        for filename, spec in data.items():
            v_path = dir_path / filename
            if v_path.exists():
                rel = str(v_path.relative_to(root_dir))
                validated = ModuleSpec.model_validate(spec)
                specs[rel] = validated.model_dump(exclude_defaults=True)
    return specs


def init_specs(root_dir: str | Path) -> list[Path]:
    """Scan all ``.v`` files and create one ``tests.yaml`` per directory.

    Returns a list of created YAML file paths.
    """
    root = Path(root_dir)

    dir_files: dict[Path, list[Path]] = {}
    for vf in sorted(root.rglob("*.v")):
        dir_files.setdefault(vf.parent, []).append(vf)

    created: list[Path] = []
    for dir_path, vfiles in dir_files.items():
        entries: dict[str, Any] = {}
        for vf in vfiles:
            ports = parse_ports(vf, "top_module")
            module_name = "top_module"
            if ports is None:
                text = vf.read_text(errors="replace")
                m = re.search(r"\bmodule\s+(\w+)", text)
                if m:
                    module_name = m.group(1)
                    ports = parse_ports(vf, module_name)

            entry: dict[str, Any] = {}
            if module_name != "top_module":
                entry["module"] = module_name

            if ports:
                inputs = sorted(
                    [n for n, p in ports.items() if p["dir"] == "input"]
                )
                outputs = sorted(
                    [n for n, p in ports.items() if p["dir"] == "output"]
                )
                if inputs or outputs:
                    entry["ports"] = {"inputs": inputs, "outputs": outputs}

                if inputs and any(
                    n.lower() in ("clk", "clock") for n in inputs
                ):
                    clk_name = next(
                        n for n in inputs if n.lower() in ("clk", "clock")
                    )
                    entry["clk"] = clk_name

            if entry:
                entries[vf.name] = entry

        if entries:
            yaml_path = dir_path / "tests.yaml"
            with open(yaml_path, "w") as f:
                f.write("# HDLbits test specifications\n")
                f.write("# Fill in test vectors for each module.\n")
                f.write("# Values are Python integers. Multi-bit use decimal.\n")
                f.write("#\n")
                yaml.dump(
                    entries,
                    f,
                    default_flow_style=None,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2,
                )
            created.append(yaml_path)

    return created
