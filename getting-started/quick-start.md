---
title: "Quick Start Guide"
description: "Get OHMind running in 10 minutes with this quick start guide"
category: "getting-started"
tags: ["installation", "quick-start", "setup"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: Getting Started
nav_order: 1
---

# Quick Start Guide

> Get OHMind up and running in under 10 minutes

This guide provides the fastest path to a working OHMind installation. For detailed installation instructions and troubleshooting, see the [full installation guide](./installation.md).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Verification](#verification)
- [Hello World Example](#hello-world-example)
- [Next Steps](#next-steps)

## Prerequisites

Before you begin, ensure you have:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Linux | Ubuntu-like | `uname -a` |
| Conda | Anaconda/Miniconda | `conda --version` |
| Python | 3.10+ | `python --version` |
| GPU + CUDA | Recommended | `nvidia-smi` |

### Quick Prerequisite Check

```bash
# Run these commands to verify your system is ready
conda --version          # Should show conda version
python --version         # Should show Python 3.10+
nvidia-smi              # Optional: shows GPU info if available
```

## Installation

### Step 1: Clone and Navigate

```bash
# Clone the repository (if not already done)
git clone <repository-url> OHMind
cd OHMind
```

### Step 2: Create Conda Environment

```bash
# Create the OHMind environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate OHMind
```

This installs all Python dependencies including:
- LangChain + LangGraph for agent orchestration
- PyTorch, DGL for VAE models
- RDKit for cheminformatics
- FastAPI, Chainlit for web interfaces
- Textual for TUI
- langchain-mcp-adapters for MCP integration

### Step 3: Configure Environment Variables

Create or edit the `.env` file in the project root:

```bash
# Minimal configuration
OHMind_workspace=/path/to/your/workspace

# LLM Configuration (OpenAI-compatible)
OPENAI_COMPATIBLE_API_KEY=your-api-key
OPENAI_COMPATIBLE_BASE_URL=https://api.openai.com/v1
OPENAI_COMPATIBLE_MODEL=gpt-4
```

### Step 4: Create Workspace Directories

```bash
# Create the workspace structure
mkdir -p $OHMind_workspace/{HEM,QM,MD,Multiwfn}
```

## Verification

### Verify Installation

Run this command to verify your installation:

```bash
# Activate environment and check imports
conda activate OHMind
python -c "
from OHMind.OHVAE import JTPropVAE
from OHMind.OHPSO import BasePSOptimizer
from OHMind.OHScore import metrics
print('✓ OHMind core library loaded successfully')
"
```

Expected output:
```
✓ OHMind core library loaded successfully
```

### Verify MCP Servers

Test that MCP servers can start:

```bash
# Test Chem server (should show available tools)
python -m OHMind_agent.MCP.Chem.server --help
```

## Hello World Example

Let's run a simple example to verify everything works.

### Option A: Using the CLI (Recommended for Quick Test)

```bash
# Start the CLI application
./start_OHMind_cli.sh
```

Once the CLI starts, try this prompt:

```
What is the molecular weight of aspirin (acetylsalicylic acid)?
```

The system should:
1. Convert the name to SMILES
2. Calculate the molecular weight
3. Return the result (~180.16 g/mol)

### Option B: Using the Web UI

```bash
# Start the backend and UI
./start_apps.sh
```

Then open `http://localhost:8000` in your browser and log in with:
- Username: `admin`
- Password: `admin`

Try the same prompt in the chat interface.

### Option C: Using Python Directly

```python
from OHMind.OHVAE import JTPropVAE
from OHMind.OHPSO.util import smiles_to_mol
from rdkit.Chem import Descriptors

# Simple molecular weight calculation
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
mol = smiles_to_mol(smiles)
mw = Descriptors.MolWt(mol)
print(f"Molecular weight of aspirin: {mw:.2f} g/mol")
```

Expected output:
```
Molecular weight of aspirin: 180.16 g/mol
```

## Quick Checklist

Use this checklist to ensure your installation is complete:

- [ ] Conda environment created: `conda env create -f environment.yml`
- [ ] Environment activated: `conda activate OHMind`
- [ ] Workspace directory exists and is writable
- [ ] `.env` file configured with LLM API keys
- [ ] Verification script runs without errors

### Optional External Tools

For full functionality, you may also need:

- [ ] **ORCA** installed and `OHMind_ORCA` environment variable set
- [ ] **Multiwfn** installed and `MULTIWFN_PATH` set
- [ ] **GROMACS** available on PATH
- [ ] **Qdrant** running for RAG functionality

See the [full installation guide](./installation.md) for details on setting up external tools.

## Next Steps

Now that OHMind is running, explore these resources:

| Goal | Resource |
|------|----------|
| Learn the interface | [First Steps](./first-steps.md) |
| Understand the architecture | [Architecture Overview](../architecture/overview.md) |
| Run HEM optimization | [HEM Optimization Tutorial](../tutorials/hem-optimization.md) |
| Configure MCP servers | [MCP Configuration](../configuration/mcp-config.md) |
| Troubleshoot issues | [Troubleshooting Guide](../troubleshooting/index.md) |

## See Also

- [Installation Guide](./installation.md) - Detailed installation instructions
- [First Steps](./first-steps.md) - Your first interaction with OHMind
- [Configuration Overview](../configuration/index.md) - All configuration options

---

*Last updated: 2025-12-22 | OHMind v1.0.0*
