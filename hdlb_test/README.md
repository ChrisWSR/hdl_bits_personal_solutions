# hdlb_test

Python package for HDLBits exercise verification — parses Verilog, loads test vectors from YAML, and drives simulation via cocotb.

## Pipeline

```
tests.yaml (per dir)
       │
       ▼
tests/conftest.py         discover modules via loader.py
       │
       ▼
tests/test_modules.py     @pytest.mark.parametrize, one test per module
       │
       ▼
cocotb_test.simulator.run()
       │
  ┌────┴────┐
  │ iverilog│   compile .v + cocotb VPI
  └────┬────┘
       ▼
  vvp + libcocotb     loads hdlb_test/cocotb_tb.py
       │
       ▼
hdlb_test/cocotb_tb.py  applies test vectors, asserts outputs
```

## Components

### `cocotb_tb.py` — cocotb test module

Loaded by the simulator at runtime. Reads test vectors from a JSON file pointed to by `HDLBITS_TESTS` env var. Applies inputs, waits for clock edge if `HDLBITS_CLK` is set, then asserts outputs match expectations.

Supports two modes:
- **Combinational / flat-vector** (`tests:` in YAML) — applies each vector independently.
- **Sequential sequence** (`sequence:` + `expected:` in YAML) — applies steps over multiple clock cycles and checks outputs per cycle.

When `WAVES=1` is set, enables VCD waveform dumping to `dump.vcd` for debugging.

This is the only file that runs *inside* the simulator (via VPI).

### `parser.py` — Verilog port parser

Parses module port declarations from `.v` files. Handles direction (`input`/`output`) and bit-width (`[4:0]`, `[N-1:0]`), including inherited widths (`input [4:0] a, b, c`). Used by `conftest.py` and `_gen_tests.py`.

### `loader.py` — YAML test loader with Pydantic validation

Reads per-directory `tests.yaml` files and returns `{relative_path → spec}` dicts. Each spec contains ports, module name, clock signal, test vectors or sequences, and expected outputs.

Validates every spec against `ModuleSpec` (Pydantic model) at load time, catching YAML errors early with clear messages. Rejects empty `tests` or `sequence` lists.

### `loader.py` — also provides `init_specs()` for stub generation

`run_tests.py --init` calls `loader.init_specs()` to scan directories and generate `tests.yaml` stubs with parsed ports but empty test vectors.

```yaml
# basics/tests.yaml
03_and_gate.v:
  module: and_gate              # optional, defaults to top_module
  ports:                         # optional, auto-parsed if missing
    inputs: [a, b]
    outputs: [out]
  tests:
    - {a: 0, b: 0, out: 0}
    - {a: 0, b: 1, out: 0}
    - {a: 1, b: 0, out: 0}
    - {a: 1, b: 1, out: 1}
```

### Sequential (flat vectors)

```yaml
dff.v:
  module: dff
  clk: clk
  tests:
    - {clk: 0, d: 0, q: 0}
    - {clk: 1, d: 1, q: 1}
```

### Sequential (multi-cycle sequences)

For modules where behavior depends on state across cycles (counters, shift registers, FSMs):

```yaml
dff_syncres.v:
  module: dff_syncres
  clk: clk
  sequence:
    - {d: 1, reset: 0}
    - {d: 0, reset: 0}
    - {d: 1, reset: 1}
  expected:
    q: [1, 1, 0]
```

Each step in `sequence` is applied on one clock cycle. After each rising edge, all outputs listed in `expected` are checked against the corresponding index.

Vector values are integers (decimal). The test module converts them to the correct bit-width before applying to the DUT.

## Test execution flow

1. `conftest.py` scans all directories for `tests.yaml` files. Each spec is validated against `ModuleSpec` (Pydantic) at load time.
2. For each module with non-empty `tests` or `sequence`, a pytest test is generated.
3. The test writes vectors/sequence/expected to a temp JSON file and calls `cocotb_test.simulator.run()`:
   - compiles the `.v` file with iverilog
   - loads `hdlb_test/cocotb_tb.py` as the cocotb test module
   - passes `HDLBITS_TESTS=/path/to/vectors.json` and `HDLBITS_CLK=<clk>` via env
   - if `WAVES=1`, also passes `WAVES` env var for VCD dump
4. Inside the simulator, `cocotb_tb.py` applies each vector/sequence step and asserts outputs.
5. Pytest collects PASS/FAIL and prints a summary.

## Auto-generating vectors

`_gen_tests.py` (at project root) simulates modules exhaustively (≤16 input bits) or sampled, and writes results into `tests.yaml`. It uses `parser.py` to identify ports and `loader.py` to read existing specs.

## Dependencies

- `cocotb` — Python coroutine-based verification library
- `cocotb-test` — pytest integration for cocotb
- `pyyaml` — YAML loading
- `pytest` — test framework
- `pydantic` — YAML spec validation at load time
- `iverilog` (external) — Icarus Verilog simulator

## Debugging

Set `WAVES=1` to dump VCD waveforms on failure:

```bash
WAVES=1 pytest tests/ -k "dff" --tb=long
# Then open _generated/sim_dff/dump.vcd in GTKWave
```
