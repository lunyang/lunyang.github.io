---
permalink: /configuration/
title: "Configuration Overview"
description: "Complete guide to configuring OHMind environment variables, MCP servers, LLM providers, and workspace settings"
category: "configuration"
tags: ["configuration", "environment", "setup", "mcp", "llm"]
last_updated: "2026-09-23"
version: "1.0.0"
nav_order: 4
has_children: true
---

# Configuration Overview

> Comprehensive guide to configuring OHMind for your environment, including environment variables, MCP servers, LLM providers, and workspace setup.

## Table of Contents

- [Configuration Hierarchy](#configuration-hierarchy)
- [Configuration Files](#configuration-files)
- [Quick Configuration Checklist](#quick-configuration-checklist)
- [Configuration Categories](#configuration-categories)
- [See Also](#see-also)

## Configuration Hierarchy

OHMind uses a layered configuration system with the following precedence (highest to lowest):

```
┌─────────────────────────────────────────────────────────────┐
│  1. Command-line arguments (highest priority)               │
├─────────────────────────────────────────────────────────────┤
│  2. Environment variables (exported in shell)               │
├─────────────────────────────────────────────────────────────┤
│  3. Component-specific .env files                           │
│     - OHMind_agent/.env                                     │
│     - OHMind_ui/.env                                        │
├─────────────────────────────────────────────────────────────┤
│  4. Root .env file (project root)                           │
├─────────────────────────────────────────────────────────────┤
│  5. Default values in code (lowest priority)                │
└─────────────────────────────────────────────────────────────┘
```

The configuration is managed through Pydantic-based settings in `OHMind_agent/config.py`, which automatically loads and validates environment variables.

## Configuration Files

### Primary Configuration Files

| File | Purpose | Used By |
|------|---------|---------|
| `.env` (root) | Main environment variables | Backend, agents, MCP servers |
| `mcp.json` | MCP server definitions | Multi-agent system, CLI |
| `OHMind_agent/.env` | Agent-specific overrides | Agent system |
| `OHMind_ui/.env` | UI-specific settings | Chainlit web UI |
| `OHMind_ui/.chainlit/mcp.json` | UI MCP documentation | Chainlit (reference only) |

### Configuration File Locations

```
OHMind/
├── .env                          # Root environment configuration
├── mcp.json                      # MCP server definitions
├── OHMind_agent/
│   └── .env                      # Agent-specific overrides
└── OHMind_ui/
    ├── .env                      # UI configuration
    └── .chainlit/
        └── mcp.json              # UI MCP reference
```

## Quick Configuration Checklist

### Essential Configuration

```bash
# 1. LLM Provider (choose one)
OPENAI_COMPATIBLE_API_KEY=your-api-key
OPENAI_COMPATIBLE_BASE_URL=https://api.provider.com/v1
OPENAI_COMPATIBLE_MODEL=gpt-4o

# 2. Workspace Root
OHMind_workspace=/path/to/workspace

# 3. MCP Configuration
MCP_CONFIG_PATH=/path/to/OHMind/mcp.json
```

### Optional but Recommended

```bash
# Vector database for RAG
QDRANT_PATH=/path/to/workspace/qdrant_db

# Web search capability
TAVILY_API_KEY=tvly-your-key

# External software paths
OHMind_ORCA=/path/to/orca
MULTIWFN_PATH=/path/to/multiwfn
```

## Configuration Categories

OHMind configuration is organized into the following categories:

### 1. Environment Variables

Core settings loaded from `.env` files:

- **LLM Configuration**: API keys, endpoints, model selection
- **Workspace Paths**: Working directories for each domain
- **Vector Database**: Qdrant connection settings
- **External Services**: Tavily, HuggingFace tokens
- **Server Settings**: Host, port, CORS origins

→ See [Environment Variables]({% link configuration/environment-variables.md %}) for complete reference.

### 2. MCP Server Configuration

JSON-based configuration for Model Context Protocol servers:

- **Server Definitions**: Command, arguments, environment
- **Transport Modes**: stdio and HTTP transports
- **Timeout Settings**: Per-server timeout configuration
- **Enable/Disable**: Individual server control

→ See [MCP Configuration]({% link configuration/mcp-config.md %}) for format and examples.

### 3. LLM Provider Setup

Support for multiple LLM providers:

- **Azure OpenAI**: Enterprise deployment
- **OpenAI Direct**: Standard OpenAI API
- **OpenAI-Compatible**: OpenRouter, Together, Groq, local models

→ See [LLM Providers]({% link configuration/llm-providers.md %}) for setup instructions.

### 4. Workspace Setup

Unified workspace organization:

- **Directory Structure**: HEM, QM, MD, Multiwfn subdirectories
- **Qdrant Storage**: Vector database location
- **Permissions**: Required access rights
- **Storage Requirements**: Disk space considerations

→ See [Workspace Setup]({% link configuration/workspace-setup.md %}) for detailed guide.

## Configuration Loading

OHMind uses Pydantic Settings for configuration management:

```python
from OHMind_agent.config import get_settings, get_mcp_config

# Get application settings
settings = get_settings()

# Access LLM configuration
llm_config = settings.get_llm_config()

# Get MCP server configuration
mcp_config = get_mcp_config()
enabled_servers = mcp_config.get_enabled_servers()
```

### Settings Class Structure

```python
class Settings(BaseSettings):
    # LLM Configuration
    openai_compatible_api_key: Optional[str]
    openai_compatible_base_url: Optional[str]
    openai_compatible_model: Optional[str]
    
    # Working Directories
    ohmind_workspace: Optional[str]
    hem_save_path: Optional[str]
    qm_work_dir: Optional[str]
    md_work_dir: Optional[str]
    multiwfn_work_dir: Optional[str]
    
    # Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

## Startup Scripts

Activate the intended environment first. The combined launchers load the root `.env` followed by the UI `.env`; later values can override earlier ones.

| Script | Purpose |
|---|---|
| `start_OHMind.sh` | MCP services, backend, and web UI |
| `start_OHMind_full.sh` | MCP services and terminal CLI |
| `start_OHMind_cli.sh` | CLI when MCP services are already running |

Use `PYTHON="$(command -v python)"` before the command to avoid developer-machine interpreter defaults, and `CHAINLIT="$(command -v chainlit)"` for the web launcher. See [Installation]({% link getting-started/installation.md %}) for complete examples.


## Validation

### Check Configuration

```bash
# Verify environment variables are set
env | grep -E "^(OPENAI|OHMind|MCP|QDRANT)"

# Test MCP configuration loading
python -c "from OHMind_agent.config import get_mcp_config; print(get_mcp_config().get_enabled_servers().keys())"

# Verify workspace directories exist
ls -la $OHMind_workspace
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "No LLM configuration found" | Set `OPENAI_COMPATIBLE_*` or `OPENAI_API_KEY` |
| "MCP config file not found" | Verify `MCP_CONFIG_PATH` points to valid `mcp.json` |
| "Permission denied" on workspace | Ensure workspace directory is writable |
| MCP server connection failed | Check Python path and environment in `mcp.json` |

## See Also

- [Environment Variables]({% link configuration/environment-variables.md %}) - Complete variable reference
- [MCP Configuration]({% link configuration/mcp-config.md %}) - MCP server setup
- [LLM Providers]({% link configuration/llm-providers.md %}) - Provider-specific configuration
- [Workspace Setup]({% link configuration/workspace-setup.md %}) - Directory structure and storage
- [Troubleshooting]({% link troubleshooting/index.md %}) - Common configuration issues

---

## Durable state and recovery memory

See [Memory and Persistence]({% link configuration/memory-persistence.md %}) for database preparation, default values, read/write modes, and current integration limits.
