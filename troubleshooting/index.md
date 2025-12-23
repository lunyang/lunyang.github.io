# Troubleshooting Guide

> Diagnostic tools, common issues, and solutions for OHMind

## Table of Contents

- [Overview](#overview)
- [Quick Diagnostics](#quick-diagnostics)
- [Log Locations](#log-locations)
- [Common Issue Categories](#common-issue-categories)
- [Diagnostic Commands](#diagnostic-commands)
- [Health Check Script](#health-check-script)
- [Getting Help](#getting-help)
- [See Also](#see-also)

## Overview

This guide helps you diagnose and resolve common issues with OHMind. Issues are organized by category:

| Category | Common Symptoms | Guide |
|----------|-----------------|-------|
| [Installation](./installation-issues.md) | Import errors, missing packages, environment issues | Setup problems |
| [MCP Servers](./mcp-issues.md) | Connection failures, tool errors, timeouts | Server connectivity |
| [LLM Providers](./llm-issues.md) | API errors, rate limits, authentication | AI model access |
| [External Software](./external-software.md) | ORCA/GROMACS/Multiwfn failures | Computational tools |

## Quick Diagnostics

### System Status Check

```bash
# Check if backend is running
curl -s http://localhost:8005/health | jq

# Check system info
curl -s http://localhost:8005/info | jq

# List active MCP servers
curl -s http://localhost:8005/ | jq '.mcp_clients'
```

### Environment Verification

```bash
# Verify conda environment
conda activate OHMind
python --version  # Should be 3.10+

# Check key packages
python -c "import langchain; print(f'LangChain: {langchain.__version__}')"
python -c "import langgraph; print(f'LangGraph: {langgraph.__version__}')"
python -c "import rdkit; print(f'RDKit: {rdkit.__version__}')"
```

### Workspace Check

```bash
# Verify workspace exists and is writable
ls -la "$OHMind_workspace"

# Check subdirectories
ls -la "$OHMind_workspace"/{HEM,QM,MD,Multiwfn} 2>/dev/null || echo "Some directories missing"
```

## Log Locations

### Application Logs

| Component | Log Location | Description |
|-----------|--------------|-------------|
| Backend | `OHMind_logs/backend.log` | FastAPI backend logs |
| CLI | `OHMind_logs/cli.log` | Terminal UI logs |
| MCP Chem | `OHMind_logs/chem_mcp.log` | Chemistry server logs |
| MCP HEM | `OHMind_logs/hem_mcp.log` | HEMDesign server logs |
| MCP ORCA | `OHMind_logs/orca_mcp.log` | ORCA server logs |
| MCP Multiwfn | `OHMind_logs/multiwfn_mcp.log` | Multiwfn server logs |
| MCP GROMACS | `OHMind_logs/gromacs_mcp.log` | GROMACS server logs |

### Viewing Logs

```bash
# View recent backend logs
tail -f OHMind_logs/backend.log

# View MCP server logs
tail -f OHMind_logs/hem_mcp.log

# Search for errors
grep -i "error\|exception" OHMind_logs/*.log
```

### External Software Logs

| Software | Log Location | Description |
|----------|--------------|-------------|
| ORCA | `$QM_WORK_DIR/*.out` | Calculation output files |
| GROMACS | `$MD_WORK_DIR/*.log` | Simulation logs |
| Multiwfn | `$MULTIWFN_WORK_DIR/*.log` | Analysis logs |

## Common Issue Categories

### 🔧 Installation Issues

Problems during setup or environment creation:

- Conda environment creation failures
- Missing Python packages
- GPU/CUDA configuration
- Dependency conflicts

→ See [Installation Issues](./installation-issues.md)

### 🔌 MCP Server Issues

Problems with MCP server connections:

- Server not starting
- Connection timeouts
- Tool execution failures
- Transport mode issues

→ See [MCP Issues](./mcp-issues.md)

### 🤖 LLM Provider Issues

Problems with AI model access:

- API key errors
- Rate limiting
- Model availability
- Response parsing errors

→ See [LLM Issues](./llm-issues.md)

### 🧪 External Software Issues

Problems with computational tools:

- ORCA calculation failures
- GROMACS simulation errors
- Multiwfn analysis issues
- Path configuration problems

→ See [External Software Issues](./external-software.md)

## Diagnostic Commands

### Process Status

```bash
# Check all OHMind processes
ps aux | grep -E "OHMind|uvicorn|python.*MCP"

# Check specific ports
lsof -i :8005  # Backend
lsof -i :8101  # Chem MCP
lsof -i :8102  # HEMDesign MCP
lsof -i :8103  # ORCA MCP
lsof -i :8104  # Multiwfn MCP
lsof -i :8105  # GROMACS MCP
```

### Network Connectivity

```bash
# Test backend connectivity
curl -v http://localhost:8005/health

# Test MCP server (HTTP transport)
curl -v http://localhost:8101/

# Check if ports are listening
netstat -tlnp | grep -E "8005|810[1-5]"
```

### Environment Variables

```bash
# Check critical environment variables
echo "OHMind_workspace: $OHMind_workspace"
echo "OHMind_ORCA: $OHMind_ORCA"
echo "MULTIWFN_PATH: $MULTIWFN_PATH"
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."  # First 10 chars only
```

### Python Environment

```bash
# List installed packages
conda list | grep -E "langchain|langgraph|rdkit|torch"

# Check import paths
python -c "import OHMind; print(OHMind.__file__)"
python -c "import OHMind_agent; print(OHMind_agent.__file__)"
```

## Health Check Script

Create a comprehensive health check:

```bash
#!/bin/bash
# health_check.sh - OHMind System Health Check

echo "=== OHMind Health Check ==="
echo ""

# 1. Environment
echo "1. Environment"
echo "   Python: $(python --version 2>&1)"
echo "   Conda env: $CONDA_DEFAULT_ENV"
echo ""

# 2. Workspace
echo "2. Workspace"
if [ -d "$OHMind_workspace" ]; then
    echo "   ✅ Workspace exists: $OHMind_workspace"
    for dir in HEM QM MD Multiwfn; do
        if [ -d "$OHMind_workspace/$dir" ]; then
            echo "   ✅ $dir directory exists"
        else
            echo "   ❌ $dir directory missing"
        fi
    done
else
    echo "   ❌ Workspace not found: $OHMind_workspace"
fi
echo ""

# 3. Backend
echo "3. Backend API"
if curl -s http://localhost:8005/health > /dev/null 2>&1; then
    echo "   ✅ Backend is running"
    curl -s http://localhost:8005/info | jq -r '.agents | "   Agents: " + (. | join(", "))'
else
    echo "   ❌ Backend not responding"
fi
echo ""

# 4. MCP Servers
echo "4. MCP Servers (HTTP)"
for port in 8101 8102 8103 8104 8105; do
    name=$(case $port in
        8101) echo "Chem";;
        8102) echo "HEMDesign";;
        8103) echo "ORCA";;
        8104) echo "Multiwfn";;
        8105) echo "GROMACS";;
    esac)
    if curl -s "http://localhost:$port/" > /dev/null 2>&1; then
        echo "   ✅ $name (port $port)"
    else
        echo "   ❌ $name (port $port) - not responding"
    fi
done
echo ""

# 5. External Software
echo "5. External Software"
if [ -n "$OHMind_ORCA" ] && [ -x "$OHMind_ORCA" ]; then
    echo "   ✅ ORCA: $OHMind_ORCA"
else
    echo "   ⚠️  ORCA: not configured or not executable"
fi

if [ -n "$MULTIWFN_PATH" ] && [ -x "$MULTIWFN_PATH" ]; then
    echo "   ✅ Multiwfn: $MULTIWFN_PATH"
else
    echo "   ⚠️  Multiwfn: not configured or not executable"
fi

if command -v gmx &> /dev/null; then
    echo "   ✅ GROMACS: $(which gmx)"
else
    echo "   ⚠️  GROMACS: not found in PATH"
fi
echo ""

echo "=== Health Check Complete ==="
```

Save as `health_check.sh` and run:

```bash
chmod +x health_check.sh
./health_check.sh
```

## Getting Help

### Before Asking for Help

1. **Check the logs** - Most issues leave traces in log files
2. **Run diagnostics** - Use the commands above to gather information
3. **Search existing issues** - Check if the problem is already documented
4. **Reproduce the issue** - Note the exact steps that cause the problem

### Information to Include

When reporting an issue, include:

```markdown
## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.12]
- OHMind version: [e.g., 0.1.0]
- Conda environment: [output of `conda list`]

## Issue Description
[Clear description of the problem]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [...]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Logs
[Relevant log excerpts]

## Additional Context
[Any other relevant information]
```

### Support Channels

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check the relevant documentation section first
- **Logs**: Always check logs before seeking help

## See Also

- [Installation Issues](./installation-issues.md) - Setup and environment problems
- [MCP Issues](./mcp-issues.md) - Server connection problems
- [LLM Issues](./llm-issues.md) - AI model access problems
- [External Software Issues](./external-software.md) - ORCA/GROMACS/Multiwfn problems
- [Configuration Reference](../configuration/index.md) - Environment setup
- [Quick Start Guide](../getting-started/quick-start.md) - Initial setup

---

*Last updated: 2025-12-23 | OHMind v0.1.0*
