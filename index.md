---
title: "OHMind Documentation"
description: "Comprehensive documentation for OHMind - A Language-Model Multi-Agent Framework for Accelerating Hydroxide Exchange Membrane Discovery"
category: "index"
tags: ["ohmind", "hem", "multi-agent", "documentation"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# OHMind Documentation

> A Language-Model Multi-Agent Framework for Accelerating Hydroxide Exchange Membrane (HEM) Discovery

Welcome to the OHMind documentation. This guide provides comprehensive information for researchers, developers, and administrators working with the OHMind platform for AI-driven cation design and HEM workflows.

## Table of Contents

- [Overview](#overview)
- [System Components](#system-components)
- [Architecture Highlights](#architecture-highlights)
- [Documentation Chapters](#documentation-chapters)
- [Quick Links](#quick-links)

## Overview

**OHMind** is developed by the PolyAI team from the Changchun Institute of Applied Chemistry, Chinese Academy of Sciences. It combines advanced machine learning models with domain-specific computational chemistry tools to accelerate the discovery of high-performance hydroxide exchange membranes.

The platform integrates:
- **Generative molecular design** using Junction Tree Variational Autoencoders (JT-VAE)
- **Multi-objective optimization** via Particle Swarm Optimization (PSO)
- **Quantum chemistry calculations** through ORCA integration
- **Molecular dynamics simulations** via GROMACS
- **Wavefunction analysis** using Multiwfn
- **Literature retrieval** through RAG-based search

## System Components

OHMind consists of five main components:

| Component | Directory | Description |
|-----------|-----------|-------------|
| **Core Library** | `OHMind/` | VAE models, PSO optimization, QM/MD integration, reaction models, and HEM property prediction |
| **Multi-Agent System** | `OHMind_agent/` | LangGraph-based multi-agent orchestration with 8 specialized agents |
| **CLI Application** | `OHMind_cli/` | Textual-based TUI for interactive agent communication |
| **Web UI** | `OHMind_ui/` | Chainlit + LangGraph frontend for browser-based access |
| **MCP Servers** | `OHMind_agent/MCP/` | Five domain-specific servers (Chemistry, ORCA, Multiwfn, GROMACS, HEMDesign) |

## Architecture Highlights

- **LangGraph Workflow**: Supervisor pattern with conditional routing and task planning
- **MCP Integration**: Model Context Protocol for tool access via `langchain-mcp-adapters`
- **Persistent Sessions**: Long-lived MCP connections for efficient tool execution
- **Task Planning**: Automatic decomposition of complex queries into multi-step execution plans
- **RAG System**: Qdrant-based vector search for HEM literature retrieval
- **Streaming Interface**: Real-time token streaming with agent activity visualization

## Documentation Chapters

### Getting Started
- [Quick Start Guide](./getting-started/quick-start.md) - Get OHMind running in 10 minutes
- [Installation](./getting-started/installation.md) - Detailed installation instructions
- [First Steps](./getting-started/first-steps.md) - Your first interaction with OHMind

### Architecture
- [System Overview](./architecture/overview.md) - High-level system architecture
- [Multi-Agent System](./architecture/multi-agent-system.md) - Agent workflow and routing
- [State Management](./architecture/state-management.md) - AgentState and data flow
- [MCP Integration](./architecture/mcp-integration.md) - MCP protocol and servers

### Agent Reference
- [Agent Overview](./agents/index.md) - Introduction to OHMind agents
- [Supervisor Agent](./agents/supervisor.md) - Central coordinator and task planning
- [HEM Agent](./agents/hem-agent.md) - HEM design and PSO optimization
- [Chemistry Agent](./agents/chemistry-agent.md) - Molecular operations
- [QM Agent](./agents/qm-agent.md) - Quantum chemistry via ORCA
- [MD Agent](./agents/md-agent.md) - Molecular dynamics via GROMACS
- [Multiwfn Agent](./agents/multiwfn-agent.md) - Wavefunction analysis
- [RAG Agent](./agents/rag-agent.md) - Literature search
- [Web Search Agent](./agents/web-search-agent.md) - Real-time web information

### MCP Server Reference
- [MCP Overview](./mcp-servers/index.md) - Introduction to MCP servers
- [Chemistry Server](./mcp-servers/chem-server.md) - SMILES operations, molecular properties
- [HEMDesign Server](./mcp-servers/hem-server.md) - PSO optimization, job management
- [ORCA Server](./mcp-servers/orca-server.md) - QM calculations
- [Multiwfn Server](./mcp-servers/multiwfn-server.md) - Wavefunction analysis
- [GROMACS Server](./mcp-servers/gromacs-server.md) - MD simulations

### Core Library
- [Library Overview](./core-library/index.md) - Core library modules
- [OHVAE](./core-library/ohvae.md) - Junction Tree VAE
- [OHPSO](./core-library/ohpso.md) - Particle Swarm Optimization
- [OHQM](./core-library/ohqm.md) - Quantum chemistry utilities
- [OHMD](./core-library/ohmd.md) - Molecular dynamics utilities
- [OHScore](./core-library/ohscore.md) - Property prediction

### CLI Application
- [CLI Overview](./cli/index.md) - Terminal user interface
- [Commands](./cli/commands.md) - Slash commands reference
- [Keyboard Shortcuts](./cli/keyboard-shortcuts.md) - Keyboard shortcuts
- [Workspace Sidebar](./cli/workspace-sidebar.md) - File browser and preview
- [Themes](./cli/themes.md) - Theme customization
- [Web Deployment](./cli/web-deployment.md) - textual-serve deployment

### Configuration
- [Configuration Overview](./configuration/index.md) - Configuration files
- [Environment Variables](./configuration/environment-variables.md) - All environment variables
- [MCP Configuration](./configuration/mcp-config.md) - mcp.json format
- [LLM Providers](./configuration/llm-providers.md) - LLM provider setup
- [Workspace Setup](./configuration/workspace-setup.md) - Directory structure

### Tutorials
- [Tutorial Overview](./tutorials/index.md) - Available tutorials
- [HEM Optimization](./tutorials/hem-optimization.md) - HEM design tutorial
- [QM Calculations](./tutorials/qm-calculations.md) - ORCA QM tutorial
- [MD Simulations](./tutorials/md-simulations.md) - GROMACS MD tutorial
- [Literature Search](./tutorials/literature-search.md) - RAG search tutorial
- [Multi-Step Workflows](./tutorials/multi-step-workflows.md) - Complex workflow tutorial

### API Reference
- [API Overview](./api/index.md) - API documentation
- [Backend API](./api/backend-api.md) - FastAPI endpoints
- [Workflow API](./api/workflow-api.md) - LangGraph workflow
- [Session Manager](./api/session-manager.md) - MCP session management

### Troubleshooting
- [Troubleshooting Overview](./troubleshooting/index.md) - Common issues
- [Installation Issues](./troubleshooting/installation-issues.md) - Installation problems
- [MCP Issues](./troubleshooting/mcp-issues.md) - MCP server issues
- [LLM Issues](./troubleshooting/llm-issues.md) - LLM provider issues
- [External Software](./troubleshooting/external-software.md) - ORCA/GROMACS/Multiwfn issues

## Quick Links

| Task | Link |
|------|------|
| **Install OHMind** | [Quick Start Guide](./getting-started/quick-start.md) |
| **Run HEM optimization** | [HEM Optimization Tutorial](./tutorials/hem-optimization.md) |
| **Configure MCP servers** | [MCP Configuration](./configuration/mcp-config.md) |
| **Troubleshoot issues** | [Troubleshooting Overview](./troubleshooting/index.md) |
| **API integration** | [API Overview](./api/index.md) |

## MCP Server Quick Reference

| Server | Tools | Purpose |
|--------|-------|---------|
| `OHMind-Chem` | 17+ | SMILES operations, functional groups, molecular properties |
| `OHMind-HEMDesign` | 7 | PSO optimization, backbone/cation management, job control |
| `OHMind-ORCA` | 10+ | QM calculations, geometry optimization, properties |
| `OHMind-Multiwfn` | 16 | Wavefunction analysis, orbital visualization, electron density |
| `OHMind-GROMACS` | 25+ | MD simulations, system preparation, trajectory analysis |

## Getting Help

- **Issues**: Report bugs and feature requests on the project repository
- **Documentation**: This documentation is continuously updated
- **Community**: Join discussions with other OHMind users

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
