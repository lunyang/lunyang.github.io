---
title: "First Steps"
description: "Your first interaction with OHMind - basic workflows and examples"
category: "getting-started"
tags: ["tutorial", "first-steps", "workflow", "examples"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# First Steps with OHMind

> Learn the basics of interacting with OHMind through practical examples

This guide walks you through your first interactions with OHMind, introducing the main interfaces and basic workflows.

## Table of Contents

- [Choosing an Interface](#choosing-an-interface)
- [Starting OHMind](#starting-ohmind)
- [Your First Conversation](#your-first-conversation)
- [Understanding Agent Responses](#understanding-agent-responses)
- [Basic Workflows](#basic-workflows)
- [Working with Results](#working-with-results)
- [Next Steps](#next-steps)

## Choosing an Interface

OHMind provides three ways to interact with the system:

| Interface | Best For | Start Command |
|-----------|----------|---------------|
| **CLI (TUI)** | Terminal users, quick queries, file preview | `./start_OHMind_cli.sh` |
| **Web UI** | Browser-based access, visual workflows | `./start_apps.sh` |
| **API** | Programmatic integration, automation | Direct HTTP calls |

### CLI Features

The terminal user interface (TUI) provides:
- Real-time streaming responses
- Workspace file browser with preview
- Syntax highlighting for code and data files
- Export to Markdown, HTML, or SVG
- Keyboard shortcuts for efficiency

### Web UI Features

The Chainlit-based web interface offers:
- Browser-based access from any device
- Visual chat profiles for different workflows
- MCP server management panel
- User authentication and session persistence

## Starting OHMind

### Option 1: CLI (Recommended for First-Time Users)

```bash
cd OHMind
./start_OHMind_cli.sh
```

The CLI will:
1. Activate the OHMind conda environment
2. Set up environment variables
3. Connect to MCP servers
4. Display the interactive chat interface

### Option 2: Web UI

```bash
cd OHMind
./start_apps.sh
```

Then open `http://localhost:8000` in your browser.

Default credentials:
- Username: `admin`
- Password: `admin`

### Option 3: Backend Only (for API Access)

```bash
cd OHMind
uvicorn app:app --host 0.0.0.0 --port 8005
```

## Your First Conversation

### Simple Chemistry Query

Start with a basic chemistry question to verify the system is working:

```
What is the molecular formula and weight of caffeine?
```

**Expected Response:**

The system will:
1. Route your query to the Chemistry agent
2. Use the `Name2Smiles` tool to get caffeine's SMILES
3. Calculate molecular properties
4. Return: C₈H₁₀N₄O₂, ~194.19 g/mol

### Understanding the Response

OHMind responses typically include:
- **Agent identification**: Which agent handled your query
- **Tool calls**: What MCP tools were used
- **Results**: The actual answer to your question
- **Context**: Additional relevant information

## Understanding Agent Responses

### Agent Routing

The Supervisor agent automatically routes queries to specialized agents:

| Query Type | Agent | Example |
|------------|-------|---------|
| Molecular properties | Chemistry | "What functional groups are in aspirin?" |
| HEM optimization | HEM | "Design cations for PBF_BB_1 backbone" |
| QM calculations | QM | "Calculate LUMO energy for this cation" |
| MD simulations | MD | "Simulate polymer at 400K" |
| Wavefunction analysis | Multiwfn | "Analyze charge distribution" |
| Literature search | RAG | "Find papers on alkaline stability" |
| General web info | Web Search | "Latest research on AEMs" |

### Tool Execution Indicators

In the CLI, you'll see visual indicators when tools are executed:

```
🔧 Calling: MoleculeWeight
   Input: {"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"}
   Result: 194.19
```

### Streaming Responses

Both CLI and Web UI support streaming, so you see responses as they're generated rather than waiting for completion.

## Basic Workflows

### Workflow 1: Molecular Analysis

Analyze a molecule's properties and structure:

```
Analyze the molecule with SMILES "CC(=O)OC1=CC=CC=C1C(=O)O" (aspirin).
Tell me its:
1. Molecular weight and formula
2. Functional groups present
3. A brief description of its structure
```

**What Happens:**
1. Chemistry agent receives the query
2. Multiple tools are called: `MoleculeWeight`, `Smiles2Formula`, `FunctionalGroups`, `MoleculeCaptioner`
3. Results are synthesized into a comprehensive response

### Workflow 2: HEM Design Query

Ask about HEM design capabilities:

```
What backbones and cation types are available for HEM optimization?
```

**What Happens:**
1. HEM agent receives the query
2. `ListBackbones` and `ListCations` tools are called
3. Available options are presented with descriptions

### Workflow 3: Literature Search

Search for relevant scientific literature:

```
Find recent research on improving alkaline stability of quaternary ammonium cations in AEMs.
```

**What Happens:**
1. RAG agent searches the vector database
2. Relevant papers and findings are retrieved
3. A summary of key insights is provided

### Workflow 4: Multi-Step Analysis

For complex queries, OHMind creates a task plan:

```
For the cation SMILES "C[N+]1(C)CCCCC1":
1. Validate the SMILES
2. Calculate its molecular properties
3. Identify functional groups
4. Suggest potential modifications for improved stability
```

**What Happens:**
1. Supervisor detects a complex query
2. A task plan is created with multiple steps
3. Each step is executed in sequence
4. Results are compiled into a final response

## Working with Results

### Viewing Generated Files

When OHMind runs calculations, results are saved to the workspace:

**In CLI:**
- Use the sidebar (toggle with `Ctrl+B`) to browse files
- Click on files to preview them
- Supports syntax highlighting for code and data files

**In Web UI:**
- Results are displayed inline when possible
- File paths are provided for larger outputs

### Workspace Structure

Results are organized by domain:

```
OHMind_workspace/
├── HEM/           # Optimization results
│   ├── best_solutions_*.csv
│   └── optimization_*.log
├── QM/            # QM calculation outputs
│   └── results/
├── MD/            # MD simulation files
│   ├── *.gro
│   └── *.xtc
└── Multiwfn/      # Wavefunction analysis
    └── *.cube
```

### Exporting Conversations

**CLI Export Options:**
- `Ctrl+E` or `/export` - Export current conversation
- Formats: Markdown, HTML, SVG screenshot

**Web UI:**
- Use the export button in the chat interface

## CLI Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Toggle workspace sidebar |
| `Ctrl+L` | Clear chat history |
| `Ctrl+E` | Export conversation |
| `Ctrl+C` | Cancel current operation |
| `Enter` | Send message |
| `Shift+Enter` | New line in message |

## Common First-Time Questions

### "How do I know which agent is handling my query?"

The response will indicate which agent processed your request. In the CLI, you'll see agent-specific icons and colors.

### "Can I specify which agent to use?"

Yes, you can mention the domain explicitly:
- "Using your chemistry tools, analyze..."
- "With your HEM optimization capabilities, design..."

### "What if a tool fails?"

The system will:
1. Report the error
2. Attempt alternative approaches if available
3. Provide guidance on how to resolve the issue

### "How long do calculations take?"

| Operation | Typical Time |
|-----------|--------------|
| Molecular properties | < 1 second |
| HEM optimization (10 steps) | 5-15 minutes |
| QM geometry optimization | 10-60 minutes |
| MD simulation (short) | 30+ minutes |

## Example Session

Here's a complete example session demonstrating basic usage:

```
You: What is the molecular weight of benzene?

OHMind: The molecular weight of benzene (SMILES: c1ccccc1) is 78.11 g/mol.

You: Now compare it to toluene - what's the difference?

OHMind: Comparing benzene and toluene:
- Benzene (C₆H₆): 78.11 g/mol
- Toluene (C₇H₈): 92.14 g/mol
- Difference: 14.03 g/mol (one CH₃ group)

Toluene is benzene with a methyl group attached, which accounts for 
the mass difference of approximately one carbon and three hydrogens.

You: What functional groups does toluene have?

OHMind: Toluene contains the following functional groups:
- Aromatic ring (benzene ring)
- Methyl group (alkyl substituent)

The molecule is classified as a methylbenzene or aromatic hydrocarbon.
```

## Next Steps

Now that you're familiar with basic interactions, explore these topics:

| Goal | Resource |
|------|----------|
| Run HEM optimization | [HEM Optimization Tutorial](../tutorials/hem-optimization.md) |
| Perform QM calculations | [QM Calculations Tutorial](../tutorials/qm-calculations.md) |
| Understand the architecture | [Architecture Overview](../architecture/overview.md) |
| Learn about agents | [Agent Reference](../agents/index.md) |
| Configure the system | [Configuration Guide](../configuration/index.md) |

## See Also

- [Quick Start Guide](./quick-start.md) - Installation overview
- [Installation Guide](./installation.md) - Detailed setup instructions
- [CLI Documentation](../cli/index.md) - Full CLI reference
- [Tutorials](../tutorials/index.md) - Step-by-step guides

---

*Last updated: 2025-12-22 | OHMind v1.0.0*
