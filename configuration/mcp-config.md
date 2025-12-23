---
title: "MCP Configuration"
description: "Guide to configuring MCP servers in OHMind including mcp.json format, transport modes, and server settings"
category: "configuration"
tags: ["mcp", "configuration", "servers", "transport"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: Configuration Overview
nav_order: 2
---

# MCP Configuration

> Complete guide to configuring Model Context Protocol (MCP) servers in OHMind, including the mcp.json format, transport modes, and per-server settings.

## Table of Contents

- [Overview](#overview)
- [Configuration File Location](#configuration-file-location)
- [mcp.json Format](#mcpjson-format)
- [Server Configuration Options](#server-configuration-options)
- [Transport Modes](#transport-modes)
- [OHMind MCP Servers](#ohmind-mcp-servers)
- [Complete Example](#complete-example)
- [Chainlit UI Configuration](#chainlit-ui-configuration)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

OHMind uses the Model Context Protocol (MCP) to provide tools to agents. MCP servers are configured in a JSON file that defines:

- Server command and arguments
- Environment variables for each server
- Transport mode (stdio or HTTP)
- Timeout and enable/disable settings

The multi-agent system loads this configuration at startup and establishes connections to enabled servers.

## Configuration File Location

The MCP configuration file location is specified by the `MCP_CONFIG_PATH` environment variable:

```bash
# In .env
MCP_CONFIG_PATH=/path/to/OHMind/mcp.json
```

**Default locations:**

| Component | Config File |
|-----------|-------------|
| Backend/Agents | `mcp.json` (project root) |
| Chainlit UI | `OHMind_ui/.chainlit/mcp.json` |

## mcp.json Format

The configuration file uses JSON format with a `mcpServers` object containing server definitions:

```json
{
  "mcpServers": {
    "server-name": {
      "disabled": false,
      "timeout": 300,
      "type": "stdio",
      "command": "/path/to/python",
      "args": ["-m", "module.server", "--transport", "stdio"],
      "env": {
        "VARIABLE": "value"
      }
    }
  }
}
```

### Top-Level Structure

```json
{
  "mcpServers": {
    "<server-name>": { /* server configuration */ },
    "<another-server>": { /* server configuration */ }
  }
}
```

## Server Configuration Options

Each server entry supports the following options:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `disabled` | boolean | No | Set to `true` to disable the server (default: `false`) |
| `timeout` | number | No | Connection timeout in seconds (default: `300`) |
| `type` | string | Yes | Transport type: `"stdio"` or `"http"` |
| `command` | string | Yes (stdio) | Path to the Python executable |
| `args` | array | Yes (stdio) | Command-line arguments |
| `env` | object | No | Environment variables for the server process |
| `url` | string | Yes (http) | Server URL for HTTP transport |
| `autoApprove` | array | No | List of tools to auto-approve (no confirmation) |

### Field Details

#### `disabled`

Controls whether the server is loaded at startup:

```json
{
  "OHMind-ORCA": {
    "disabled": true,  // Server will not be started
    ...
  }
}
```

#### `timeout`

Connection and operation timeout in seconds:

```json
{
  "OHMind-HEMDesign": {
    "timeout": 600,  // 10 minutes for long PSO optimizations
    ...
  }
}
```

#### `type`

Transport mode for communication:

- `"stdio"`: Standard input/output (recommended for local use)
- `"http"`: HTTP transport (for remote or IDE integration)

#### `command` and `args`

For stdio transport, specify the Python executable and module:

```json
{
  "command": "/home/user/anaconda3/envs/OHMind/bin/python",
  "args": ["-m", "OHMind_agent.MCP.Chem.server", "--transport", "stdio"]
}
```

#### `env`

Environment variables passed to the server process:

```json
{
  "env": {
    "PYTHONPATH": "/path/to/OHMind",
    "OHMind_ORCA": "/opt/orca/orca",
    "QM_WORK_DIR": "/data/workspace/ORCA"
  }
}
```

#### `autoApprove`

List of tool names that don't require user confirmation:

```json
{
  "autoApprove": ["MoleculeWeight", "SmilesCanonicalization"]
}
```

## Transport Modes

### stdio Transport (Recommended)

Standard input/output transport for local server processes:

```json
{
  "OHMind-Chem": {
    "type": "stdio",
    "command": "/path/to/python",
    "args": ["-m", "OHMind_agent.MCP.Chem.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind"
    }
  }
}
```

**Advantages:**
- Simple setup
- No network configuration
- Automatic process management

**Use cases:**
- Local development
- Single-user deployments
- CLI application

### HTTP Transport

HTTP-based transport for remote access or IDE integration:

```json
{
  "OHMind-Chem-HTTP": {
    "type": "http",
    "url": "http://127.0.0.1:8101/",
    "disabled": false
  }
}
```

**Default HTTP Ports:**

| Server | Port | URL |
|--------|------|-----|
| OHMind-Chem | 8101 | `http://127.0.0.1:8101/` |
| OHMind-HEMDesign | 8102 | `http://127.0.0.1:8102/` |
| OHMind-ORCA | 8103 | `http://127.0.0.1:8103/` |
| OHMind-Multiwfn | 8104 | `http://127.0.0.1:8104/` |
| OHMind-GROMACS | 8105 | `http://127.0.0.1:8105/` |

**Starting HTTP servers:**

```bash
./start_OHMind.sh
```

**Advantages:**
- Remote access capability
- IDE plugin integration
- Multiple client support

**Use cases:**
- IDE plugins (VS Code, etc.)
- External MCP clients
- Multi-user environments

## OHMind MCP Servers

### OHMind-Chem

Chemistry and molecular informatics tools.

```json
{
  "OHMind-Chem": {
    "disabled": false,
    "timeout": 300,
    "type": "stdio",
    "command": "/path/to/python",
    "args": ["-m", "OHMind_agent.MCP.Chem.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "TAVILY_API_KEY": "tvly-your-key"
    }
  }
}
```

**Required environment:**
- `PYTHONPATH`: Path to OHMind project
- `TAVILY_API_KEY`: For web search functionality (optional)

### OHMind-HEMDesign

HEM optimization and PSO tools.

```json
{
  "OHMind-HEMDesign": {
    "disabled": false,
    "timeout": 600,
    "type": "stdio",
    "command": "/path/to/python",
    "args": ["-m", "OHMind_agent.MCP.HEMDesign.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "HEM_SAVE_PATH": "/data/workspace/HEM"
    }
  }
}
```

**Required environment:**
- `PYTHONPATH`: Path to OHMind project
- `HEM_SAVE_PATH`: Directory for optimization results

**Note:** Longer timeout (600s) recommended for PSO optimizations.

### OHMind-ORCA

Quantum chemistry calculations via ORCA.

```json
{
  "OHMind-ORCA": {
    "disabled": false,
    "timeout": 300,
    "type": "stdio",
    "command": "/path/to/python",
    "args": ["-m", "OHMind_agent.MCP.ORCA.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "OHMind_ORCA": "/opt/orca/orca",
      "OHMind_MPI": "/usr/local/openmpi/bin",
      "QM_WORK_DIR": "/data/workspace/ORCA"
    }
  }
}
```

**Required environment:**
- `PYTHONPATH`: Path to OHMind project
- `OHMind_ORCA`: Full path to ORCA executable
- `OHMind_MPI`: Directory containing MPI binaries
- `QM_WORK_DIR`: Working directory for calculations

### OHMind-Multiwfn

Wavefunction analysis via Multiwfn.

```json
{
  "OHMind-Multiwfn": {
    "disabled": false,
    "timeout": 300,
    "type": "stdio",
    "command": "/path/to/python",
    "args": ["-m", "OHMind_agent.MCP.Multiwfn.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "MULTIWFN_PATH": "/opt/multiwfn/Multiwfn",
      "MULTIWFN_WORK_DIR": "/data/workspace/Multiwfn"
    }
  }
}
```

**Required environment:**
- `PYTHONPATH`: Path to OHMind project
- `MULTIWFN_PATH`: Full path to Multiwfn executable
- `MULTIWFN_WORK_DIR`: Working directory for analysis

### OHMind-GROMACS

Molecular dynamics simulations via GROMACS.

```json
{
  "OHMind-GROMACS": {
    "disabled": false,
    "timeout": 300,
    "type": "stdio",
    "command": "/path/to/python",
    "args": ["-m", "OHMind_agent.MCP.GROMACS.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "MD_WORK_DIR": "/data/workspace/GROMACS"
    }
  }
}
```

**Required environment:**
- `PYTHONPATH`: Path to OHMind project
- `MD_WORK_DIR`: Working directory for simulations

**Note:** GROMACS binaries must be available on PATH.

## Complete Example

Full `mcp.json` configuration:

```json
{
  "mcpServers": {
    "OHMind-Chem": {
      "disabled": false,
      "timeout": 300,
      "type": "stdio",
      "command": "/home/user/anaconda3/envs/OHMind/bin/python",
      "args": ["-m", "OHMind_agent.MCP.Chem.server", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "/home/user/OHMind",
        "TAVILY_API_KEY": "tvly-dev-your-key"
      }
    },
    "OHMind-HEMDesign": {
      "disabled": false,
      "timeout": 600,
      "type": "stdio",
      "command": "/home/user/anaconda3/envs/OHMind/bin/python",
      "args": ["-m", "OHMind_agent.MCP.HEMDesign.server", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "/home/user/OHMind",
        "HEM_SAVE_PATH": "/data/ohmind_workspace/HEM"
      }
    },
    "OHMind-ORCA": {
      "disabled": false,
      "timeout": 300,
      "type": "stdio",
      "command": "/home/user/anaconda3/envs/OHMind/bin/python",
      "args": ["-m", "OHMind_agent.MCP.ORCA.server", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "/home/user/OHMind",
        "OHMind_ORCA": "/opt/orca/orca",
        "OHMind_MPI": "/usr/local/openmpi/bin",
        "QM_WORK_DIR": "/data/ohmind_workspace/ORCA"
      }
    },
    "OHMind-Multiwfn": {
      "disabled": false,
      "timeout": 300,
      "type": "stdio",
      "command": "/home/user/anaconda3/envs/OHMind/bin/python",
      "args": ["-m", "OHMind_agent.MCP.Multiwfn.server", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "/home/user/OHMind",
        "MULTIWFN_PATH": "/opt/multiwfn/Multiwfn",
        "MULTIWFN_WORK_DIR": "/data/ohmind_workspace/Multiwfn"
      }
    },
    "OHMind-GROMACS": {
      "disabled": false,
      "timeout": 300,
      "type": "stdio",
      "command": "/home/user/anaconda3/envs/OHMind/bin/python",
      "args": ["-m", "OHMind_agent.MCP.GROMACS.server", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "/home/user/OHMind",
        "MD_WORK_DIR": "/data/ohmind_workspace/GROMACS"
      }
    }
  }
}
```

## Chainlit UI Configuration

The Chainlit web UI requires manual MCP server configuration through its interface.

### Adding Servers in Chainlit

1. Start the backend and UI:
   ```bash
   ./start_apps.sh
   ```

2. Open the UI at `http://localhost:8000`

3. Click the **MCP** panel in the left sidebar

4. Click **Add server** for each server:
   - **Name**: e.g., `OHMind-Chem`
   - **Type**: `stdio`
   - **Command**: `/path/to/python`
   - **Args**: `-m OHMind_agent.MCP.Chem.server --transport stdio`

### Reference Configuration

The file `OHMind_ui/.chainlit/mcp.json` documents the expected configuration but is not automatically loaded by Chainlit.

## Troubleshooting

### Server Not Connecting

1. **Verify Python path:**
   ```bash
   which python  # Should match command in mcp.json
   ```

2. **Test server manually:**
   ```bash
   PYTHONPATH=/path/to/OHMind \
     /path/to/python -m OHMind_agent.MCP.Chem.server --transport stdio
   ```

3. **Check environment variables:**
   ```bash
   env | grep -E "^(PYTHONPATH|OHMind|HEM|QM|MD|MULTIWFN)"
   ```

### Timeout Errors

Increase the timeout for long-running operations:

```json
{
  "OHMind-HEMDesign": {
    "timeout": 1200,  // 20 minutes
    ...
  }
}
```

### Missing Tools

Ensure the server is enabled and properly configured:

```python
from OHMind_agent.config import get_mcp_config

mcp_config = get_mcp_config()
print(mcp_config.get_enabled_servers().keys())
```

### Permission Errors

Verify working directories are writable:

```bash
mkdir -p $HEM_SAVE_PATH $QM_WORK_DIR $MD_WORK_DIR $MULTIWFN_WORK_DIR
chmod u+rwx $HEM_SAVE_PATH $QM_WORK_DIR $MD_WORK_DIR $MULTIWFN_WORK_DIR
```

## See Also

- [Configuration Overview](./index.md) - Configuration system overview
- [Environment Variables](./environment-variables.md) - All environment variables
- [MCP Servers](../mcp-servers/index.md) - MCP server reference
- [MCP Issues](../troubleshooting/mcp-issues.md) - Troubleshooting guide

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
