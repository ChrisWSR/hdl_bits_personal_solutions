"""Iverilog compilation & simulation runner."""

import re
import subprocess
from pathlib import Path

IVERILOG = "iverilog"
VVP = "vvp"

GENERATED_DIR = None  # set by set_output_dir()


def set_output_dir(path):
    global GENERATED_DIR
    GENERATED_DIR = Path(path)


def run_one(source_path, tb_text):
    """Compile source + testbench with iverilog and run simulation.

    Returns a dict:
        {"status": "PASS"|"FAIL"|"COMPILE_ERROR"|"SIM_ERROR",
         "pass": int, "total": int, "fail_lines": [str],
         "detail": str}
    """
    slug = source_path.stem
    tb_path = GENERATED_DIR / f"tb_{slug}.v"
    output_path = GENERATED_DIR / f"{slug}.out"

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    tb_path.write_text(tb_text)

    comp = subprocess.run(
        [IVERILOG, "-o", str(output_path), "-g2012", str(source_path), str(tb_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if comp.returncode != 0:
        return {
            "status": "COMPILE_ERROR",
            "pass": 0,
            "total": 0,
            "fail_lines": [],
            "detail": (comp.stderr[:500] if comp.stderr else comp.stdout[:500]),
        }

    sim = subprocess.run(
        [VVP, str(output_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )

    stdout = sim.stdout or ""

    done_match = re.search(r"===DONE:.*?:(\d+)/(\d+)===", stdout)
    pass_count = int(done_match.group(1)) if done_match else 0
    total_count = int(done_match.group(2)) if done_match else 0

    fail_lines = [line for line in stdout.splitlines() if line.startswith("FAIL:")]

    if sim.returncode != 0 and pass_count == 0:
        return {
            "status": "SIM_ERROR",
            "pass": 0,
            "total": 0,
            "fail_lines": fail_lines or [(sim.stderr or stdout)[:300]],
            "detail": "",
        }

    status = "PASS" if pass_count == total_count and total_count > 0 else "FAIL"
    return {
        "status": status,
        "pass": pass_count,
        "total": total_count,
        "fail_lines": fail_lines,
        "detail": "",
    }
