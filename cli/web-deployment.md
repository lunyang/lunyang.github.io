---
title: "Web Deployment"
description: "Deploy OHMind CLI as a web application using textual-serve"
category: "cli"
tags: ["cli", "web", "deployment", "textual-serve", "remote"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: CLI Application
nav_order: 5
---

# Web Deployment

> Deploy the OHMind CLI as a web application for remote access

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Configuration Options](#configuration-options)
- [Network Configuration](#network-configuration)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The OHMind CLI can be deployed as a web application using `textual-serve`, allowing remote access through a web browser. This is useful for:

- Sharing OHMind with team members
- Accessing OHMind from different machines
- Running OHMind on a server with remote access
- Demonstrating OHMind capabilities

### How It Works

`textual-serve` creates a web server that:
1. Runs the Textual TUI application on the server
2. Streams the terminal output to web browsers via WebSocket
3. Captures keyboard input from the browser
4. Provides a terminal-like experience in the browser

## Quick Start

### Deploy Command

```bash
# Deploy with default settings
python -m OHMind_cli deploy

# Deploy with custom host and port
python -m OHMind_cli deploy --host 0.0.0.0 --port 8000
```

### Access the Application

After starting, access the application at:
- Local: `http://localhost:8000`
- Network: `http://<your-ip>:8000`

## Configuration Options

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--host` | `0.0.0.0` | Host address to bind |
| `--port`, `-p` | `8000` | Port number |
| `--title` | `HEM Design Multi-Agent System — PolyAI Team, CIAC` | Browser title |
| `--public-url` | `http://localhost:<port>` | Public URL for WebSocket |
| `--debug`, `-d` | `false` | Enable debug logging |

### Examples

```bash
# Local development
python -m OHMind_cli deploy --host 127.0.0.1 --port 3000

# Network access
python -m OHMind_cli deploy --host 0.0.0.0 --port 8080

# With custom title
python -m OHMind_cli deploy --title "OHMind Research Server"

# Behind reverse proxy
python -m OHMind_cli deploy --public-url https://ohmind.example.com
```

## Network Configuration

### Binding to All Interfaces

Use `--host 0.0.0.0` to accept connections from any network interface:

```bash
python -m OHMind_cli deploy --host 0.0.0.0 --port 8000
```

This allows access from:
- `localhost` (local machine)
- LAN IP address (other machines on network)
- Public IP (if port is forwarded)

### Localhost Only

For local-only access, bind to `127.0.0.1`:

```bash
python -m OHMind_cli deploy --host 127.0.0.1 --port 8000
```

### Behind a Reverse Proxy

When running behind nginx, Apache, or another reverse proxy:

```bash
python -m OHMind_cli deploy \
    --host 127.0.0.1 \
    --port 8000 \
    --public-url https://ohmind.example.com
```

The `--public-url` is important for WebSocket connections to work correctly.

### Nginx Configuration Example

```nginx
server {
    listen 443 ssl;
    server_name ohmind.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }
}
```

## Security Considerations

### Authentication

The web deployment does not include built-in authentication. Consider:

1. **Reverse proxy authentication**: Use nginx or Apache basic auth
2. **VPN access**: Restrict to VPN users only
3. **Firewall rules**: Limit access by IP address

### Example: Basic Auth with Nginx

```nginx
location / {
    auth_basic "OHMind Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    
    proxy_pass http://127.0.0.1:8000;
    # ... other proxy settings
}
```

### Network Security

- Avoid exposing directly to the internet without authentication
- Use HTTPS when deploying publicly
- Consider rate limiting for public deployments
- Monitor access logs for suspicious activity

### Resource Limits

Each connected user runs a separate instance of the CLI. Consider:
- Memory usage per connection
- CPU usage during agent operations
- MCP server connection limits

## Environment Setup

### Required Environment Variables

Ensure these are set before deploying:

```bash
# LLM Configuration
export OPENAI_API_KEY="your-api-key"

# Workspace
export OHMind_workspace="/path/to/workspace"

# External Software (if using)
export OHMind_ORCA="/path/to/orca"
export MULTIWFN_PATH="/path/to/Multiwfn"
```

### PYTHONPATH

The deploy command automatically sets `PYTHONPATH` to include the OHMind root directory.

## Startup Output

When deploying, you'll see:

```
🌐 Starting OHMind web server...
   Host: 0.0.0.0
   Port: 8000
   Public URL: http://localhost:8000
   Command: /path/to/python -m OHMind_cli

   Access the app at:
   - Local: http://localhost:8000
   - Network: http://<your-ip>:8000

   Note: The app may take a moment to initialize.
   If you see a loading screen, wait a few seconds for the app to start.
```

## Troubleshooting

### Connection Issues

**Problem**: Browser shows "Connection refused"

**Solutions**:
- Verify the server is running
- Check firewall allows the port
- Ensure correct host binding (`0.0.0.0` for network access)

### WebSocket Errors

**Problem**: Application loads but doesn't respond

**Solutions**:
- Check `--public-url` matches actual access URL
- Verify WebSocket upgrade is allowed by proxy
- Check browser console for WebSocket errors

### Slow Performance

**Problem**: Application feels sluggish

**Solutions**:
- Check network latency
- Reduce terminal size in browser
- Consider running closer to users geographically

### MCP Server Issues

**Problem**: MCP tools not available

**Solutions**:
- Ensure MCP servers are started before deploying
- Check environment variables are set
- Verify MCP server ports are accessible

### Memory Issues

**Problem**: Server runs out of memory with multiple users

**Solutions**:
- Limit concurrent connections
- Increase server memory
- Use process manager with memory limits

## Production Deployment

### Using systemd

Create `/etc/systemd/system/ohmind-web.service`:

```ini
[Unit]
Description=OHMind Web Interface
After=network.target

[Service]
Type=simple
User=ohmind
WorkingDirectory=/opt/ohmind
Environment="OPENAI_API_KEY=your-key"
Environment="OHMind_workspace=/opt/ohmind/workspace"
ExecStart=/opt/ohmind/venv/bin/python -m OHMind_cli deploy --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ohmind-web
sudo systemctl start ohmind-web
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000

CMD ["python", "-m", "OHMind_cli", "deploy", "--host", "0.0.0.0", "--port", "8000"]
```

## See Also

- [CLI Overview](./index.md) - Getting started with the CLI
- [Configuration](../configuration/index.md) - Environment configuration
- [Troubleshooting](../troubleshooting/index.md) - Common issues

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
