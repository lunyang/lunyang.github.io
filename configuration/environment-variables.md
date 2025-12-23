---
title: "Environment Variables"
description: "Complete reference for all OHMind environment variables including LLM, workspace, and external software configuration"
category: "configuration"
tags: ["environment", "variables", "configuration", "setup"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: Configuration Overview
nav_order: 1
---

# Environment Variables

> Complete reference for all environment variables used by OHMind, organized by category.

## Table of Contents

- [LLM Configuration](#llm-configuration)
- [Workspace Configuration](#workspace-configuration)
- [Vector Database (Qdrant)](#vector-database-qdrant)
- [External Services](#external-services)
- [External Software Paths](#external-software-paths)
- [Server Configuration](#server-configuration)
- [Application Settings](#application-settings)
- [Example .env File](#example-env-file)
- [See Also](#see-also)

## LLM Configuration

OHMind supports multiple LLM providers. Configure one of the following options:

### OpenAI-Compatible APIs (Recommended)

Works with OpenRouter, Together AI, Groq, local models, and other OpenAI-compatible endpoints.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_COMPATIBLE_API_KEY` | API key for the provider | - | Yes |
| `OPENAI_COMPATIBLE_BASE_URL` | Base URL for the API endpoint | - | Yes |
| `OPENAI_COMPATIBLE_MODEL` | Model name to use | `gpt-4o` | No |
| `OPENAI_COMPATIBLE_EMBEDDING_MODEL` | Embedding model name | - | For RAG |

**Example:**

```bash
# Using OpenRouter
OPENAI_COMPATIBLE_API_KEY=sk-or-v1-your-key
OPENAI_COMPATIBLE_BASE_URL=https://openrouter.ai/api/v1
OPENAI_COMPATIBLE_MODEL=anthropic/claude-3.5-sonnet
OPENAI_COMPATIBLE_EMBEDDING_MODEL=openai/text-embedding-3-large

# Using Together AI
OPENAI_COMPATIBLE_API_KEY=your-together-key
OPENAI_COMPATIBLE_BASE_URL=https://api.together.xyz/v1
OPENAI_COMPATIBLE_MODEL=meta-llama/Llama-3-70b-chat-hf

# Using local Ollama
OPENAI_COMPATIBLE_API_KEY=ollama
OPENAI_COMPATIBLE_BASE_URL=http://localhost:11434/v1
OPENAI_COMPATIBLE_MODEL=llama3.1:70b
```

### Direct OpenAI

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `DEPLOYMENT_NAME` | Model name | `gpt-4o` | No |
| `EMBEDDING_DEPLOYMENT_NAME` | Embedding model | `text-embedding-ada-002` | No |

**Example:**

```bash
OPENAI_API_KEY=sk-your-openai-key
DEPLOYMENT_NAME=gpt-4o
EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
```

### Azure OpenAI

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | - | Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure endpoint URL | - | Yes |
| `OPENAI_API_VERSION` | API version | `2024-02-15-preview` | No |
| `DEPLOYMENT_NAME` | Deployment name | `gpt-4o` | No |
| `EMBEDDING_DEPLOYMENT_NAME` | Embedding deployment | `text-embedding-ada-002` | No |

**Example:**

```bash
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2024-02-15-preview
DEPLOYMENT_NAME=gpt-4o-deployment
EMBEDDING_DEPLOYMENT_NAME=embedding-deployment
```

## Workspace Configuration

All computational results are organized under a unified workspace root.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OHMind_workspace` | Root workspace directory | - | Yes |
| `WORKSPACE_ROOT` | Alias for workspace root | `$OHMind_workspace` | No |
| `HEM_SAVE_PATH` | HEM optimization results | `$OHMind_workspace/HEM` | No |
| `QM_WORK_DIR` | ORCA QM calculations | `$OHMind_workspace/ORCA` | No |
| `MD_WORK_DIR` | GROMACS MD simulations | `$OHMind_workspace/GROMACS` | No |
| `MULTIWFN_WORK_DIR` | Multiwfn analysis outputs | `$OHMind_workspace/Multiwfn` | No |
| `CHEM_WORK_DIR` | Chemistry tool outputs | `$OHMind_workspace` | No |

**Example:**

```bash
# Set the root workspace
OHMind_workspace=/data/ohmind_workspace

# Subdirectories (optional - defaults are derived from root)
HEM_SAVE_PATH=${OHMind_workspace}/HEM
QM_WORK_DIR=${OHMind_workspace}/ORCA
MD_WORK_DIR=${OHMind_workspace}/GROMACS
MULTIWFN_WORK_DIR=${OHMind_workspace}/Multiwfn
WORKSPACE_ROOT=${OHMind_workspace}
```

### Workspace Directory Structure

When properly configured, the workspace will have this structure:

```
$OHMind_workspace/
├── HEM/                    # PSO optimization results
│   ├── best_solutions_*.csv
│   ├── best_fitness_history_*.csv
│   └── optimization_*.log
├── ORCA/                   # QM calculation files
│   ├── temp_*/             # Per-job temporary directories
│   └── results/            # Preserved results
├── GROMACS/                # MD simulation files
│   ├── *.pdb, *.top        # Topology files
│   └── *.xtc, *.trr        # Trajectories
├── Multiwfn/               # Wavefunction analysis
│   └── <job-name>/         # Per-analysis directories
└── qdrant_db/              # Vector database (if local)
```

## Vector Database (Qdrant)

Configuration for the RAG system's vector database.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `QDRANT_URL` | Qdrant server URL | - | For server mode |
| `QDRANT_PATH` | Local storage path | `$OHMind_workspace/qdrant_db` | For local mode |
| `QDRANT_API_KEY` | API key (if required) | - | No |

**Local Mode (Recommended for single-user):**

```bash
# Use local file-based storage
QDRANT_PATH=/data/ohmind_workspace/qdrant_db
# Leave QDRANT_URL unset
```

**Server Mode (For multi-user or production):**

```bash
# Connect to Qdrant server
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-api-key
# Leave QDRANT_PATH unset
```

## External Services

### Web Search (Tavily)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TAVILY_API_KEY` | Tavily API key for web search | - | For web search |

Get a free API key at [tavily.com](https://tavily.com).

```bash
TAVILY_API_KEY=tvly-dev-your-key
```

### HuggingFace

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HUGGINGFACE_TOKEN` | HuggingFace access token | - | For reranking |

```bash
HUGGINGFACE_TOKEN=hf_your_token
```

### LangSmith (Tracing)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | `false` | No |
| `LANGCHAIN_API_KEY` | LangSmith API key | - | If tracing enabled |
| `LANGCHAIN_PROJECT` | Project name for traces | `hem-design-agents` | No |

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls_your_key
LANGCHAIN_PROJECT=my-ohmind-project
```

## External Software Paths

Paths to external computational chemistry software.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OHMind_ORCA` | Full path to ORCA binary | - | For QM calculations |
| `OHMind_MPI` | Directory containing MPI binaries | - | For parallel ORCA |
| `MULTIWFN_PATH` | Full path to Multiwfn executable | - | For wavefunction analysis |

**Example:**

```bash
# ORCA quantum chemistry
OHMind_ORCA=/opt/orca/orca
OHMind_MPI=/usr/local/openmpi/bin

# Multiwfn wavefunction analysis
MULTIWFN_PATH=/opt/multiwfn/Multiwfn

# GROMACS (typically on PATH after sourcing GMXRC)
# source /usr/local/gromacs/bin/GMXRC
```

### Verifying External Software

```bash
# Check ORCA
$OHMind_ORCA --version

# Check Multiwfn
$MULTIWFN_PATH <<< "q"

# Check GROMACS
gmx --version
```

## Server Configuration

Settings for the FastAPI backend server.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_HOST` | Server bind address | `0.0.0.0` | No |
| `API_PORT` | Server port | `8000` | No |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `http://localhost:3000,http://localhost:3001` | No |

**Example:**

```bash
API_HOST=0.0.0.0
API_PORT=8005
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://myapp.example.com
```

## MCP Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MCP_CONFIG_PATH` | Path to mcp.json configuration | - | Yes |

**Example:**

```bash
MCP_CONFIG_PATH=/path/to/OHMind/mcp.json
```

## Application Settings

General application behavior settings.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LOG_LEVEL` | Logging verbosity | `INFO` | No |
| `MAX_TOKENS` | Maximum tokens for LLM responses | `4096` | No |
| `TEMPERATURE` | LLM temperature (0.0-1.0) | `0.7` | No |

**Example:**

```bash
LOG_LEVEL=DEBUG
MAX_TOKENS=8192
TEMPERATURE=0.5
```

## Example .env File

Complete example configuration:

```bash
# =============================================================================
# OHMind Environment Configuration
# =============================================================================

# -----------------------------------------------------------------------------
# LLM Configuration (choose one provider)
# -----------------------------------------------------------------------------

# Option 1: OpenAI-Compatible API (recommended)
OPENAI_COMPATIBLE_API_KEY=sk-your-api-key
OPENAI_COMPATIBLE_BASE_URL=https://api.provider.com/v1
OPENAI_COMPATIBLE_MODEL=gpt-4o
OPENAI_COMPATIBLE_EMBEDDING_MODEL=text-embedding-3-large

# Option 2: Direct OpenAI
# OPENAI_API_KEY=sk-your-openai-key

# Option 3: Azure OpenAI
# AZURE_OPENAI_API_KEY=your-azure-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# -----------------------------------------------------------------------------
# Workspace Configuration
# -----------------------------------------------------------------------------

OHMind_workspace=/data/ohmind_workspace
WORKSPACE_ROOT=${OHMind_workspace}
HEM_SAVE_PATH=${OHMind_workspace}/HEM
QM_WORK_DIR=${OHMind_workspace}/ORCA
MD_WORK_DIR=${OHMind_workspace}/GROMACS
MULTIWFN_WORK_DIR=${OHMind_workspace}/Multiwfn

# -----------------------------------------------------------------------------
# Vector Database (Qdrant)
# -----------------------------------------------------------------------------

# Local mode (recommended for single-user)
QDRANT_PATH=${OHMind_workspace}/qdrant_db

# Server mode (uncomment for multi-user)
# QDRANT_URL=http://localhost:6333
# QDRANT_API_KEY=

# -----------------------------------------------------------------------------
# External Services
# -----------------------------------------------------------------------------

TAVILY_API_KEY=tvly-dev-your-key
HUGGINGFACE_TOKEN=

# -----------------------------------------------------------------------------
# External Software Paths
# -----------------------------------------------------------------------------

OHMind_ORCA=/opt/orca/orca
OHMind_MPI=/usr/local/openmpi/bin
MULTIWFN_PATH=/opt/multiwfn/Multiwfn

# -----------------------------------------------------------------------------
# MCP Configuration
# -----------------------------------------------------------------------------

MCP_CONFIG_PATH=/path/to/OHMind/mcp.json

# -----------------------------------------------------------------------------
# Server Configuration
# -----------------------------------------------------------------------------

API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# -----------------------------------------------------------------------------
# Application Settings
# -----------------------------------------------------------------------------

LOG_LEVEL=INFO
MAX_TOKENS=4096
TEMPERATURE=0.7

# -----------------------------------------------------------------------------
# LangSmith Tracing (optional)
# -----------------------------------------------------------------------------

LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=hem-design-agents
```

## Environment Variable Precedence

When the same variable is defined in multiple places:

1. **Shell environment** (highest priority)
2. **Component-specific .env** (`OHMind_agent/.env`, `OHMind_ui/.env`)
3. **Root .env** (lowest priority)

```bash
# Example: Override for a single command
OHMind_workspace=/tmp/test_workspace python -m OHMind_cli
```

## See Also

- [Configuration Overview](./index.md) - Configuration system overview
- [MCP Configuration](./mcp-config.md) - MCP server setup
- [LLM Providers](./llm-providers.md) - Provider-specific details
- [Workspace Setup](./workspace-setup.md) - Directory structure
- [Installation Issues](../troubleshooting/installation-issues.md) - Common setup problems

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
