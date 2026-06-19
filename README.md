# HDLBits

Personal solutions to [HDLBits](https://hdlbits.01xz.net/) exercises — a platform for learning digital logic design with Verilog/SystemVerilog.

## Structure

```
hdlBits/
├── basics/                      # Basic gates and wiring
├── modules/                     # Module instantiation and hierarchy
├── vectors/                     # Vectors, concatenation, replication
├── procedures/                  # Procedural blocks (always, if, case)
├── more_verilog_features/       # Reduction operators, generate, parameters
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

**Total: 43 modules implemented**

## Notes

- Some files contain multiple commented solution variants.
- Some exercises use SystemVerilog (`always_comb`, `logic`, `unique case`).
- Learning repository — may contain minor errors or experimental approaches.
- Each file is a standalone synthesizable module meant to be pasted into the HDLBits online simulator.

## Usage

```bash
iverilog -o <name> <file.v> && vvp <name>
```
