---
title: "OHMind-ORCA MCP Server"
description: "Quantum chemistry MCP server for ORCA calculations"
category: "mcp-servers"
tags: ["quantum-chemistry", "orca", "dft", "calculations"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# OHMind-ORCA MCP Server

> Quantum chemistry tools for DFT calculations, geometry optimization, and property predictions using ORCA.

## Table of Contents

- [Overview](#overview)
- [Server Configuration](#server-configuration)
- [Tools Reference](#tools-reference)
- [Usage Examples](#usage-examples)
- [Results Format](#results-format)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The OHMind-ORCA MCP server provides 10 tools for quantum chemistry calculations using ORCA. It handles structure preparation, DFT calculations, geometry optimization, and various property predictions relevant to HEM design.

### Server Details

| Property | Value |
|----------|-------|
| Server Name | `OHMind-ORCA` |
| Entry Point | `python -m OHMind_agent.MCP.ORCA.server` |
| Tool Count | 10 |
| Dependencies | ORCA, RDKit, cclib |

### Capabilities

- SMILES to 3D coordinate conversion
- Single point energy calculations
- Geometry optimization
- Frequency calculations and thermochemistry
- Proton affinity and pKa estimation
- Binding energy calculations
- Charge analysis (Mulliken, Löwdin, Hirshfeld)
- NMR chemical shift prediction
- Transition state search

## Server Configuration

### Starting the Server

```bash
# stdio transport (default)
python -m OHMind_agent.MCP.ORCA.server --transport stdio

# HTTP transport
python -m OHMind_agent.MCP.ORCA.server --transport streamable-http --port 8103
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `PYTHONPATH` | Path to OHMind project | Yes |
| `OHMind_ORCA` | Path to ORCA binary | Yes |
| `OHMind_MPI` | Path to MPI binaries | For parallel |
| `QM_WORK_DIR` | Working directory | Yes |

### mcp.json Configuration

```json
{
  "OHMind-ORCA": {
    "command": "python",
    "args": ["-m", "OHMind_agent.MCP.ORCA.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "OHMind_ORCA": "/path/to/orca",
      "OHMind_MPI": "/usr/local/bin",
      "QM_WORK_DIR": "/OHMind_workspace/ORCA"
    }
  }
}
```

## Tools Reference

### Structure Preparation

#### `SmilesToXYZ`

Convert SMILES to 3D XYZ coordinates using RDKit.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: XYZ coordinate string

**Note**: Always use this tool first before running calculations.

**Example**:
```json
{
  "smiles": "C[N+]1(C)CCCCC1"
}
```

### Core Calculation Tools

#### `SinglePointEnergy`

Single-point energy calculation at fixed geometry.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | XYZ coordinates |
| `method` | string | No | DFT functional (default: `B3LYP`) |
| `basis` | string | No | Basis set (default: `def2-SVP`) |
| `dispersion` | string | No | Dispersion correction (default: `D3BJ`) |

**Returns**: Energy in Hartree, output file paths

**Available Methods**:
- `B3LYP` - Hybrid functional (default)
- `PBE0` - Hybrid functional
- `M06-2X` - Minnesota functional
- `wB97X-D3` - Range-separated with dispersion

**Available Basis Sets**:
- `def2-SVP` - Double-zeta (default, fast)
- `def2-TZVP` - Triple-zeta (accurate)
- `def2-QZVP` - Quadruple-zeta (very accurate)

#### `GeometryOptimization`

⚠️ **EXPENSIVE OPERATION** - Requires user approval

Optimize molecular geometry to find minimum energy structure.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | Initial XYZ coordinates |
| `method` | string | No | DFT functional |
| `basis` | string | No | Basis set |
| `dispersion` | string | No | Dispersion correction |

**Returns**: Optimized coordinates, final energy, results directory

**Estimated Time**: 5-30 minutes

#### `FrequencyCalculation`

⚠️ **EXPENSIVE OPERATION** - Requires user approval

Vibrational frequency calculation for thermochemistry.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | XYZ coordinates (should be optimized) |
| `method` | string | No | DFT functional |
| `basis` | string | No | Basis set |
| `temperature` | float | No | Temperature in K (default: 298.15) |

**Returns**: Frequencies, IR spectrum, thermochemistry, Gibbs free energy

**Estimated Time**: 5-30 minutes

### IEM-Focused Tools

#### `ProtonAffinityCalculation`

Proton affinity and approximate pKa for acidic groups.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | XYZ coordinates |
| `acidic_site` | integer | Yes | Atom index of acidic proton |
| `solvent` | string | No | Solvent for implicit solvation |

**Returns**: Gas-phase and solution-phase proton affinity, estimated pKa

#### `BindingEnergyCalculation`

Ion-functional group binding energies.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `complex_xyz` | string | Yes | Ion-molecule complex coordinates |
| `ion_xyz` | string | Yes | Isolated ion coordinates |
| `molecule_xyz` | string | Yes | Isolated molecule coordinates |
| `bsse_correction` | boolean | No | Apply BSSE correction |
| `solvent` | string | No | Implicit solvation |

**Returns**: Binding energy with/without corrections

#### `IonicSolvationEnergy`

Solvation/hydration energies for ions.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | Ion or ion-water cluster coordinates |
| `charge` | integer | Yes | Total charge |
| `solvent` | string | Yes | Solvent model |

**Returns**: Solvation energy and free energy

#### `ChargeAnalysis`

Calculate atomic charges using various methods.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | XYZ coordinates |
| `methods` | array | No | Charge methods (default: all) |

**Available Methods**:
- `mulliken` - Mulliken population analysis
- `loewdin` - Löwdin population analysis
- `hirshfeld` - Hirshfeld charges

**Returns**: Charges per atom, dipole/quadrupole moments

#### `TransitionStateSearch`

⚠️ **EXPENSIVE OPERATION** - Requires user approval

Transition state search with optional frequency verification.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | Initial TS guess coordinates |
| `method` | string | No | DFT functional |
| `verify_frequencies` | boolean | No | Run frequency calculation to verify |

**Returns**: TS geometry, activation energy, imaginary frequency

#### `NMRChemicalShift`

⚠️ **EXPENSIVE OPERATION** - Requires user approval

NMR shielding and chemical shifts.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `xyz_string` | string | Yes | XYZ coordinates |
| `nuclei` | array | No | Nuclei to calculate |
| `reference` | string | No | Reference compound |

**Available Nuclei**:
- `1H` - Proton
- `13C` - Carbon-13
- `19F` - Fluorine-19
- `31P` - Phosphorus-31

**Returns**: Chemical shifts for selected nuclei

## Usage Examples

### End-to-End QM Descriptor Pipeline

```
Using your OHMind-ORCA QM tools, start from the SMILES `C[N+]1(C)CCCCC1` and:

1) Convert to a reasonable 3D geometry.
2) Optimize the structure at B3LYP/def2-SVP with D3BJ.
3) Compute frequencies to confirm there are no imaginary modes.
4) Report LUMO energy and any descriptors relevant to alkaline stability, 
   and interpret them qualitatively.
```

### Proton Affinity and pKa Estimation

```
For a sulfonic-acid-containing fragment, use your proton affinity tool to 
estimate gas-phase and solution-phase proton affinity and the corresponding pKa.

Explain what these values imply for acid strength and membrane behavior.
```

### Binding and Solvation Comparison

```
Compare the binding energy and hydration energy of OH⁻ vs Cl⁻ to a model 
quaternary ammonium site using your ORCA binding and solvation tools.

Summarize which ion binds more strongly and how solvation competes with binding.
```

### Simple Single Point Calculation

```
Calculate the single point energy for this cation: C[N+]1(C)CCCCC1
Use B3LYP/def2-SVP with D3BJ dispersion correction.
```

## Results Format

### Output Directory Structure

QM results are saved to `$QM_WORK_DIR/`:

```
$QM_WORK_DIR/
├── temp_<timestamp>/     # Per-job temporary directories
│   ├── input.inp         # ORCA input file
│   ├── input.out         # ORCA output file
│   ├── input.gbw         # Wavefunction file
│   ├── input.xyz         # Final geometry
│   └── input.hess        # Hessian (for frequencies)
└── results/              # Preserved results
```

### Output File Contents

| File | Contents |
|------|----------|
| `input.inp` | ORCA input with method, basis, coordinates |
| `input.out` | Full ORCA output with energies, properties |
| `input.gbw` | Binary wavefunction for Multiwfn analysis |
| `input.xyz` | Optimized geometry (if optimization) |

### Energy Units

| Property | Unit |
|----------|------|
| Total energy | Hartree |
| Binding energy | kcal/mol |
| Proton affinity | kcal/mol |
| Frequencies | cm⁻¹ |
| Gibbs free energy | Hartree |

## Troubleshooting

### Common Issues

#### ORCA Not Found

```
Error: ORCA executable not found
```

**Solution**: Set the ORCA path:
```bash
export OHMind_ORCA=/path/to/orca
```

#### MPI Not Available

```
Warning: MPI not found, running in serial mode
```

**Solution**: Set MPI path for parallel calculations:
```bash
export OHMind_MPI=/usr/local/bin
```

#### Calculation Failed

```
Error: ORCA calculation failed
```

**Solutions**:
1. Check `input.out` for error messages
2. Verify input geometry is reasonable
3. Try a smaller basis set
4. Check disk space in `QM_WORK_DIR`

#### Memory Error

```
Error: Not enough memory
```

**Solution**: Reduce basis set size or molecule size. ORCA memory is controlled in the input file.

### Expensive Operations

The following tools require validation before execution:

| Tool | Estimated Time |
|------|----------------|
| `GeometryOptimization` | 5-30 minutes |
| `FrequencyCalculation` | 5-30 minutes |
| `NMRChemicalShift` | 10-60 minutes |
| `TransitionStateSearch` | 15-60 minutes |

### Debug Mode

Run the server with verbose logging:

```bash
PYTHONPATH=/path/to/OHMind \
  OHMind_ORCA=/path/to/orca \
  QM_WORK_DIR=/OHMind_workspace/ORCA \
  python -m OHMind_agent.MCP.ORCA.server --transport stdio 2>&1 | tee orca_debug.log
```

## See Also

- [MCP Server Reference](./index.md) - Overview of all servers
- [QM Agent](../agents/qm-agent.md) - Agent documentation
- [Multiwfn Server](./multiwfn-server.md) - For result analysis
- [QM Calculations Tutorial](../tutorials/qm-calculations.md) - Step-by-step guide
- [OHQM Module](../core-library/ohqm.md) - QM utilities

---
*Last updated: 2025-12-22 | OHMind v1.0.0*
