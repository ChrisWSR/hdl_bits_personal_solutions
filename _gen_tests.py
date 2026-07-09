#!/usr/bin/env python3
"""Auto-generate test vectors by simulating with iverilog.

Usage:
    python3 _gen_tests.py                    # generate all missing test vectors
    python3 _gen_tests.py basic_gates        # generate for one directory
"""

import yaml
import subprocess
import re
import sys
import itertools
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from hdlb_test.parser import parse_ports


def _find_module_name(v_path):
    text = v_path.read_text(errors="replace")
    m = re.search(r"\bmodule\s+(\w+)", text)
    return m.group(1) if m else "top_module"


def _input_combinations(inputs):
    """Generate all exhaustive input combinations as dicts."""
    names = list(inputs.keys())
    widths = [inputs[n]["width"] for n in names]
    total_bits = sum(widths)
    if total_bits > 20:
        return None  # too many
    for vals in itertools.product(*[range(2**w) for w in widths]):
        yield dict(zip(names, vals))


def _sampled_combinations(inputs):
    """Generate a smart sample of input combinations."""
    names = list(inputs.keys())
    widths = [inputs[n]["width"] for n in names]
    tests = []
    # all zeros
    tests.append({n: 0 for n in names})
    # all ones (per port)
    for n, w in zip(names, widths):
        tests.append({n: (2**w - 1) if w > 1 else 1})
    # alternating patterns for multi-bit
    for n, w in zip(names, widths):
        if w > 1:
            tests.append({n: 0b01010101010101010101010101010101 % (2**w)})
            tests.append({n: 0b10101010101010101010101010101010 % (2**w)})
    # some random-ish values
    tests.append({n: (i * 12345) % (2**w) for i, (n, w) in enumerate(zip(names, widths))})
    tests.append({n: (i * 67890) % (2**w) for i, (n, w) in enumerate(zip(names, widths))})
    # deduplicate by converting to tuples
    seen = set()
    unique = []
    for t in tests:
        key = tuple(sorted(t.items()))
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique


def _make_ref_tb(module_name, ports, patterns):
    """Generate a reference testbench that dumps outputs for each pattern."""
    inputs = {n: p for n, p in ports.items() if p["dir"] == "input"}
    outputs = {n: p for n, p in ports.items() if p["dir"] == "output"}
    has_clk = any(n.lower() in ("clk", "clock") for n in inputs)

    lines = []
    lines.append("`timescale 1ns/1ps")
    lines.append(f"module ref_{module_name}();")
    lines.append("")

    for name, info in inputs.items():
        if has_clk and name.lower() in ("clk", "clock"):
            continue
        w = f" [{info['width']-1}:0]" if info["width"] > 1 else ""
        lines.append(f"    reg{w} {name};")
    lines.append("")

    for name, info in outputs.items():
        w = f" [{info['width']-1}:0]" if info["width"] > 1 else ""
        lines.append(f"    wire{w} {name};")
    lines.append("")

    if has_clk:
        clk_name = next(n for n in inputs if n.lower() in ("clk", "clock"))
        lines.append(f"    reg {clk_name} = 0;")
        lines.append(f"    always #5 {clk_name} = ~{clk_name};")
        lines.append("")

    conns = ", ".join(f".{n}({n})" for n in ports)
    lines.append(f"    {module_name} dut({conns});")
    lines.append("")

    lines.append("    initial begin")
    lines.append('        $display("BEGIN");')

    if has_clk:
        clk_name = next(n for n in inputs if n.lower() in ("clk", "clock"))

    for i, pat in enumerate(patterns):
        for name in inputs:
            if has_clk and name.lower() in ("clk", "clock"):
                continue
            val = pat.get(name, 0)
            info = inputs[name]
            if info["width"] == 1:
                lines.append(f"        {name} = {val};")
            else:
                lines.append(f"        {name} = {info['width']}'d{val};")

        if has_clk:
            # Wait for posedge then read outputs
            lines.append(f"        @(posedge {clk_name});")
            lines.append("        #1;")
        else:
            lines.append("        #1;")

        # Print outputs
        disp_parts = [f"PAT:{i}"]
        for name in inputs:
            if has_clk and name.lower() in ("clk", "clock"):
                continue
            disp_parts.append(f"{name}=%0d")
        for name in outputs:
            disp_parts.append(f"{name}=%0d")
        fmt = ",".join(disp_parts)
        vars_list = []
        for name in inputs:
            if has_clk and name.lower() in ("clk", "clock"):
                continue
            vars_list.append(name)
        for name in outputs:
            vars_list.append(name)
        lines.append(f'        $display("{fmt}", {", ".join(vars_list)});')

    lines.append('        $display("END");')
    lines.append("        $finish(0);")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")

    return "\n".join(lines)


