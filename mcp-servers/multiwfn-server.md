---
title: "OHMind-Multiwfn MCP Server"
description: "Wavefunction analysis MCP server using Multiwfn"
category: "mcp-servers"
tags: ["multiwfn", "wavefunction", "orbitals", "electronic-structure"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: MCP Server Reference
nav_order: 4
---

# OHMind-Multiwfn MCP Server

> Wavefunction analysis and electronic structure post-processing tools using Multiwfn.

## Table of Contents

- [Overview](#overview)
- [Server Configuration](#server-configuration)
- [Tools Reference](#tools-reference)
- [Usage Examples](#usage-examples)
- [Results Format](#results-format)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The OHMind-Multiwfn MCP server provides 16 tools for wavefunction analysis and electronic structure post-processing. It analyzes ORCA output files to extract orbital energies, electron density information, population analysis, and generates visualizations.

### Server Details

| Property | Value |
|----------|-------|
| Server Name | `OHMind-Multiwfn` |
| Entry Point | `python -m OHMind_agent.MCP.Multiwfn.server` |
| Tool Count | 16 |
| Dependencies | Multiwfn executable |

### Capabilities

- Orbital analysis (HOMO/LUMO energies, compositions)
- Population analysis (Mulliken, Hirshfeld, ADCH, RESP)
- Electron density analysis (AIM, ELF, LOL)
- Weak interaction analysis (NCI, RDG, IGMH)
- Bond analysis and bond orders
- Aromaticity analysis (NICS)
- Spectrum simulation (UV-Vis, IR, NMR)
- Orbital visualization (2D/3D)

## Server Configuration

### Starting the Server

```bash
# stdio transport (default)
python -m OHMind_agent.MCP.Multiwfn.server --transport stdio

# HTTP transport
python -m OHMind_agent.MCP.Multiwfn.server --transport streamable-http --port 8104
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `PYTHONPATH` | Path to OHMind project | Yes |
| `MULTIWFN_PATH` | Path to Multiwfn executable | Yes |
| `MULTIWFN_WORK_DIR` | Working directory | Yes |
| `QM_WORK_DIR` | QM results directory | For finding ORCA files |

### mcp.json Configuration

```json
{
  "OHMind-Multiwfn": {
    "command": "python",
    "args": ["-m", "OHMind_agent.MCP.Multiwfn.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "MULTIWFN_PATH": "/path/to/Multiwfn",
      "MULTIWFN_WORK_DIR": "/OHMind_workspace/Multiwfn",
      "QM_WORK_DIR": "/OHMind_workspace/ORCA"
    }
  }
}
```

## Tools Reference

### Core Analysis Tools

#### `AnalyzeWavefunction`

Basic wavefunction analysis for a given input file.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file (fchk/wfn/gbw/out) |

**Returns**: Wavefunction diagnostics and summary

#### `OrbitalAnalysis`

Analyze HOMO, LUMO, and other molecular orbitals.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to `.out` or `.gbw` file, OR results_directory |
| `orbital_number` | string | No | `"HOMO"`, `"LUMO"`, `"HOMO-1"`, `"LUMO+1"`, or integer |
| `composition_method` | string | No | `"Mulliken"`, `"Hirshfeld"`, `"NAO"`, `"Becke"` |

**Returns**: Orbital energies, compositions, and properties

**Example**:
```json
{
  "input_file": "/OHMind_workspace/ORCA/results",
  "orbital_number": "LUMO",
  "composition_method": "Mulliken"
}
```

#### `PopulationAnalysis`

Calculate atomic charges using various methods.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `methods` | array | No | Charge methods to use |

**Available Methods**:
| Method | Description |
|--------|-------------|
| `mulliken` | Mulliken population analysis |
| `hirshfeld` | Hirshfeld charges |
| `adch` | ADCH charges |
| `resp` | RESP charges |
| `cm5` | CM5 charges |
| `mbis` | MBIS charges |

**Returns**: Charges per atom for each method

#### `ElectronDensityAnalysis`

Analyze electron density using various methods.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `analysis_type` | string | Yes | Analysis type |

**Analysis Types**:
| Type | Description |
|------|-------------|
| `aim` | Atoms in Molecules (Bader) analysis |
| `elf` | Electron Localization Function |
| `lol` | Localized Orbital Locator |
| `laplacian` | Laplacian of electron density |

**Returns**: Electron density analysis results

#### `BondAnalysis`

Analyze chemical bonds and bond orders.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `bond_order_type` | string | No | `"mayer"`, `"wiberg"`, `"fuzzy"` |

**Returns**: Bond orders and strength descriptors

### Interaction Analysis Tools

#### `WeakInteractionAnalysis`

Analyze noncovalent interactions.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `analysis_type` | string | Yes | Analysis type |

**Analysis Types**:
| Type | Description |
|------|-------------|
| `rdg` | Reduced Density Gradient |
| `nci` | Non-Covalent Interaction |
| `igmh` | Independent Gradient Model based on Hirshfeld |
| `iri` | Interaction Region Indicator |

**Returns**: Weak interaction analysis results

#### `AromaticityAnalysis`

Calculate aromaticity indices.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `ring_atoms` | array | Yes | Atom indices defining the ring |

**Returns**: NICS values and related aromaticity measures

#### `EnergyDecomposition`

Energy decomposition analysis.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `method` | string | No | `"lmo-eda"`, `"sapt"` |

**Returns**: Energy decomposition results

### Spectrum Simulation Tools

#### `SimulateSpectrum`

Simulate various spectra from computed properties.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction/output file |
| `spectrum_type` | string | Yes | Spectrum type |
| `broadening` | float | No | Peak broadening parameter |

**Spectrum Types**:
| Type | Description |
|------|-------------|
| `uv-vis` | UV-Visible absorption |
| `ir` | Infrared |
| `raman` | Raman |
| `nmr` | NMR |
| `ecd` | Electronic Circular Dichroism |
| `vcd` | Vibrational Circular Dichroism |

**Returns**: Simulated spectrum data

### Visualization Tools

#### `GenerateCubeFiles`

Generate cube files for densities and orbitals.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `property` | string | Yes | Property to generate |
| `orbital_number` | integer | No | Orbital index for orbital cubes |

**Properties**:
- `density` - Electron density
- `orbital` - Molecular orbital
- `elf` - Electron Localization Function
- `lol` - Localized Orbital Locator

**Returns**: Path to generated cube file

#### `VisualizeOrbitals`

High-level orbital visualization orchestration.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |
| `orbitals` | array | Yes | Orbital numbers to visualize |
| `output_format` | string | No | Output format (`"png"`, `"cube"`) |

**Returns**: Paths to visualization files

#### `QuickVisualizeHOMOLUMO`

Convenience tool to quickly visualize HOMO/LUMO.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |

**Returns**: HOMO and LUMO visualization files

#### `RenderOrbitals2D`

2D slice plotting of orbitals/densities.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cube_file` | string | Yes | Path to cube file |
| `plane` | string | No | Slice plane (`"xy"`, `"xz"`, `"yz"`) |
| `slice_position` | float | No | Position along perpendicular axis |

**Returns**: 2D plot image

#### `RenderOrbitals3D`

3D orbital rendering with VMD/Tachyon style.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cube_file` | string | Yes | Path to cube file |
| `isovalue` | float | No | Isosurface value |
| `style` | string | No | Rendering style |

**Returns**: 3D render image

### MD Analysis Tools

#### `MDAnalysis`

Post-processing of MD trajectories.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trajectory` | string | Yes | Path to trajectory file |
| `topology` | string | Yes | Path to topology file |
| `analysis_type` | string | Yes | `"rdf"`, `"coordination"`, `"hbond"` |

**Returns**: MD analysis results

### Advanced Analysis Tools

#### `AdNDPAnalysis`

Adaptive Natural Density Partitioning analysis.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_file` | string | Yes | Path to wavefunction file |

**Returns**: AdNDP bonding analysis

## Usage Examples

### Charge and Reactive Hot-Spot Analysis

```
For the optimized cation geometry from my QM calculation (assume I have 
already generated a suitable wavefunction file), use your Multiwfn tools 
to analyze charge distribution and identify likely degradation hot spots 
under alkaline conditions.

Report which atoms or fragments are most positively charged or otherwise reactive.
```

### Orbital Visualization

```
Starting from the wavefunction of a candidate cation, generate HOMO and 
LUMO visualizations (both 2D slices and 3D renders).

Describe where the LUMO is localized and what that suggests about 
degradation pathways.
```

### HOMO/LUMO Energy Analysis

```
For the ORCA calculation results in /OHMind_workspace/ORCA, analyze the 
HOMO and LUMO energies using Mulliken composition analysis.

Report the orbital energies in eV and explain what the HOMO-LUMO gap 
implies for the molecule's reactivity.
```

### Spectrum Simulation

```
Take a representative structure from an MD snapshot of my membrane system 
and use Multiwfn to simulate an approximate UV-Vis or IR spectrum, 
highlighting features that correlate with specific structural motifs.
```

### Comprehensive Electronic Analysis

```
Using your Multiwfn tools, perform a comprehensive electronic analysis 
of this cation:

1) Calculate Hirshfeld and ADCH charges
2) Analyze the LUMO orbital composition
3) Identify any weak interactions using NCI analysis
4) Generate a 3D visualization of the LUMO

Summarize which parts of the molecule are most vulnerable to nucleophilic attack.
```

## Results Format

### Output Directory Structure

Multiwfn results are saved to `$MULTIWFN_WORK_DIR/`:

```
$MULTIWFN_WORK_DIR/
├── <job-name>/
│   ├── input.*           # Input files
│   ├── analysis.log      # Analysis log
│   ├── *.dat             # Data files
│   ├── *.cube            # Cube files
│   └── *.png             # Visualization images
```

### Output File Types

| Extension | Contents |
|-----------|----------|
| `.dat` | Numerical data (charges, energies) |
| `.cube` | 3D volumetric data |
| `.png` | Visualization images |
| `.log` | Analysis log |

### Visualization Output

Cube files can be visualized with external tools:
- VMD (Visual Molecular Dynamics)
- PyMOL
- Avogadro
- Custom Python scripts with matplotlib

## Troubleshooting

### Common Issues

#### Multiwfn Not Found

```
Error: Multiwfn executable not found
```

**Solution**: Set the Multiwfn path:
```bash
export MULTIWFN_PATH=/path/to/Multiwfn
```

#### Input File Not Found

```
Error: Could not find wavefunction file
```

**Solutions**:
1. Check if ORCA calculation completed successfully
2. Verify `QM_WORK_DIR` is set correctly
3. Use full path to the `.out` or `.gbw` file

#### Analysis Failed

```
Error: Multiwfn analysis failed
```

**Solutions**:
1. Check Multiwfn log for error messages
2. Verify input file format is supported
3. Ensure sufficient disk space

#### Visualization Error

```
Error: Could not generate visualization
```

**Solutions**:
1. Check if cube file was generated
2. Verify matplotlib is installed
3. Check display settings for 3D rendering

### Supported Input Formats

| Format | Extension | Source |
|--------|-----------|--------|
| ORCA output | `.out` | ORCA calculation |
| ORCA wavefunction | `.gbw` | ORCA calculation |
| Gaussian fchk | `.fchk` | Gaussian |
| Molden | `.molden` | Various |
| WFN/WFX | `.wfn`, `.wfx` | Various |

### Debug Mode

Run the server with verbose logging:

```bash
PYTHONPATH=/path/to/OHMind \
  MULTIWFN_PATH=/path/to/Multiwfn \
  MULTIWFN_WORK_DIR=/OHMind_workspace/Multiwfn \
  python -m OHMind_agent.MCP.Multiwfn.server --transport stdio 2>&1 | tee multiwfn_debug.log
```

## See Also

- [MCP Server Reference](./index.md) - Overview of all servers
- [Multiwfn Agent](../agents/multiwfn-agent.md) - Agent documentation
- [ORCA Server](./orca-server.md) - For running calculations
- [QM Calculations Tutorial](../tutorials/qm-calculations.md) - Step-by-step guide

---
*Last updated: 2025-12-22 | OHMind v1.0.0*
