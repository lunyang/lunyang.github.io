---
title: "OHMind-GROMACS MCP Server"
description: "Molecular dynamics MCP server for IEM simulations using GROMACS"
category: "mcp-servers"
tags: ["molecular-dynamics", "gromacs", "simulations", "polymers"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: MCP Server Reference
nav_order: 5
---

# OHMind-GROMACS MCP Server

> Comprehensive molecular dynamics tools for ion exchange membrane simulations using GROMACS.

## Table of Contents

- [Overview](#overview)
- [Server Configuration](#server-configuration)
- [Tools Reference](#tools-reference)
- [Usage Examples](#usage-examples)
- [Results Format](#results-format)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The OHMind-GROMACS MCP server provides 25+ tools for molecular dynamics simulations of polymer ion exchange membranes. It handles the complete workflow from monomer SMILES to production MD and analysis.

### Server Details

| Property | Value |
|----------|-------|
| Server Name | `OHMind-GROMACS` |
| Entry Point | `python -m OHMind_agent.MCP.GROMACS.server` |
| Tool Count | 25+ |
| Dependencies | GROMACS, AmberTools, PACKMOL, OpenBabel |

### Capabilities

- Polymer building from SMILES
- Force field parameterization (AMBER/GAFF)
- System preparation and solvation
- Ion addition and charge balancing
- MD simulation (EM, NVT, NPT, production)
- Trajectory and energy analysis
- Complete IEM workflow automation

## Server Configuration

### Starting the Server

```bash
# stdio transport (default)
python -m OHMind_agent.MCP.GROMACS.server --transport stdio

# HTTP transport
python -m OHMind_agent.MCP.GROMACS.server --transport streamable-http --port 8105
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `PYTHONPATH` | Path to OHMind project | Yes |
| `MD_WORK_DIR` | Working directory | Yes |
| `OHMind_workspace` | Base workspace path | Yes |

### mcp.json Configuration

```json
{
  "OHMind-GROMACS": {
    "command": "python",
    "args": ["-m", "OHMind_agent.MCP.GROMACS.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "MD_WORK_DIR": "/OHMind_workspace/GROMACS",
      "OHMind_workspace": "/OHMind_workspace"
    }
  }
}
```

### Software Requirements

| Software | Purpose | Required |
|----------|---------|----------|
| GROMACS | MD simulations | Yes |
| AmberTools | Parameterization | Yes |
| PACKMOL | System packing | Yes |
| OpenBabel | Format conversion | Recommended |

## Tools Reference

### High-Level Workflow Tools

#### `run_complete_iem_workflow_tool`

⚠️ **VERY EXPENSIVE** - Requires user approval

Complete IEM MD workflow from monomer SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Monomer SMILES |
| `num_chains` | integer | No | Number of polymer chains (default: 10) |
| `degree_of_polymerization` | integer | No | Chain length (default: 25) |
| `temperature` | float | No | Simulation temperature in K (default: 353.15) |
| `water_model` | string | No | Water model (default: `spce`) |
| `simulation_time` | float | No | Production time in ns |

**Returns**: Complete simulation results

**Estimated Time**: 1-4 hours

#### `run_complete_md_simulation_tool`

⚠️ **VERY EXPENSIVE** - Requires user approval

Full EM → NVT → NPT → MD pipeline.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gro_file` | string | Yes | Initial coordinates |
| `top_file` | string | Yes | Topology file |
| `temperature` | float | No | Target temperature in K |
| `pressure` | float | No | Target pressure in bar |
| `production_time` | float | No | Production time in ns |

**Returns**: Simulation trajectory and analysis

**Estimated Time**: 1-4 hours

### Analysis Tools

#### `calculate_ions_per_monomer_tool`

Calculate ion content from monomer SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Monomer SMILES string |

**Returns**: Number of ionizable sites per monomer

#### `analyze_ion_exchange_groups_tool`

Advanced analysis of ion-exchange groups in monomers.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Monomer SMILES string |

**Returns**: Detailed analysis of functional groups

### Building Tools

#### `create_polymer_from_smiles_tool`

Build oligomer/polymer PDB structures from monomer SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Monomer SMILES |
| `degree_of_polymerization` | integer | Yes | Number of repeat units |
| `num_chains` | integer | No | Number of polymer chains |

**Returns**: Path to generated PDB file

#### `create_itp_file_tool`

End-to-end workflow from polymer PDB to GROMACS `.itp` file.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pdb_file` | string | Yes | Path to polymer PDB |
| `charge_method` | string | No | Charge calculation method |

**Returns**: Path to generated ITP file

Uses Antechamber + tleap + conversion + extraction pipeline.

### Parameterization Tools

#### `parameterize_molecule_antechamber_tool`

Run Antechamber on a molecule for charges and atom types.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pdb_file` | string | Yes | Input PDB file |
| `charge_method` | string | No | AM1-BCC or other method |

**Returns**: Parameterization results

#### `prepare_mainchain_files_tool`

Produce HEAD/CHAIN/TAIL mainchain definitions.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `antechamber_output` | string | Yes | Path to Antechamber output |

**Returns**: Mainchain definition files

#### `run_prepgen_tool`

Generate PREPI residue files from mainchain definitions.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mainchain_files` | string | Yes | Path to mainchain files |

**Returns**: PREPI file path

#### `build_polymer_with_tleap_tool`

Build polymer chains with tleap for topology generation.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prepi_file` | string | Yes | PREPI residue file |
| `num_chains` | integer | Yes | Number of chains |
| `chain_length` | integer | Yes | Monomers per chain |

**Returns**: AMBER topology and coordinate files

#### `convert_amber_to_gromacs_tool`

Convert AMBER topologies to GROMACS formats.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prmtop` | string | Yes | AMBER parameter file |
| `inpcrd` | string | Yes | AMBER coordinate file |

**Returns**: GROMACS `.top` and `.gro` files

#### `extract_ff_and_itp_tool`

Extract `forcefield.itp` and monomer `.itp` from a `.top` file.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `top_file` | string | Yes | GROMACS topology file |

**Returns**: Extracted ITP files

### System Preparation Tools

#### `calculate_single_ion_system_tool`

Compute system composition and charge balance.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `polymer_charge` | integer | Yes | Total polymer charge |
| `target_water_content` | float | Yes | Water uptake target |
| `ion_type` | string | Yes | Counter-ion type |

**Returns**: System composition details

**Available Ion Types**:
| Ion | Charge |
|-----|--------|
| `OH` | -1 |
| `Cl` | -1 |
| `Br` | -1 |
| `NO3` | -1 |
| `ClO4` | -1 |
| `H2PO4` | -1 |
| `CO3` | -2 |
| `SO4` | -2 |
| `HPO4` | -2 |

#### `create_system_topology_tool`

Build system `.top` with polymers, ions, and water.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `polymer_itp` | string | Yes | Polymer ITP file |
| `num_polymers` | integer | Yes | Number of polymer chains |
| `num_ions` | integer | Yes | Number of counter-ions |
| `water_model` | string | Yes | Water model name |

**Returns**: System topology file

#### `create_packmol_input_tool`

Run PACKMOL-based initial packing.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `components` | array | Yes | System components |
| `box_size` | array | Yes | Box dimensions |

**Returns**: Packed coordinate file

#### `prepare_simulation_box_tool`

Use `gmx editconf` to define simulation box.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_gro` | string | Yes | Input coordinate file |
| `box_type` | string | No | Box type (cubic, dodecahedron) |
| `box_size` | array | No | Box dimensions |

**Returns**: Box-defined coordinate file

### Simulation Tools

#### `create_mdp_file_tool`

Generate MDP files for different simulation phases.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `simulation_type` | string | Yes | `em`, `nvt`, `npt`, or `md` |
| `temperature` | float | No | Target temperature in K |
| `pressure` | float | No | Target pressure in bar |
| `nsteps` | integer | No | Number of steps |
| `dt` | float | No | Timestep in ps |

**Returns**: Path to MDP file

**Simulation Types**:
| Type | Description |
|------|-------------|
| `em` | Energy minimization |
| `nvt` | NVT equilibration |
| `npt` | NPT equilibration |
| `md` | Production MD |

#### `run_grompp_tool`

Prepare TPR files via `gmx grompp`.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mdp_file` | string | Yes | MDP parameter file |
| `gro_file` | string | Yes | Coordinate file |
| `top_file` | string | Yes | Topology file |

**Returns**: TPR file path

#### `run_mdrun_tool`

⚠️ **EXPENSIVE OPERATION** - Requires user approval

Execute MD runs with `gmx mdrun`.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tpr_file` | string | Yes | TPR input file |
| `ntomp` | integer | No | OpenMP threads |

**Returns**: Trajectory and output files

### Analysis Tools

#### `calculate_msd_tool`

Compute MSD and diffusion coefficients from trajectories.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trajectory` | string | Yes | Trajectory file (.xtc, .trr) |
| `topology` | string | Yes | Topology file |
| `selection` | string | Yes | Atom selection |

**Returns**: MSD data and diffusion coefficient

#### `analyze_energy_tool`

Analyze energies from `.edr` files.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `edr_file` | string | Yes | Energy file |
| `terms` | array | Yes | Energy terms to extract |

**Returns**: Energy time series and averages

### Configuration Tools

#### `get_water_model_info_tool`

Get detailed info for a water model.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `model_name` | string | Yes | Water model name |

**Returns**: Model parameters and usage notes

**Available Water Models**:
| Model | Description |
|-------|-------------|
| `spce` | SPC/E (recommended for IEMs) |
| `tip3p` | TIP3P |
| `tip4p` | TIP4P |
| `tip4pew` | TIP4P/Ew |
| `spc` | SPC |
| `tip5p` | TIP5P |

#### `list_available_water_models_tool`

List all configured water models.

**Returns**: Available models with recommendations

#### `get_current_config_tool`

Report current configuration and work directory.

**Returns**: Configuration details

#### `update_work_directory_tool`

Change the default work directory.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `new_directory` | string | Yes | New work directory path |

**Returns**: Confirmation

## Usage Examples

### Small AEM System from SMILES

```
Using your OHMind-GROMACS tools, start from this monomer SMILES: [SMILES].

1) Estimate ions per monomer and suggest an appropriate ion type and water model.
2) Build an oligomer, parameterize it, generate a real `.itp` file, and create 
   a small system (e.g. 10 chains, DP 25, reasonable water uptake).
3) Run a short MD simulation at 400 K and summarize key properties such as 
   density and qualitatively estimated conductivity.
```

### Focused MD Pipeline Control

```
I already have `system_initial.pdb` and `system.top`.

Use your GROMACS MCP tools to:
a) Build a simulation box
b) Generate NVT and NPT MDP files with 400 K and 1 bar
c) Run grompp and mdrun for a short production run
d) Analyze MSD and key energy terms

