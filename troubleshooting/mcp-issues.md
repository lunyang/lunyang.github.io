---
title: MCP Server Issues
description: "Solutions for MCP server connection, transport, and tool execution problems"
parent: Troubleshooting
nav_order: 2
---

# MCP Server Issues

> Solutions for MCP server connection, transport, and tool execution problems

## Table of Contents

- [Overview](#overview)
- [Connection Issues](#connection-issues)
- [Transport Mode Issues](#transport-mode-issues)
- [Tool Execution Errors](#tool-execution-errors)
- [Session Management Issues](#session-management-issues)
- [Server-Specific Issues](#server-specific-issues)
- [Debugging MCP Servers](#debugging-mcp-servers)
- [See Also](#see-also)

## Overview

MCP (Model Context Protocol) issues typically fall into these categories:

| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| Connection | Server not responding | Server not started, wrong port |
| Transport | Protocol errors | Mismatched transport modes |
| Tools | Tool execution fails | Missing dependencies, bad input |
| Sessions | Timeout, disconnection | Long operations, resource limits |

## Connection Issues

### Server Not Responding

**Symptom:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Solutions:**

1. **Check if server is running:**
   ```bash
   # For HTTP transport
   curl http://localhost:8101/
   
   # Check process
   ps aux | grep "MCP.*server"
   ```

2. **Start the server manually:**
   ```bash
   # Start all servers
   ./start_OHMind.sh
   
   # Or start individual server
   python -m OHMind_agent.MCP.Chem.server --transport streamable_http --port 8101
   ```

3. **Check port availability:**
   ```bash
   lsof -i :8101
   netstat -tlnp | grep 8101
   ```

### Wrong Port Configuration

**Symptom:** Server running but client can't connect

**Solutions:**

1. **Verify port configuration:**
   ```bash
   # Check environment variables
   echo $MCP_CHEM_PORT      # Default: 8101
   echo $MCP_HEMDESIGN_PORT # Default: 8102
   echo $MCP_ORCA_PORT      # Default: 8103
   echo $MCP_MULTIWFN_PORT  # Default: 8104
   echo $MCP_GROMACS_PORT   # Default: 8105
   ```

2. **Check mcp.json configuration:**
   ```json
   {
     "mcpServers": {
       "OHMind-Chem": {
         "transport": "streamable_http",
         "url": "http://localhost:8101/"
       }
     }
   }
   ```

3. **Test connectivity:**
   ```bash
   for port in 8101 8102 8103 8104 8105; do
     echo -n "Port $port: "
     curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/" || echo "failed"
     echo ""
   done
   ```

### Server Startup Failure

**Symptom:**
```
ERROR: Failed to start MCP server: OHMind-Chem
```

**Solutions:**

1. **Check server logs:**
   ```bash
   tail -f OHMind_logs/chem_mcp.log
   ```

2. **Run server manually to see errors:**
   ```bash
   PYTHONPATH=. python -m OHMind_agent.MCP.Chem.server --transport stdio
   ```

3. **Check dependencies:**
   ```bash
   python -c "from OHMind_agent.MCP.Chem.server import mcp; print('OK')"
   ```

## Transport Mode Issues

### stdio vs HTTP Mismatch

**Symptom:**
```
Error: Invalid transport mode
```

**Solutions:**

1. **For stdio transport (Chainlit UI):**
   ```json
   {
     "command": "python",
     "args": ["-m", "OHMind_agent.MCP.Chem.server", "--transport", "stdio"]
   }
   ```

2. **For HTTP transport (Backend/CLI):**
   ```json
   {
     "transport": "streamable_http",
     "url": "http://localhost:8101/"
   }
   ```

3. **Verify server is using correct transport:**
   ```bash
   # Start with explicit transport
   python -m OHMind_agent.MCP.Chem.server --transport streamable_http --port 8101
   ```

### HTTP Transport Not Working

**Symptom:** HTTP requests fail or timeout

**Solutions:**

1. **Check server is in HTTP mode:**
   ```bash
   # Server should show:
   # INFO: Uvicorn running on http://0.0.0.0:8101
   ```

2. **Test endpoint:**
   ```bash
   curl -v http://localhost:8101/
   ```

3. **Check firewall:**
   ```bash
   sudo ufw status
   # Allow port if needed
   sudo ufw allow 8101
   ```

### stdio Transport Hangs

**Symptom:** Server starts but doesn't respond to commands

**Solutions:**

1. **Check for buffering issues:**
   ```bash
   # Run with unbuffered output
   PYTHONUNBUFFERED=1 python -m OHMind_agent.MCP.Chem.server --transport stdio
   ```

2. **Verify stdin/stdout not redirected:**
   ```bash
   # Test with echo
   echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
     python -m OHMind_agent.MCP.Chem.server --transport stdio
   ```

## Tool Execution Errors

### Tool Not Found

**Symptom:**
```
ToolNotFoundError: Tool 'xyz' not found in server
```

**Solutions:**

1. **List available tools:**
   ```python
   from OHMind_agent.agents.mcp_session_manager import get_session_manager
   
   manager = get_session_manager()
   for server, tools in manager.tools_by_server.items():
       print(f"{server}:")
       for tool in tools:
           print(f"  - {tool.name}")
   ```

2. **Check tool is registered:**
   ```bash
   # For HTTP server
   curl http://localhost:8101/tools/list
   ```

3. **Verify server has tool:**
   ```python
   # In server code, check @mcp.tool() decorators
   ```

### Tool Execution Timeout

**Symptom:**
```
TimeoutError: Tool execution exceeded timeout
```

**Solutions:**

1. **Increase timeout in client:**
   ```python
   # In session manager configuration
   config = {
       "timeout": 300  # 5 minutes
   }
   ```

2. **Check for long-running operations:**
   - QM calculations can take hours
   - MD simulations can take days
   - Use async/background execution

3. **Monitor tool progress:**
   ```bash
   # Check server logs
   tail -f OHMind_logs/orca_mcp.log
   ```

### Tool Input Validation Error

**Symptom:**
```
ValidationError: Invalid input for tool 'optimize_hem_design'
```

**Solutions:**

1. **Check tool schema:**
   ```python
   tool = manager.get_tools("OHMind-HEMDesign")[0]
   print(tool.args_schema.schema())
   ```

2. **Verify input format:**
   ```python
   # Correct format
   {
       "backbone": "PBF_BB_1",
       "cation_name": "piperidinium",
       "property": "multi",
       "num_part": 100,
       "steps": 20
   }
   ```

3. **Check required vs optional fields**

### Tool Returns Error

**Symptom:**
```
ToolError: SMILES parsing failed
```

**Solutions:**

1. **Check input validity:**
   ```python
   from rdkit import Chem
   mol = Chem.MolFromSmiles("your_smiles")
   if mol is None:
       print("Invalid SMILES")
   ```

2. **Check server logs for details:**
   ```bash
   grep -i error OHMind_logs/chem_mcp.log | tail -20
   ```

3. **Test tool directly:**
   ```python
   from OHMind_agent.MCP.Chem.server import smiles_to_mol
   result = smiles_to_mol("CCO")
   print(result)
   ```

## Session Management Issues

### Session Timeout

**Symptom:**
```
SessionError: Session expired or disconnected
```

**Solutions:**

1. **Check session manager state:**
   ```python
   manager = get_session_manager()
   print(f"Active sessions: {list(manager._active_sessions.keys())}")
   ```

2. **Reinitialize sessions:**
   ```python
   await cleanup_mcp_sessions()
   manager = await initialize_mcp_sessions(server_configs)
   ```

3. **Increase keep-alive settings**

### Multiple Session Conflicts

**Symptom:** Tools work sometimes but fail randomly

**Solutions:**

1. **Use single global session manager:**
   ```python
   # Don't create multiple managers
   manager = get_session_manager()  # Always returns same instance
   ```

2. **Check for concurrent access issues**

3. **Ensure proper cleanup:**
   ```python
   # In application shutdown
   await cleanup_mcp_sessions()
   ```

### Memory Leak in Sessions

**Symptom:** Memory usage grows over time

**Solutions:**

1. **Monitor memory:**
   ```bash
   ps aux | grep "MCP.*server" | awk '{print $6}'
   ```

2. **Restart servers periodically:**
   ```bash
   ./stop_OHMind.sh
   ./start_OHMind.sh
   ```

3. **Check for unclosed resources in tools**

## Server-Specific Issues

### OHMind-Chem Issues

**Common problems:**

1. **RDKit not available:**
   ```bash
   python -c "from rdkit import Chem; print('OK')"
   ```

2. **Tavily API key missing:**
   ```bash
   echo $TAVILY_API_KEY
   # Set if missing
   export TAVILY_API_KEY="your-key"
   ```

### OHMind-HEMDesign Issues

**Common problems:**

1. **VAE model not found:**
   ```bash
   ls -la OHMind/OHVAE/model.epoch-*
   ```

2. **HEM_SAVE_PATH not writable:**
   ```bash
   mkdir -p "$HEM_SAVE_PATH"
   touch "$HEM_SAVE_PATH/test" && rm "$HEM_SAVE_PATH/test"
   ```

### OHMind-ORCA Issues

**Common problems:**

1. **ORCA binary not found:**
   ```bash
   echo $OHMind_ORCA
   ls -la "$OHMind_ORCA"
   ```

2. **MPI not configured:**
   ```bash
   echo $OHMind_MPI
   ls -la "$OHMind_MPI/mpirun"
   ```

3. **QM_WORK_DIR issues:**
   ```bash
   mkdir -p "$QM_WORK_DIR"
   chmod 755 "$QM_WORK_DIR"
   ```

### OHMind-Multiwfn Issues

**Common problems:**

1. **Multiwfn binary not found:**
   ```bash
   echo $MULTIWFN_PATH
   ls -la "$MULTIWFN_PATH"
   ```

2. **Missing input files:**
   - Multiwfn requires wavefunction files (.wfn, .wfx, .molden)
   - Run QM calculation first

### OHMind-GROMACS Issues

**Common problems:**

1. **GROMACS not in PATH:**
   ```bash
   which gmx
   # If not found, source GROMACS
   source /path/to/gromacs/bin/GMXRC
   ```

2. **MD_WORK_DIR issues:**
   ```bash
   mkdir -p "$MD_WORK_DIR"
   chmod 755 "$MD_WORK_DIR"
   ```

## Debugging MCP Servers

### Enable Debug Logging

```bash
# Set log level
export MCP_LOG_LEVEL=DEBUG

# Or in Python
import logging
logging.getLogger("OHMind_agent.MCP").setLevel(logging.DEBUG)
```

### Manual Server Testing

```bash
# Test Chem server
PYTHONPATH=. python -c "
from OHMind_agent.MCP.Chem.server import mcp
print('Tools:', [t.name for t in mcp.list_tools()])
"

# Test tool directly
PYTHONPATH=. python -c "
from OHMind_agent.MCP.Chem.server import get_molecular_weight
result = get_molecular_weight('CCO')
print('Result:', result)
"
```

### MCP Protocol Debugging

```bash
# Capture MCP messages
python -m OHMind_agent.MCP.Chem.server --transport stdio 2>&1 | tee mcp_debug.log

# Send test message
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  python -m OHMind_agent.MCP.Chem.server --transport stdio
```

### Health Check Script

```bash
#!/bin/bash
# mcp_health_check.sh

echo "=== MCP Server Health Check ==="

servers=(
    "OHMind-Chem:8101"
    "OHMind-HEMDesign:8102"
    "OHMind-ORCA:8103"
    "OHMind-Multiwfn:8104"
    "OHMind-GROMACS:8105"
)

for server in "${servers[@]}"; do
    name="${server%%:*}"
    port="${server##*:}"
    
    echo -n "$name (port $port): "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo "✅ Running"
    elif [ "$response" = "000" ]; then
        echo "❌ Not responding"
    else
        echo "⚠️  HTTP $response"
    fi
done

echo ""
echo "=== Check Complete ==="
```

## See Also

- [Troubleshooting Overview](./index.md) - Main troubleshooting guide
- [Installation Issues](./installation-issues.md) - Setup problems
- [MCP Integration](../architecture/mcp-integration.md) - MCP architecture
- [MCP Servers Reference](../mcp-servers/index.md) - Server documentation
- [Session Manager API](../api/session-manager.md) - Session management

---

*Last updated: 2025-12-23 | OHMind v0.1.0*
