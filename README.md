# HDLBits

Personal solutions to [HDLBits](https://hdlbits.01xz.net/) exercises — a platform for learning digital logic design with Verilog/SystemVerilog.

## Structure

```
hdlBits/
├── run_tests.py                  # Test runner entry point
├── _gen_tests.py                 # Auto-generate test vectors via iverilog
├── hdlb_test/                    # Python package
│   ├── cli.py                    #   CLI orchestration (legacy init)
│   ├── parser.py                 #   Verilog port list parser
│   ├── cocotb_tb.py              #   Cocotb test module (loaded by simulator)
│   ├── generator.py              #   Legacy testbench generator
│   ├── runner.py                 #   Legacy iverilog runner
│   └── loader.py                 #   Per-directory YAML loader
├── tests/                        # Pytest test suite
│   ├── conftest.py               #   Fixtures & module discovery
│   └── test_modules.py           #   Parameterized cocotb tests
├── pyproject.toml                # Project config & dependencies
├── .gitignore
├── Makefile
├── basics/                       # Basic gates and wiring
├── modules/                      # Module instantiation and hierarchy
├── vectors/                      # Vectors, concatenation, replication
├── procedures/                   # Procedural blocks (always, if, case)
├── more_verilog_features/        # Reduction operators, generate, parameters
└── Circuits/
    ├── combinational_logic/
    │   ├── basic_gates/
    │   ├── multiplexers/
    │   ├── arithmetic_circuits/
    │   └── karnaugh_map_to_circuit/
    └── sequential_logic/
        ├── latches_and_flip_flops/
        ├── counters/
        ├── shift_registers/
        ├── more_circuits/
        ├── finite_state_machines/
        └── building_larger_circuits/
```

## Contents

| Folder | Files | Topics |
|---|---|---|
| **basics/** | 10 | Assignments, AND/OR/NAND/NOR/XNOR gates, 7458 chip |
| **modules/** | 9 | Port connections (name/position), adders, shift registers, carry-select |
| **vectors/** | 9 | Vectors, concatenation `{}`, replication `{n{}}`, sign extension, bit reversal |
| **procedures/** | 8 | `always`, `if`/`else`, `case`/`casez`, priority, latches |
| **more_verilog_features/** | 7 | Reduction, generate-for, popcount, ripple-carry, BCD adder |
| **basic_gates** | 17 | Wire, GND, NOR/AND-OR-INVERT, 7420, truth tables, equality, ring/vibrate, popcount3, gatesv |
| **multiplexers** | 5 | 2-to-1, 9-to-1, 256-to-1, indexed vector part-select |
| **arithmetic_circuits** | 7 | Half/full adder, signed adder, BCD adder, 100-bit adder |
| **karnaugh_map_to_circuit** | 8 | K-map minimization, SOP/POS, don't-cares, minterm/maxterm |
| **latches_and_flip_flops** | 11 | DFF, DFF with reset/enable, JK/muxed DFF, edge-detect |
| **counters** | 12 | 4-bit binary/decade counter, 12-hour clock |
| **shift_registers** | 6 | 4-bit shift, rotator, LFSR, 5-input LUT |
| **more_circuits** | 7 | Rule 90/110, Conway's Game of Life |
| **finite_state_machines** | 27 | Moore/Mealy, edge-detect, serial receiver, LE, DRAM |
| **building_larger_circuits** | 2 | 4-bit variant, counter + FSM |

**Total: ~100/182 modules implemented** (71 with test vectors, 100% passing)

## Quick Start

### Install

```bash
pip install cocotb cocotb-test pyyaml pytest
```

### Run tests

```bash
make init         # scan all .v files, generate tests.yaml stubs (if needed)
make test         # run all tests with pytest & cocotb
make test-one FILE=and_gate   # test matching modules
make list         # list all discovered tests
make clean        # remove generated files
```

Or directly:

```bash
python3 -m pytest tests/ -v                              # run all
python3 -m pytest tests/ -k "and_gate" --tb=short        # filter by name
python3 run_tests.py                                      # same as pytest tests/
python3 run_tests.py --init                               # generate tests.yaml stubs
```

### Auto-generating test vectors

For modules that have `tests.yaml` stubs with no test data:

```bash
python3 _gen_tests.py                       # generate vectors for all stubs
python3 _gen_tests.py basic_gates           # generate for one directory
```

This simulates the module with iverilog (exhaustive for ≤16 input bits, sampled for larger).

## How the test infrastructure works

1. **Test vectors** are stored in per-directory `tests.yaml` files alongside the Verilog source.
2. **Pytest** discovers modules from `tests.yaml` and creates one parameterized test per module.
3. Each test uses **cocotb-test** (`cocotb_test.simulator.run`) to:
   - Compile the `.v` file with Icarus Verilog
   - Load the cocotb VPI library
   - Run the Python test module (`hdlb_test/cocotb_tb.py`)
4. The cocotb test applies each test vector, waits for clock edges (if `clk` is specified), and asserts output values match expectations.

### Adding tests

Edit the `tests.yaml` in the relevant directory:

```yaml
# basics/tests.yaml
03_and_gate.v:
  module: and_gate
  tests:
    - {a: 0, b: 0, out: 0}
    - {a: 0, b: 1, out: 0}
    - {a: 1, b: 0, out: 0}
    - {a: 1, b: 1, out: 1}
```

For modules not named `top_module`, add `module: <name>`. For sequential modules, add `clk: <name>`.

## Notes

- Some files contain multiple commented solution variants.
- Some exercises use SystemVerilog (`always_comb`, `logic`, `unique case`).
- Learning repository — may contain minor errors or experimental approaches.
- Each file is a standalone synthesizable module meant to be pasted into the HDLBits online simulator.