Return a human-readable summary of the MD setup and results.
```

### Water Model Selection

```
With your configuration tools, list available water models and recommend 
one for hydroxide-conducting AEMs.

Then update the MD work directory to a new folder under my project 
(e.g. `./simulations/aem_test`) and confirm the change.
```

### Temperature Sweep

```
Using your MD tools, design a small AEM system and run short test 
simulations at 300 K, 350 K, and 400 K.

Compare how water uptake and ionic conductivity change with temperature, 
and provide a brief discussion.
```

## Results Format

### Output Directory Structure

MD results are saved to `$MD_WORK_DIR/`:

```
$MD_WORK_DIR/
├── system_setup/
│   ├── polymer.pdb
│   ├── polymer.itp
│   └── system.top
├── em/
│   ├── em.mdp
│   ├── em.tpr
│   └── em.gro
├── nvt/
│   ├── nvt.mdp
│   ├── nvt.tpr
│   └── nvt.gro
├── npt/
│   ├── npt.mdp
│   ├── npt.tpr
│   └── npt.gro
├── production/
│   ├── md.mdp
│   ├── md.tpr
│   ├── md.xtc
│   ├── md.edr
│   └── md.gro
└── analysis/
    ├── msd.xvg
    └── energy.xvg
```

### Output File Types

| Extension | Contents |
|-----------|----------|
| `.gro` | GROMACS coordinate file |
| `.top` | Topology file |
| `.itp` | Include topology file |
| `.mdp` | MD parameter file |
| `.tpr` | Portable binary run input |
| `.xtc` | Compressed trajectory |
| `.trr` | Full precision trajectory |
| `.edr` | Energy file |
| `.xvg` | XY data (Grace format) |

## Troubleshooting

### Common Issues

#### GROMACS Not Found

```
Error: gmx command not found
```

**Solution**: Ensure GROMACS is on PATH:
```bash
source /path/to/gromacs/bin/GMXRC
```

#### AmberTools Not Found

```
Error: antechamber not found
```

**Solution**: Install AmberTools:
```bash
conda install -c conda-forge ambertools
```

#### PACKMOL Not Found

```
Error: packmol not found
```

**Solution**: Install PACKMOL:
```bash
conda install -c conda-forge packmol
```

#### Simulation Failed

```
Error: MD simulation failed
```

**Solutions**:
1. Check `.log` file for error messages
2. Verify topology is correct
3. Check for overlapping atoms
4. Reduce timestep

### Expensive Operations

The following tools require validation:

| Tool | Estimated Time |
|------|----------------|
| `run_complete_iem_workflow_tool` | 1-4 hours |
| `run_complete_md_simulation_tool` | 1-4 hours |
| `run_mdrun_tool` | Varies |

### Debug Mode

Run the server with verbose logging:

```bash
PYTHONPATH=/path/to/OHMind \
  MD_WORK_DIR=/OHMind_workspace/GROMACS \
  python -m OHMind_agent.MCP.GROMACS.server --transport stdio 2>&1 | tee gromacs_debug.log
```

## See Also

- [MCP Server Reference](./index.md) - Overview of all servers
- [MD Agent](../agents/md-agent.md) - Agent documentation
- [MD Simulations Tutorial](../tutorials/md-simulations.md) - Step-by-step guide
- [OHMD Module](../core-library/ohmd.md) - MD utilities

---
*Last updated: 2025-12-22 | OHMind v1.0.0*
