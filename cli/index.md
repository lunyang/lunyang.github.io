---
title: "CLI Application"
description: "OHMind Terminal User Interface (TUI) - Interactive chat interface for HEM design"
category: "cli"
tags: ["cli", "tui", "textual", "terminal", "interface"]
last_updated: "2025-12-23"
version: "1.0.0"
nav_order: 8
has_children: true
---

# CLI Application

> Modern terminal user interface for interacting with the OHMind multi-agent system

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Interface Layout](#interface-layout)
- [Quick Reference](#quick-reference)
- [See Also](#see-also)

## Overview

The OHMind CLI is a Textual-based Terminal User Interface (TUI) that provides an interactive chat experience with the HEM Design Multi-Agent System. Built with Python's Textual framework, it offers a rich, responsive interface directly in your terminal.

The CLI connects directly to MCP servers without requiring the FastAPI backend, making it ideal for local development and research workflows.

## Features

### Interactive Chat
- Real-time streaming responses from AI agents
- Agent-specific styling with icons and colors
- Markdown rendering for formatted responses
- Tool call visualization showing agent activity

### Workspace Sidebar
- Live directory tree of generated files
- File preview with syntax highlighting
- Image file information display
- Resizable sidebar with drag-to-resize splitter

### Export Functionality
- Export chat history to Markdown format
- Export chat history to styled HTML
- Screenshot capture to SVG format

### Keyboard-Driven Interface
- Comprehensive keyboard shortcuts for all actions
- Slash commands for quick operations
- Focus management for efficient navigation

### Theming
- Multiple built-in scientific themes
- Galaxy-inspired color palette
- Agent-specific color coding

## Getting Started

### Starting the CLI

```bash
# Navigate to OHMind directory
cd OHMind

# Start the CLI application
./start_OHMind_cli.sh
```

Or run directly with Python:

```bash
python -m OHMind_cli
```

### Command Line Options

```bash
# Enable debug logging
python -m OHMind_cli --debug

# Show version
python -m OHMind_cli --version

# Deploy as web application
python -m OHMind_cli deploy --host 0.0.0.0 --port 8000
```

### First Interaction

1. Wait for system initialization (RAG, MCP servers, workflow)
2. Type your question in the input field at the bottom
3. Press Enter to send
4. Watch streaming responses from specialized agents

## Interface Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Header: OHMind - HEM Design Multi-Agent System                 │
├─────────────────────┬───────────────────────────────────────────┤
│                     │                                           │
│  Workspace Sidebar  │  Chat View                                │
│  (File Browser)     │  - Welcome message                        │
│                     │  - User prompts                           │
│  📁 HEM/            │  - Agent responses                        │
│  📁 QM/             │  - Tool call indicators                   │
│  📁 MD/             │  - System messages                        │
│                     │                                           │
├─────────────────────┴───────────────────────────────────────────┤
│  Input: Ask about HEM design, chemistry, QM, or MD...           │
├─────────────────────────────────────────────────────────────────┤
│  Footer: Ctrl+C Quit | Ctrl+L Clear | Ctrl+B Files | F1 Help    │
└─────────────────────────────────────────────────────────────────┘
```

### Components

| Component | Description |
|-----------|-------------|
| Header | Application title and subtitle |
| Sidebar | Workspace directory tree with file browser |
| Splitter | Draggable divider to resize sidebar |
| Chat View | Scrollable area for conversation |
| Input | Text input for user messages |
| Footer | Keyboard shortcut hints |

## Quick Reference

### Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Quit application |
| `Ctrl+L` | Clear conversation |
| `Ctrl+B` | Toggle sidebar |
| `Ctrl+E` | Export chat |
| `F1` | Show help |

### Essential Commands

| Command | Action |
|---------|--------|
| `/help` | Show help screen |
| `/clear` | Clear conversation |
| `/export` | Export dialog |
| `/quit` | Exit application |

### Agent Icons

| Icon | Agent | Domain |
|------|-------|--------|
| 👑 | Supervisor | Task routing and planning |
| 🧬 | HEM | Membrane design and optimization |
| 🧪 | Chemistry | SMILES and molecular properties |
| ⚛️ | QM | Quantum chemistry calculations |
| 💻 | MD | Molecular dynamics simulations |
| 📊 | Multiwfn | Wavefunction analysis |
| 📚 | RAG | Literature search |
| 🌐 | Web Search | External resources |

## See Also

- [Commands Reference](./commands.md) - Complete slash command documentation
- [Keyboard Shortcuts](./keyboard-shortcuts.md) - All keyboard shortcuts
- [Workspace Sidebar](./workspace-sidebar.md) - File browser and preview
- [Themes](./themes.md) - Theme customization
- [Web Deployment](./web-deployment.md) - Deploy as web application

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
