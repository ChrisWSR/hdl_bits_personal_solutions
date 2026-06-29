"""CLI orchestration."""

from __future__ import annotations

import json
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

from . import loader
from .parser import parse_ports
from .generator import gen_tb
from .runner import run_one, set_output_dir

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = REPO_ROOT / "_generated"


def _green(s: str) -> str:
    return f"\033[92m{s}\033[0m"


def _red(s: str) -> str:
    return f"\033[91m{s}\033[0m"


def _yellow(s: str) -> str:
    return f"\033[93m{s}\033[0m"


def _cyan(s: str) -> str:
    return f"\033[96m{s}\033[0m"


# ─── commands ───────────────────────────────────────────────────────


def cmd_init() -> None:
    """Generate tests.yaml per directory."""
    created = loader.init_specs(REPO_ROOT)
    print(_green(f"Wrote {len(created)} tests.yaml files."))
    for p in created:
        rel = p.relative_to(REPO_ROOT)
        print(f"  {rel}")


def _write_report(
    results: list[dict[str, Any]],
    total_pass: int,
    total_tests: int,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write JSON and Markdown report files."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    json_path = output_dir / "report.json"
    md_path = output_dir / "report.md"

    summary = {
        "timestamp": ts,
        "passed": total_pass,
        "total": total_tests,
        "all_passed": total_pass == total_tests,
    }

    rows = []
    for r in results:
        rows.append({
            "file": r["rel"],
            "status": r["status"],
            "passed": r.get("pass", 0),
            "total": r.get("total", 0),
            "fail_lines": r.get("fail_lines", []),
        })

    report = {**summary, "results": rows}
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n")

    md = [
        f"# Test Report — {ts}",
        "",
        f"**Result:** {'PASS' if summary['all_passed'] else 'FAIL'}  "
        f"**{total_pass}/{total_tests}** passed",
        "",
        "| File | Status | Tests |",
        "|------|--------|-------|",
    ]
    for r in rows:
        badge = {
            "PASS": "PASS", "FAIL": "FAIL",
            "COMPILE_ERROR": "COMPILE_ERR", "SIM_ERROR": "SIM_ERROR",
            "PARSE_ERROR": "PARSE_ERR",
        }.get(r["status"], r["status"])
        t = f"{r['passed']}/{r['total']}" if r["total"] > 0 else "—"
        md.append(f"| {r['file']} | {badge} | {t} |")

    md.append("")
    md_path.write_text("\n".join(md) + "\n")

    return json_path, md_path


def cmd_test(
    targets: list[str] | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    report: bool = False,
) -> bool:
    """Run tests for all or specified files."""
    specs = loader.load_all_specs(REPO_ROOT)
    if not specs:
        print(
            _yellow("No tests.yaml files found. Run 'run_tests.py --init' first.")
        )
        sys.exit(1)

    set_output_dir(GENERATED_DIR)

    if targets:
        test_targets: list[Path] = []
        for t in targets:
            p = Path(t).resolve()
            if p.exists():
                test_targets.append(p)
            else:
                p2 = (REPO_ROOT / t).resolve()
                if p2.exists():
                    test_targets.append(p2)
                else:
                    print(_red(f"File not found: {t}"))
                    sys.exit(1)
    else:
        test_targets = sorted(
            (REPO_ROOT / rel).resolve() for rel in specs
            if (REPO_ROOT / rel).exists()
        )

    if not test_targets:
        print(_yellow("No matching files found."))
        sys.exit(0)

    if dry_run:
        print(_cyan(f"Would test {len(test_targets)} file(s):"))
        for p in test_targets:
            rel = p.relative_to(REPO_ROOT)
            spec = specs.get(str(rel), {})
            tcount = len(spec.get("tests", []))
            print(f"  {rel}  ({tcount} test vectors)")
        return True

    results: list[dict[str, Any]] = []
    total_pass = 0
    total_tests = 0
    max_len = max(len(str(p.relative_to(REPO_ROOT))) for p in test_targets)

    print()
    print(f"  {'File'.ljust(max_len)}  {'Status':12}  {'Tests':8}")
    print(f"  {'-' * max_len}  {'-' * 12}  {'-' * 8}")
    print()

    for src_path in test_targets:
        rel = str(src_path.relative_to(REPO_ROOT))
        spec = specs.get(rel, {})
        tests = spec.get("tests", [])
        module_name = spec.get("module", "top_module")
        clk = spec.get("clk")

        if not tests:
            if verbose:
                print(f"  {rel.ljust(max_len)}  {_yellow('SKIP'):12}")
            continue

        ports = parse_ports(src_path, module_name)
        if ports is None:
            results.append({"rel": rel, "status": "PARSE_ERROR", "pass": 0, "total": 0})
            print(f"  {rel.ljust(max_len)}  {_red('PARSE_ERR'):12}")
            continue

        tb_text = gen_tb(src_path, module_name, ports, tests, clk)
        result = run_one(src_path, tb_text)
        result["rel"] = rel
        result.setdefault("pass", 0)
        result.setdefault("total", 0)
        results.append(result)

        s = result["status"]
        if s == "PASS":
            ss = _green("PASS")
        elif s == "FAIL":
            ss = _red("FAIL")
        elif s in ("COMPILE_ERROR", "SIM_ERROR"):
            ss = _yellow(s)
        else:
            ss = _yellow(s)

        ts = f"{result['pass']}/{result['total']}" if result["total"] > 0 else ""
        print(f"  {rel.ljust(max_len)}  {ss:12}  {ts:8}")

        if verbose and result["status"] in ("FAIL", "COMPILE_ERROR", "SIM_ERROR"):
            for fl in result.get("fail_lines", []):
                print(f"    {_red(fl)}")
            if result.get("detail"):
                print(f"    {_yellow(result['detail'][:200])}")

        if result["status"] == "PASS":
            total_pass += 1
        total_tests += 1

    print()
    ss = _green("PASS") if total_pass == total_tests else _red("FAIL")
    print(f"  Summary: {ss}  {total_pass}/{total_tests} passed")
    print()

    if report and results:
        json_p, md_p = _write_report(results, total_pass, total_tests, GENERATED_DIR)
        print(_cyan(f"  Report written to:"))
        print(f"    {json_p.relative_to(REPO_ROOT)}")
        print(f"    {md_p.relative_to(REPO_ROOT)}")
        print()

    return total_pass == total_tests


# ─── entry point ────────────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="HDLbits test runner — Plan B",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              %(prog)s                        run all tests
              %(prog)s basics/03_and_gate.v   run one file
              %(prog)s --init                 generate tests.yaml files
              %(prog)s --dry-run              preview
              %(prog)s --verbose              detailed output
            """
        ),
    )
    parser.add_argument("targets", nargs="*", help=".v files to test")
    parser.add_argument("--init", action="store_true", help="Generate tests.yaml files")
    parser.add_argument("--dry-run", action="store_true", help="Preview")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detailed output")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Write JSON and Markdown report to _generated/")

    args = parser.parse_args()

    if args.init:
        cmd_init()
        return

    ok = cmd_test(
        targets=args.targets or None,
        dry_run=args.dry_run,
        verbose=args.verbose,
        report=args.report,
    )
    sys.exit(0 if ok is None or ok else 1)