def _simulate(v_path, module_name, ports):
    """Run iverilog simulation and return list of output dicts."""
    inputs = {n: p for n, p in ports.items() if p["dir"] == "input"}
    outputs = {n: p for n, p in ports.items() if p["dir"] == "output"}
    has_clk = any(n.lower() in ("clk", "clock") for n in inputs)

    total_bits = sum(p["width"] for p in inputs.values())
    if total_bits <= 16:
        patterns = list(_input_combinations(inputs))
    else:
        patterns = _sampled_combinations(inputs)

    if not patterns:
        return None

    tb_text = _make_ref_tb(module_name, ports, patterns)
    slug = v_path.stem
    gen_dir = REPO_ROOT / "_generated"
    gen_dir.mkdir(parents=True, exist_ok=True)

    tb_path = gen_dir / f"ref_{slug}.v"
    tb_path.write_text(tb_text)

    out_path = gen_dir / f"ref_{slug}.out"
    comp = subprocess.run(
        ["iverilog", "-o", str(out_path), "-g2012", str(v_path), str(tb_path)],
        capture_output=True, text=True, timeout=30,
    )
    if comp.returncode != 0:
        err = (comp.stderr or comp.stdout)[:300]
        print(f"    COMPILE ERROR: {err}")
        return None

    sim = subprocess.run(
        ["vvp", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    if sim.returncode != 0 and not sim.stdout.strip():
        print(f"    SIM ERROR: {(sim.stderr or sim.stdout)[:200]}")
        return None

    # Parse output: PAT:<idx>,in1=val1,...,out1=val1,...
    results = []
    for line in sim.stdout.splitlines():
        line = line.strip()
        if line.startswith("PAT:"):
            parts = line.split(",")
            d = {}
            for p in parts[1:]:
                if "=" in p:
                    k, v = p.split("=", 1)
                    d[k.strip()] = int(v.strip())
            if d:
                results.append(d)
    return results


def _update_tests_yaml(tests_yaml_path, dry_run=False):
    """Update one tests.yaml file, filling in missing test vectors."""
    with open(tests_yaml_path) as f:
        data = yaml.safe_load(f) or {}

    dir_path = tests_yaml_path.parent
    changed = False

    for filename, spec in sorted(data.items()):
        if "tests" in spec and spec["tests"]:
            continue  # already has tests
        if "ports" not in spec:
            continue

        v_path = dir_path / filename
        if not v_path.exists():
            print(f"  SKIP {filename}: file not found")
            continue

        module_name = spec.get("module", "top_module")
        ports = parse_ports(v_path, module_name)
        if ports is None:
            # try discovering module name
            module_name = _find_module_name(v_path)
            if module_name != "top_module":
                spec["module"] = module_name
                ports = parse_ports(v_path, module_name)
        if ports is None:
            print(f"  SKIP {filename}: cannot parse ports")
            continue

        print(f"  Simulating {filename} (module={module_name})...", end=" ")
        sys.stdout.flush()
        results = _simulate(v_path, module_name, ports)
        if results is None:
            print("FAILED")
            continue

        # Build tests list
        inputs_list = sorted([n for n, p in ports.items() if p["dir"] == "input"])
        outputs_list = sorted([n for n, p in ports.items() if p["dir"] == "output"])
        has_clk = any(n.lower() in ("clk", "clock") for n in inputs_list)

        tests = []
        for r in results:
            test = {}
            for n in inputs_list:
                if has_clk and n.lower() in ("clk", "clock"):
                    continue
                if n in r:
                    test[n] = r[n]
            for n in outputs_list:
                if n in r:
                    test[n] = r[n]
            if test:
                tests.append(test)

        if tests:
            spec["tests"] = tests
            changed = True
            print(f"OK ({len(tests)} vectors)")
        else:
            print("no results generated")

    if changed and not dry_run:
        with open(tests_yaml_path, "w") as f:
            f.write("# HDLbits test specifications\n")
            f.write("# Auto-generated with _gen_tests.py\n")
            f.write("# Values are Python integers. Multi-bit use decimal.\n")
            f.write("#\n")
            yaml.dump(data, f, default_flow_style=None, allow_unicode=True,
                      sort_keys=False, indent=2)
        print(f"  -> Updated {tests_yaml_path.relative_to(REPO_ROOT)}")


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else None

    for tests_yaml in sorted(Path(REPO_ROOT).rglob("tests.yaml")):
        rel = tests_yaml.relative_to(REPO_ROOT)
        if targets and not any(t in str(rel) for t in targets):
            continue
        print(f"\n{rel}:")
        _update_tests_yaml(tests_yaml)


if __name__ == "__main__":
    main()
