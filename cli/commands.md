---
title: "CLI Commands"
description: "Complete reference for OHMind CLI slash commands"
category: "cli"
tags: ["cli", "commands", "reference"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: CLI Application
nav_order: 1
---

# CLI Commands

> Complete reference for all slash commands available in the OHMind CLI

## Table of Contents

- [Overview](#overview)
- [Command Reference](#command-reference)
- [Usage Examples](#usage-examples)
- [See Also](#see-also)

## Overview

Slash commands provide quick access to CLI functionality without using keyboard shortcuts. Type a command starting with `/` in the input field and press Enter.

Commands are case-insensitive and can be abbreviated where noted.

## Command Reference

### Navigation Commands

#### `/help` or `/?`

Display the help screen with available commands and keyboard shortcuts.

```
/help
```

The help screen shows:
- Available slash commands
- Keyboard shortcuts
- Agent information

#### `/quit`, `/exit`, or `/q`

Exit the application with confirmation dialog.

```
/quit
```

A confirmation prompt appears before closing to prevent accidental exits.

### Conversation Commands

#### `/clear`

Clear the current conversation and start fresh.

```
/clear
```

This command:
- Removes all messages from the chat view
- Generates a new thread ID
- Resets conversation state
- Displays a confirmation message

#### `/new`

Start a new conversation while keeping the application running.

```
/new
```

Similar to `/clear`, this resets the conversation state and generates a new session ID.

### Information Commands

#### `/agents`

Display available agents and their capabilities.

```
/agents
```

Shows a panel listing all specialized agents:
- 👑 Supervisor - Task routing and orchestration
- 🧬 HEM Design - Membrane optimization
- 🧪 Chemistry - Molecular operations
- ⚛️ Quantum Mechanics - DFT calculations
- 💻 Molecular Dynamics - GROMACS simulations
- 📊 Multiwfn - Wavefunction analysis
- 📚 RAG Literature - Knowledge retrieval
- 🌐 Web Search - External resources

#### `/tools`

Display available MCP tools organized by server.

```
/tools
```

Shows tools grouped by MCP server:
- OHMind-Chem (17+ chemistry tools)
- OHMind-HEMDesign (7 HEM tools)
- OHMind-ORCA (10+ QM tools)
- OHMind-Multiwfn (16 analysis tools)
- OHMind-GROMACS (25+ MD tools)

#### `/status`

Display current system status.

```
/status
```

Shows:
- Connected agents
- Active MCP servers
- RAG system status

#### `/history`

Display recent conversation history.

```
/history
```

Shows the last 10 messages with role indicators (User/AI).

### Export Commands

#### `/export`

Open the export dialog to choose export format.

```
/export
```

Presents options:
- Markdown (.md)
- HTML (.html)
- Screenshot (.svg)

#### `/export md`

Export chat history directly to Markdown format.

```
/export md
```

Creates a file named `ohmind_chat_YYYYMMDD_HHMMSS.md` in the current directory.

#### `/export html`

Export chat history directly to styled HTML format.

```
/export html
```

Creates a file named `ohmind_chat_YYYYMMDD_HHMMSS.html` with embedded CSS styling.

### Debug Commands

#### `/debug`

Toggle debug mode on/off.

```
/debug
```

When enabled:
- Verbose logging to console
- Detailed error messages
- Agent state information

## Usage Examples

### Starting a Research Session

```
# Check system status
/status

# View available tools
/tools

# Start asking questions
What backbones are available for HEM design?
```

### Exporting Results

```
# After a productive session
/export md

# Or use the dialog
/export
```

### Troubleshooting

```
# Enable debug mode
/debug

# Check available agents
/agents

# Clear and restart
/clear
```

### Quick Navigation

```
# Get help anytime
/help

# View conversation history
/history

# Exit when done
/quit
```

## Command Summary Table

| Command | Aliases | Description |
|---------|---------|-------------|
| `/help` | `/?` | Show help screen |
| `/quit` | `/exit`, `/q` | Exit application |
| `/clear` | - | Clear conversation |
| `/new` | - | Start new conversation |
| `/agents` | - | List available agents |
| `/tools` | - | List MCP tools |
| `/status` | - | Show system status |
| `/history` | - | Show message history |
| `/export` | - | Open export dialog |
| `/export md` | - | Export to Markdown |
| `/export html` | - | Export to HTML |
| `/debug` | - | Toggle debug mode |

## See Also

- [CLI Overview](./index.md) - Getting started with the CLI
- [Keyboard Shortcuts](./keyboard-shortcuts.md) - Keyboard-based navigation
- [Workspace Sidebar](./workspace-sidebar.md) - File browser features

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
