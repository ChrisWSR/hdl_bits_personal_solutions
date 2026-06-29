"""Verilog testbench generator."""


def _verilog_value(val, width):
    """Format a Python int as a Verilog literal."""
    if width == 1:
        return f"{val}"
    return f"{width}'d{val}"


def _make_slug(*parts):
    return "_".join(str(p) for p in parts)


def gen_tb(source_path, module_name, ports, tests, clk=None):
    """Generate a Verilog testbench as a string.

    Parameters
    ----------
    source_path : Path
        Path to the source .v file (used for slug).
    module_name : str
        Name of the module under test.
    ports : dict
        {name: {"dir": ..., "width": int}} from the parser.
    tests : list of dict
        Each dict maps port names to Python ints.
    clk : str or None
        Name of the clock signal (generates a free-running clock).
    """
    inputs = {n: p for n, p in ports.items() if p["dir"] == "input"}
    outputs = {n: p for n, p in ports.items() if p["dir"] == "output"}

    lines = []
    lines.append("`timescale 1ns/1ps")
    lines.append(f"module tb_{module_name}();")
    lines.append("")

    for name, info in inputs.items():
        if clk and name == clk:
            continue
        w = f" [{info['width']-1}:0]" if info["width"] > 1 else ""
        lines.append(f"    reg{w} {name};")
    lines.append("")

    for name, info in outputs.items():
        w = f" [{info['width']-1}:0]" if info["width"] > 1 else ""
        lines.append(f"    wire{w} {name};")
    lines.append("")

    if clk:
        lines.append(f"    reg {clk} = 0;")
        lines.append(f"    always #5 {clk} = ~{clk};")
        lines.append("")

    conns = ", ".join(f".{n}({n})" for n in ports)
    lines.append(f"    {module_name} dut({conns});")
    lines.append("")

    lines.append("    integer _tn = 0;")
    lines.append("    integer _ok = 0;")
    lines.append("    integer _fail = 0;")
    lines.append("")

    lines.append("    initial begin")
    lines.append(f'        $display("===START:{_make_slug(source_path.stem, module_name)}===");')
    lines.append("")

    slug = _make_slug(source_path.stem, module_name)
    for idx, test in enumerate(tests, 1):
        lines.append(f"        _tn = {idx};")
        for name, info in inputs.items():
            if name in test:
                val = test[name]
            elif clk and name == clk:
                continue
            else:
                val = 0
            lines.append(f"        {name} = {_verilog_value(val, info['width'])};")

        if clk:
            lines.append(f"        @(posedge {clk});")
        lines.append("        #1;")

        checks = [
            (n, _verilog_value(test[n], info["width"]))
            for n, info in outputs.items()
            if n in test
        ]
        if checks:
            fail_cond = " || ".join(f"({n} !== {exp})" for n, exp in checks)
            lines.append(f"        if ({fail_cond}) begin")
            lines.append(f'            $write("FAIL:{slug}:{idx}");')
            for n, exp in checks:
                lines.append(f'            $write(" {n}=%0d(expected=%0d)", {n}, {exp});')
            lines.append('            $write("\\n");')
            lines.append("            _fail = _fail + 1;")
            lines.append("        end else begin")
            lines.append("            _ok = _ok + 1;")
            lines.append("        end")
        else:
            lines.append("            _ok = _ok + 1;")
        lines.append("")

    lines.append(f'        $display("===DONE:{slug}:%0d/%0d===", _ok, _tn);')
    lines.append("        if (_fail > 0) $finish(1);")
    lines.append("        else $finish(0);")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")
    lines.append("")

    return "\n".join(lines)
