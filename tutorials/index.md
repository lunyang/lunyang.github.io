---
title: "Tutorials"
description: "Step-by-step tutorials for common OHMind workflows including HEM optimization, QM calculations, MD simulations, and literature search"
category: "tutorials"
tags: ["tutorials", "guides", "workflows", "examples"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# Tutorials

> Step-by-step guides for common OHMind workflows, from HEM optimization to multi-step computational chemistry pipelines.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Tutorial List](#tutorial-list)
- [Difficulty Levels](#difficulty-levels)
- [Getting Help](#getting-help)
- [See Also](#see-also)

## Overview

These tutorials provide hands-on guidance for using OHMind's multi-agent system to perform computational chemistry tasks. Each tutorial includes:

- **Clear objectives** - What you'll accomplish
- **Step-by-step instructions** - Detailed prompts and commands
- **Expected outputs** - What results to expect
- **Result interpretation** - How to understand the outputs
- **Troubleshooting tips** - Common issues and solutions

## Prerequisites

Before starting any tutorial, ensure you have:

### System Requirements

- [ ] OHMind installed and configured ([Installation Guide](../getting-started/installation.md))
- [ ] Conda environment activated (`conda activate OHMind`)
- [ ] Workspace directory set up ([Workspace Setup](../configuration/workspace-setup.md))
- [ ] LLM provider configured ([LLM Providers](../configuration/llm-providers.md))

### For Specific Tutorials

| Tutorial | Additional Requirements |
|----------|------------------------|
| HEM Optimization | None (uses built-in models) |
| QM Calculations | ORCA installed, `OHMind_ORCA` configured |
| MD Simulations | GROMACS installed and on PATH |
| Wavefunction Analysis | Multiwfn installed, `MULTIWFN_PATH` configured |
| Literature Search | Qdrant configured, documents ingested |

### Starting the Interface

Choose your preferred interface:

**Terminal UI (CLI):**
```bash
cd OHMind
./start_OHMind_cli.sh
```

**Web UI:**
```bash
cd OHMind
./start_apps.sh
# Open http://localhost:8000
```

## Tutorial List

### Beginner Tutorials

| Tutorial | Time | Description |
|----------|------|-------------|
| [HEM Optimization](./hem-optimization.md) | 30 min | Design new cations using PSO optimization |
| [Literature Search](./literature-search.md) | 15 min | Search scientific literature with RAG |

### Intermediate Tutorials

| Tutorial | Time | Description |
|----------|------|-------------|
| [QM Calculations](./qm-calculations.md) | 45 min | Run quantum chemistry calculations with ORCA |
| [MD Simulations](./md-simulations.md) | 60 min | Perform molecular dynamics with GROMACS |

### Advanced Tutorials

| Tutorial | Time | Description |
|----------|------|-------------|
| [Multi-Step Workflows](./multi-step-workflows.md) | 90 min | Combine multiple agents for complex tasks |

## Difficulty Levels

### 🟢 Beginner

- No external software required (except LLM)
- Single-agent workflows
- Quick results (< 30 minutes)
- Minimal configuration

**Recommended starting point:** [HEM Optimization](./hem-optimization.md)

### 🟡 Intermediate

- External software required (ORCA, GROMACS)
- Single or dual-agent workflows
- Moderate computation time
- Some configuration needed

**Recommended:** [QM Calculations](./qm-calculations.md)

### 🔴 Advanced

- Multiple external tools
- Multi-agent coordination
- Complex workflows
- Full system configuration

**Recommended:** [Multi-Step Workflows](./multi-step-workflows.md)

## Tutorial Workflow

Each tutorial follows this general structure:

```mermaid
graph LR
    A[Setup] --> B[Prompt]
    B --> C[Agent Processing]
    C --> D[Results]
    D --> E[Interpretation]
    E --> F[Next Steps]
```

### 1. Setup
- Verify prerequisites
- Start the interface
- Select appropriate chat profile

### 2. Prompt
- Copy the provided prompt
- Modify parameters as needed
- Submit to the agent

### 3. Agent Processing
- Watch agent activity
- Monitor tool calls
- Wait for completion

### 4. Results
- Review generated files
- Check output locations
- Verify completion

### 5. Interpretation
- Understand the results
- Compare with expected outputs
- Identify key findings

### 6. Next Steps
- Suggested follow-up tasks
- Related tutorials
- Advanced variations

## Quick Start Examples

### HEM Optimization (Beginner)

```
Design new piperidinium-based cations for backbone PBF_BB_1 
optimizing multi-objective HEM performance. Run PSO with 
200 particles for 5 steps.
```

**Expected time:** 5-10 minutes  
**Output:** CSV files with top candidates in `$OHMind_workspace/HEM/`

### QM Property Calculation (Intermediate)

```
For the cation SMILES "C[N+]1(C)CCCCC1", run a QM calculation 
to estimate LUMO energy and alkaline stability descriptors.
```

**Expected time:** 10-30 minutes  
**Output:** Optimized geometry and properties in `$OHMind_workspace/ORCA/`

### Literature Search (Beginner)

```
Search for recent literature on cation designs for hydroxide 
exchange membranes with high alkaline stability. Summarize 
the key structural motifs.
```

**Expected time:** 1-2 minutes  
**Output:** Summary with citations

## Getting Help

### During Tutorials

If you encounter issues:

1. **Check prerequisites** - Ensure all requirements are met
2. **Review error messages** - Agent responses include diagnostic info
3. **Check workspace** - Verify files are being created
4. **Consult troubleshooting** - See [Troubleshooting Guide](../troubleshooting/index.md)

### Common Issues

| Issue | Solution |
|-------|----------|
| "Tool not found" | Check MCP server configuration |
| "Permission denied" | Verify workspace permissions |
| "Timeout" | Increase timeout in mcp.json |
| "Model not found" | Check LLM configuration |

### Getting Support

- Check the [Troubleshooting Guide](../troubleshooting/index.md)
- Review [Configuration](../configuration/index.md) settings
- Consult [Agent Reference](../agents/index.md) for capabilities

## See Also

- [Getting Started](../getting-started/quick-start.md) - Initial setup
- [Agent Reference](../agents/index.md) - Agent capabilities
- [MCP Servers](../mcp-servers/index.md) - Available tools
- [Configuration](../configuration/index.md) - System configuration

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
