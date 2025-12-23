---
title: "Installation Guide"
description: "Detailed installation instructions for OHMind on all supported platforms"
category: "getting-started"
tags: ["installation", "setup", "configuration", "external-software"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: Getting Started
nav_order: 2
---

# Installation Guide

> Complete installation instructions for OHMind and all external dependencies

This guide provides detailed installation instructions for OHMind, including all optional external software for full functionality.

## Table of Contents

- [System Requirements](#system-requirements)
- [Core Installation](#core-installation)
- [External Software Setup](#external-software-setup)
- [Environment Configuration](#environment-configuration)
- [Workspace Setup](#workspace-setup)
- [Verification](#verification)
- [Platform-Specific Notes](#platform-specific-notes)

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Linux (Ubuntu 20.04+ recommended) |
| Python | 3.10 or higher |
| RAM | 16 GB minimum, 32 GB recommended |
| Storage | 50 GB free space |
| Package Manager | Conda (Anaconda or Miniconda) |

### Recommended Requirements

| Component | Recommendation |
|-----------|----------------|
| GPU | NVIDIA GPU with CUDA 11.8+ |
| VRAM | 8 GB+ for VAE models |
| CPU | 8+ cores for MD simulations |
| Storage | SSD for workspace directory |

### Software Dependencies

OHMind integrates with several external computational chemistry packages:

| Software | Purpose | Required |
|----------|---------|----------|
| ORCA | Quantum chemistry calculations | Optional |
| GROMACS | Molecular dynamics simulations | Optional |
| Multiwfn | Wavefunction analysis | Optional |
| Qdrant | Vector database for RAG | Optional |
| PostgreSQL | Web UI persistence | Optional (UI only) |
| MinIO | File storage for UI | Optional (UI only) |

## Core Installation

### Step 1: Install Conda

If you don't have Conda installed:

```bash
# Download Miniconda (recommended)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh

# Restart shell or source
source ~/.bashrc
```

### Step 2: Clone the Repository

```bash
git clone <repository-url> OHMind
cd OHMind
```

### Step 3: Create the Conda Environment

The `environment.yml` file contains all Python dependencies:

```bash
# Create environment (this may take 10-15 minutes)
conda env create -f environment.yml

# Activate the environment
conda activate OHMind
```

#### What Gets Installed

The environment includes:

**Core ML/AI Libraries:**
- PyTorch with CUDA support
- DGL (Deep Graph Library)
- LangChain + LangGraph
- Transformers

**Chemistry Libraries:**
- RDKit for cheminformatics
- OpenBabel for format conversion
- ASE for atomic simulations

**Web/UI Libraries:**
- FastAPI for backend
- Chainlit for web UI
- Textual for TUI

**MCP Integration:**
- langchain-mcp-adapters
- FastMCP

### Step 4: Verify Core Installation

```bash
# Test that core imports work
python -c "
import torch
import rdkit
from langchain_core.messages import HumanMessage
from OHMind.OHVAE import JTPropVAE
print('✓ All core dependencies loaded')
print(f'  PyTorch: {torch.__version__}')
print(f'  CUDA available: {torch.cuda.is_available()}')
"
```

## External Software Setup

### ORCA (Quantum Chemistry)

ORCA is required for QM calculations (geometry optimization, frequencies, etc.).

#### Installation

1. Register and download from [ORCA Forum](https://orcaforum.kofo.mpg.de/app.php/portal)
2. Extract to a permanent location:

```bash
# Example installation
tar -xf orca_5_0_4_linux_x86-64_shared_openmpi411.tar.xz
sudo mv orca_5_0_4_linux_x86-64_shared_openmpi411 /opt/orca
```

3. Set environment variables:

```bash
# Add to ~/.bashrc or .env
export OHMind_ORCA=/opt/orca/orca
export OHMind_MPI=/opt/orca  # MPI binaries location
export PATH=$PATH:/opt/orca
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/orca
```

#### Verification

```bash
# Test ORCA installation
$OHMind_ORCA --version
```

### GROMACS (Molecular Dynamics)

GROMACS is required for MD simulations.

#### Installation via Conda

```bash
# Easiest method - install via conda
conda install -c conda-forge gromacs
```

#### Installation from Source

For better performance, compile from source:

```bash
# Download and extract
wget https://ftp.gromacs.org/gromacs/gromacs-2023.3.tar.gz
tar -xzf gromacs-2023.3.tar.gz
cd gromacs-2023.3

# Build with GPU support
mkdir build && cd build
cmake .. -DGMX_BUILD_OWN_FFTW=ON -DGMX_GPU=CUDA
make -j$(nproc)
sudo make install

# Source the GROMACS environment
source /usr/local/gromacs/bin/GMXRC
```

#### Verification

```bash
gmx --version
```

### Multiwfn (Wavefunction Analysis)

Multiwfn provides detailed electronic structure analysis.

#### Installation

1. Download from [Multiwfn website](http://sobereva.com/multiwfn/)
2. Extract and set permissions:

```bash
tar -xf Multiwfn_3.8_dev_bin_Linux.tar.gz
chmod +x Multiwfn_3.8_dev_bin_Linux/Multiwfn
sudo mv Multiwfn_3.8_dev_bin_Linux /opt/multiwfn
```

3. Set environment variable:

```bash
export MULTIWFN_PATH=/opt/multiwfn/Multiwfn
```

#### Verification

```bash
$MULTIWFN_PATH <<< "q"
```

### Qdrant (Vector Database for RAG)

Qdrant enables literature search functionality.

#### Using Docker (Recommended)

```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

#### Using Binary

```bash
# Download and run
wget https://github.com/qdrant/qdrant/releases/download/v1.7.4/qdrant-x86_64-unknown-linux-gnu.tar.gz
tar -xzf qdrant-x86_64-unknown-linux-gnu.tar.gz
./qdrant
```

#### Configuration

Set in `.env`:

```bash
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Optional, for secured instances
```

## Environment Configuration

### Main Configuration File (.env)

Create a `.env` file in the project root:

```bash
# ===========================================
# OHMind Environment Configuration
# ===========================================

# --- LLM Configuration ---
OPENAI_COMPATIBLE_API_KEY=your-api-key-here
OPENAI_COMPATIBLE_BASE_URL=https://api.openai.com/v1
OPENAI_COMPATIBLE_MODEL=gpt-4

# --- Workspace Configuration ---
OHMind_workspace=/path/to/workspace
HEM_SAVE_PATH=${OHMind_workspace}/HEM
QM_WORK_DIR=${OHMind_workspace}/QM
MD_WORK_DIR=${OHMind_workspace}/MD
MULTIWFN_WORK_DIR=${OHMind_workspace}/Multiwfn
WORKSPACE_ROOT=${OHMind_workspace}

# --- External Software Paths ---
OHMind_ORCA=/opt/orca/orca
OHMind_MPI=/opt/orca
MULTIWFN_PATH=/opt/multiwfn/Multiwfn

# --- MCP Configuration ---
MCP_CONFIG_PATH=/path/to/OHMind/mcp.json

# --- RAG Configuration ---
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# --- Web Search ---
TAVILY_API_KEY=your-tavily-key  # Optional, for web search
```

### MCP Configuration (mcp.json)

The `mcp.json` file configures MCP server connections. A default configuration is provided in the project root.

See [MCP Configuration](../configuration/mcp-config.md) for detailed configuration options.

## Workspace Setup

### Directory Structure

OHMind uses a unified workspace for all computational outputs:

```
OHMind_workspace/
├── HEM/        # PSO/HEMDesign optimization results
├── QM/         # ORCA QM calculations
├── MD/         # GROMACS MD simulations
└── Multiwfn/   # Wavefunction analysis outputs
```

### Creating the Workspace

```bash
# Set workspace location
export OHMind_workspace=/path/to/your/workspace

# Create directory structure
mkdir -p "$OHMind_workspace"/{HEM,QM,MD,Multiwfn}

# Ensure proper permissions
chmod -R u+rwx "$OHMind_workspace"
```

### Automatic Workspace Setup

The `start_apps.sh` script automatically creates workspace directories if they don't exist:

```bash
# This will create workspace with default settings
./start_apps.sh
```

## Verification

### Complete Installation Check

Run this comprehensive verification script:

```bash
#!/bin/bash
echo "=== OHMind Installation Verification ==="

# Check Conda environment
echo -n "Conda environment: "
if conda info --envs | grep -q "OHMind"; then
    echo "✓ Found"
else
    echo "✗ Not found"
fi

# Check Python imports
echo -n "Core Python imports: "
python -c "from OHMind.OHVAE import JTPropVAE; from OHMind.OHPSO import BasePSOptimizer" 2>/dev/null && echo "✓ OK" || echo "✗ Failed"

# Check ORCA
echo -n "ORCA: "
if [ -n "$OHMind_ORCA" ] && [ -x "$OHMind_ORCA" ]; then
    echo "✓ Found at $OHMind_ORCA"
else
    echo "○ Not configured (optional)"
fi

# Check GROMACS
echo -n "GROMACS: "
if command -v gmx &> /dev/null; then
    echo "✓ Found"
else
    echo "○ Not found (optional)"
fi

# Check Multiwfn
echo -n "Multiwfn: "
if [ -n "$MULTIWFN_PATH" ] && [ -x "$MULTIWFN_PATH" ]; then
    echo "✓ Found at $MULTIWFN_PATH"
else
    echo "○ Not configured (optional)"
fi

# Check workspace
echo -n "Workspace: "
if [ -d "$OHMind_workspace" ] && [ -w "$OHMind_workspace" ]; then
    echo "✓ Writable at $OHMind_workspace"
else
    echo "✗ Not configured or not writable"
fi

echo "=== Verification Complete ==="
```

### Test MCP Servers

```bash
# Test each MCP server
python -m OHMind_agent.MCP.Chem.server --help
python -m OHMind_agent.MCP.HEMDesign.server --help
python -m OHMind_agent.MCP.ORCA.server --help
python -m OHMind_agent.MCP.Multiwfn.server --help
python -m OHMind_agent.MCP.GROMACS.server --help
```

## Platform-Specific Notes

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    libfftw3-dev \
    libgsl-dev
```

### CentOS/RHEL

```bash
# Install system dependencies
sudo yum groupinstall -y "Development Tools"
sudo yum install -y \
    cmake \
    openblas-devel \
    fftw-devel \
    gsl-devel
```

### GPU Setup (NVIDIA)

Ensure CUDA is properly installed:

```bash
# Check CUDA version
nvcc --version

# Verify PyTorch can see GPU
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Running Without GPU

OHMind can run without a GPU, but VAE model inference will be slower:

```bash
# Force CPU mode in PyTorch
export CUDA_VISIBLE_DEVICES=""
```

## Troubleshooting Installation

### Common Issues

| Issue | Solution |
|-------|----------|
| Conda environment creation fails | Try `conda clean --all` then retry |
| CUDA not detected | Verify NVIDIA drivers and CUDA toolkit |
| RDKit import error | Reinstall: `conda install -c conda-forge rdkit` |
| Permission denied on workspace | Check directory ownership and permissions |

For more troubleshooting help, see [Troubleshooting Guide](../troubleshooting/index.md).

## See Also

- [Quick Start Guide](./quick-start.md) - Fast-track installation
- [First Steps](./first-steps.md) - Your first interaction with OHMind
- [Environment Variables](../configuration/environment-variables.md) - All configuration options
- [Troubleshooting](../troubleshooting/installation-issues.md) - Installation issues

---

*Last updated: 2025-12-22 | OHMind v1.0.0*
