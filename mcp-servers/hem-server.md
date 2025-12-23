---
title: "OHMind-HEMDesign MCP Server"
description: "HEM optimization MCP server for PSO-based cation design"
category: "mcp-servers"
tags: ["hem", "pso", "optimization", "cation", "backbone"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# OHMind-HEMDesign MCP Server

> PSO-based optimization tools for Hydroxide Exchange Membrane (HEM) cation design and job management.

## Table of Contents

- [Overview](#overview)
- [Server Configuration](#server-configuration)
- [Tools Reference](#tools-reference)
- [Usage Examples](#usage-examples)
- [Results Format](#results-format)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The OHMind-HEMDesign MCP server provides 7 tools for HEM optimization using Particle Swarm Optimization (PSO) with a Junction Tree VAE. It enables design of optimal cation structures for specific polymer backbones.

### Server Details

| Property | Value |
|----------|-------|
| Server Name | `OHMind-HEMDesign` |
| Entry Point | `python -m OHMind_agent.MCP.HEMDesign.server` |
| Tool Count | 7 |
| Dependencies | RDKit, PyYAML, Pandas, OHMind core library |

### Capabilities

- List available polymer backbones
- List available cation families
- Validate optimization configurations
- Run PSO-based optimization
- Check optimization results
- Monitor running jobs
- Terminate jobs

## Server Configuration

### Starting the Server

```bash
# stdio transport (default)
python -m OHMind_agent.MCP.HEMDesign.server --transport stdio

# HTTP transport
python -m OHMind_agent.MCP.HEMDesign.server --transport streamable-http --port 8102
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `PYTHONPATH` | Path to OHMind project | Yes |
| `HEM_SAVE_PATH` | Results storage directory | Yes |
| `OHMind_workspace` | Base workspace path | Yes |

### mcp.json Configuration

```json
{
  "OHMind-HEMDesign": {
    "command": "python",
    "args": ["-m", "OHMind_agent.MCP.HEMDesign.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "HEM_SAVE_PATH": "/OHMind_workspace/HEM",
      "OHMind_workspace": "/OHMind_workspace"
    }
  }
}
```

### Required Files

The server requires these files in the `MCP/HEMDesign/` directory:

| File | Purpose |
|------|---------|
| `aem_backbones.yaml` | Backbone definitions and SMILES |
| `model.epoch-29` | Pre-trained VAE model weights |
| `vocab.txt` | Vocabulary for SMILES encoding |

## Tools Reference

### Discovery Tools

#### `ListBackbones`

List available polymer backbones for HEM design.

**Parameters**: None

**Returns**: List of backbones with identifiers and SMILES

**Available Backbones**:

| Identifier | Description |
|------------|-------------|
| `PBF_BB_1` | Polybenzofuran backbone 1 |
| `PBF_BB_2` | Polybenzofuran backbone 2 |
| `PP_BB_1` | Polyphenylene backbone 1 |
| `PP_BB_2` | Polyphenylene backbone 2 |
| `PP_BB_3` | Polyphenylene backbone 3 |
| `PX_BB_1` | Polyxylene backbone |
| `PAI_BB_1` | Polyarylimidazolium backbone |
| `PF_BB_1` | Polyfluorene backbone |
| `PPO_BB_1` | Polyphenylene oxide backbone 1 |
| `PPO_BB_2` | Polyphenylene oxide backbone 2 |
| `PPO_BB_3` | Polyphenylene oxide backbone 3 |

#### `ListCations`

List available cation families and initial SMILES templates.

**Parameters**: None

**Returns**: List of cation types with example structures

**Available Cation Families**:

| Family | Description |
|--------|-------------|
| `tetraalkylammonium` | Quaternary ammonium cations |
| `imidazolium` | Imidazolium-based cations |
| `benzimidazolium` | Benzimidazolium cations |
| `guanidinium` | Guanidinium cations |
| `piperidinium` | Piperidinium cations |
| `spiro_undecane` | Spirocyclic cations |

### Configuration Tools

#### `ValidateConfig`

Validate a prospective optimization configuration before running.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `backbone` | string | Yes | Backbone identifier (e.g., `PBF_BB_1`) |
| `cation_name` | string | Yes | Cation family name |
| `property` | string | Yes | Property mode: `multi`, `ec`, `ewu`, `esr` |

**Returns**: Validation result with any issues found

**Property Modes**:
| Mode | Description |
|------|-------------|
| `multi` | Multi-objective (EC, EWU, ESR combined) |
| `ec` | Electrical conductivity only |
| `ewu` | Equilibrium water uptake only |
| `esr` | Equivalent series resistance only |

### Optimization Tools

#### `HEMOptimizer`

⚠️ **EXPENSIVE OPERATION** - Requires user approval

Launch PSO-based optimization to design new cation structures.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `backbone` | string | Yes | Target backbone (e.g., `PBF_BB_1`) |
| `cation_name` | string | Yes | Cation family (e.g., `piperidinium`) |
| `property` | string | Yes | Optimization target mode |
| `num_part` | integer | No | Number of particles (default: 250) |
| `steps` | integer | No | Number of PSO steps (default: 5) |
| `save_path` | string | No | Results directory (default: `$HEM_SAVE_PATH`) |

**Returns**: Job status and results location

**Estimated Time**: 10-15 minutes

**Example**:
```json
{
  "backbone": "PBF_BB_1",
  "cation_name": "piperidinium",
  "property": "multi",
  "num_part": 250,
  "steps": 5
}
```

### Results Tools

#### `CheckStatus`

Check results from completed optimization runs.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `save_path` | string | No | Workspace directory |
| `backbone` | string | Yes | Backbone used |
| `cation_name` | string | Yes | Cation type used |

**Returns**: Top solutions from CSV logs with SMILES and scores

### Monitoring Tools

#### `ShowLogs`

Stream recent optimization log lines for monitoring.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `backbone` | string | Yes | Backbone identifier |
| `cation_name` | string | Yes | Cation type |
| `lines` | integer | No | Number of lines to show (default: 50) |

**Returns**: Recent log content

#### `KillJob`

List running optimization jobs or terminate one.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `backbone` | string | No | Filter by backbone |
| `cation_name` | string | No | Filter by cation |
| `job_id` | string | No | Specific job to kill |

**Returns**: Job status or termination confirmation

## Usage Examples

### Discover Design Space

```
Using your OHMind-HEMDesign tools, list all available backbones and cation 
types, then recommend 2-3 promising backbone-cation combinations for 
alkaline-stable AEMs. Summarize why these combinations are interesting.
```

### Validate and Start Optimization

```
First validate a multi-objective optimization for backbone `PBF_BB_1` with 
`piperidinium` cations and property mode `multi`.

If the configuration is valid, start a PSO optimization with moderate 
settings (e.g. ~250 particles, ~5-10 steps), saving results to a fresh 
directory.

Explain what metrics you are optimizing and how you will interpret the 
final Pareto front.
```

### Monitor Running Job

```
Using your HEMDesign job-management tools, find any currently running 
optimizations. Show me a short snippet of the latest log lines for each job, 
and if any look clearly stalled or failing, ask me whether to kill them.
```

### Check Results

```
Show me the results from the PBF_BB_1 piperidinium optimization. 
Display the top 5 candidates with their SMILES and property scores.
```

### Compare Backbones

```
For backbones PBF_BB_1 and PP_BB_1, design the best tetraalkylammonium 
cations using your HEM optimization tools. Compare the top candidates 
for each backbone in terms of alkaline stability, ESR, and conductivity.
```

## Results Format

### Output Files

Optimization results are saved to `$HEM_SAVE_PATH/`:

```
$HEM_SAVE_PATH/
├── best_solutions_<BACKBONE>_<CATION>.csv
├── best_fitness_history_<BACKBONE>_<CATION>.csv
└── optimization_<BACKBONE>_<CATION>.log
```

### CSV Output Format

The `best_solutions_*.csv` file contains:

| Column | Description |
|--------|-------------|
| `smiles` | Optimized cation SMILES |
| `ec_score` | Electrical conductivity score |
| `ewu_score` | Water uptake score |
| `esr_score` | ESR score |
| `fitness` | Combined fitness value |

### Fitness History

The `best_fitness_history_*.csv` tracks optimization progress:

| Column | Description |
|--------|-------------|
| `step` | PSO iteration number |
| `max_fitness` | Best fitness in population |
| `min_fitness` | Worst fitness in population |
| `mean_fitness` | Average fitness |

### Log File

The `optimization_*.log` contains:

- PSO iteration progress
- Particle positions and velocities
- Fitness evaluations
- Convergence information

## Troubleshooting

### Common Issues

#### OHMind Library Not Found

```
ImportError: No module named 'OHMind.OHPSO'
```

**Solution**: Ensure PYTHONPATH includes the OHMind project root:
```bash
export PYTHONPATH=/path/to/OHMind:$PYTHONPATH
```

#### Model Files Missing

```
FileNotFoundError: model.epoch-29 not found
```

**Solution**: Ensure model files are in `MCP/HEMDesign/`:
- `aem_backbones.yaml`
- `model.epoch-29`
- `vocab.txt`

#### HEM_SAVE_PATH Not Set

```
Error: HEM_SAVE_PATH environment variable not set
```

**Solution**: Set the environment variable:
```bash
export HEM_SAVE_PATH=/OHMind_workspace/HEM
```

#### Optimization Timeout

Long-running optimizations may appear to hang.

**Solution**: 
1. Use `ShowLogs` to check progress
2. Increase `steps` for more thorough search
3. Reduce `num_part` for faster iterations

### Debug Mode

Run the server with verbose logging:

```bash
PYTHONPATH=/path/to/OHMind \
  HEM_SAVE_PATH=/OHMind_workspace/HEM \
  python -m OHMind_agent.MCP.HEMDesign.server --transport stdio 2>&1 | tee hem_debug.log
```

## See Also

- [MCP Server Reference](./index.md) - Overview of all servers
- [HEM Agent](../agents/hem-agent.md) - Agent documentation
- [HEM Optimization Tutorial](../tutorials/hem-optimization.md) - Step-by-step guide
- [OHPSO Module](../core-library/ohpso.md) - PSO implementation details

---
*Last updated: 2025-12-22 | OHMind v1.0.0*
