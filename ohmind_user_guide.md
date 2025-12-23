# OHMind User Guide

A practical tutorial for installing, configuring, and using the OHMind platform for AI‑driven cation design and HEM (Hydroxide Exchange Membrane) workflows.

---

## 1. Overview

**OHMind** is a Language-Model Multi-Agent Framework for Accelerating Hydroxide Exchange Membrane (HEM) Discovery, developed by the PolyAI team from the Changchun Institute of Applied Chemistry, Chinese Academy of Sciences.

### System Components

OHMind consists of four main components:

- **Core library** (`OHMind/`): VAE models, PSO optimization, QM/MD integration, reaction models, and HEM property prediction
- **Multi‑agent system** (`OHMind_agent/`): LangGraph-based multi-agent orchestration with 8 specialized agents
- **CLI application** (`OHMind_cli/`): Textual-based TUI for interactive agent communication
- **Web UI** (`OHMind_ui/`): Chainlit + LangGraph frontend for browser-based access
- **MCP servers**: Five domain-specific servers (Chemistry, ORCA, Multiwfn, GROMACS, HEMDesign)

### Architecture Highlights

- **LangGraph Workflow**: Supervisor pattern with conditional routing and task planning
- **MCP Integration**: Model Context Protocol for tool access via `langchain-mcp-adapters`
- **Persistent Sessions**: Long-lived MCP connections for efficient tool execution
- **Task Planning**: Automatic decomposition of complex queries into multi-step execution plans
- **RAG System**: Qdrant-based vector search for HEM literature retrieval
- **Streaming Interface**: Real-time token streaming with agent activity visualization

This guide walks you through:

1. Installation and environment setup
2. System architecture and component interaction
3. Workspace layout and unified result storage
4. Configuring environment variables and MCP servers
5. Starting the backend, CLI, and UI
6. Running typical workflows (especially HEM multi‑agent)
7. Understanding the agent system and task planning
8. Debugging MCP servers and troubleshooting

---

## 2. System Architecture Overview

### 2.1 OHMind_agent - Multi-Agent System

The `OHMind_agent` directory implements a LangGraph-based multi-agent architecture with:

#### Agent Graph Structure
- **StateGraph**: Manages conversation flow and agent state
- **Supervisor Agent**: Central coordinator with complexity detection and task planning
- **8 Specialized Agents**:
  - `hem_agent`: HEM design & PSO optimization
  - `chemistry_agent`: Molecular operations & SMILES handling
  - `qm_agent`: Quantum chemistry via ORCA
  - `md_agent`: Molecular dynamics via GROMACS
  - `multiwfn_agent`: Wavefunction analysis
  - `rag_agent`: Scientific literature search
  - `web_search_agent`: Real-time web information
  - `summary_agent`: Summarizes results from the agent system

#### Key Features
- **Task Planning**: Auto-detects complex queries and creates multi-step execution plans
- **Conditional Routing**: `route_after_agent()` handles transitions between agents
- **Streaming Support**: Real-time token streaming with callback handlers
- **State Management**: Shared `AgentState` dictionary tracks messages, MCP results, and task progress

#### MCP Session Management
- **Persistent Connections**: Uses `MultiServerMCPClient` from `langchain-mcp-adapters`
- **Transport Support**: Both `stdio` and `streamable_http` transports
- **Tool Distribution**: Session manager loads and distributes tools to agents by server
- **Long-lived Sessions**: Context managers kept active to maintain tool references

### 2.2 OHMind_cli - Terminal User Interface

The `OHMind_cli` directory provides a Textual-based TUI with:

#### Main Features
- **Resizable Sidebar**: Workspace file browser with drag-to-resize
- **File Preview**: Text (with syntax highlighting) and image preview modals
- **Agent Visualization**: Galaxy-themed colors and icons for each agent
- **Export**: Markdown, HTML, and SVG screenshot export

#### Custom Widgets
- `TextPreview`: Syntax highlighting for Python, JSON, YAML, etc.
- `SidebarSplitter`: Draggable divider for resizing sidebar
- `WorkspaceSidebar`: Filtered directory tree for workspace files
- `StreamingMessage`: Real-time token display with cursor indicator
- `ToolCallWidget`: Visual indicators for tool execution

#### Callback System
- `TextualCallbackHandler`: Captures LLM tokens and tool events
- Integrates with LangChain/LangGraph callbacks
- Updates UI in real-time during agent execution

### 2.3 MCP Server Architecture

Five domain-specific MCP servers provide tools to agents:

| Server | Location | Tool Count | Purpose |
|--------|----------|------------|---------|
| Chem | `MCP/Chem/` | 18 | SMILES operations, functional groups, molecular properties |
| HEMDesign | `MCP/HEMDesign/` | 7 | PSO optimization, backbone/cation management, job control |
| ORCA | `MCP/ORCA/` | 10+ | QM calculations, geometry optimization, properties |
| Multiwfn | `MCP/Multiwfn/` | 14 | Wavefunction analysis, orbital visualization, electron density |
| GROMACS | `MCP/GROMACS/` | 30+ | MD simulations, system preparation, trajectory analysis |

Each server implements:
- Tool discovery via MCP protocol
- Input validation and error handling
- Result storage in unified workspace
- Progress monitoring for long-running jobs

---

## 3. Installation & Environment

### 3.1 Prerequisites

- Linux (tested on Ubuntu‑like systems)
- Conda (Anaconda or Miniconda)
- GPU with CUDA (recommended for VAE models)
- Python 3.10+ (specified in environment.yml)
- Optional but recommended external tools:
  - [ORCA](https://orcaforum.kofo.mpg.de/app.php/portal) – quantum chemistry calculations
  - [Multiwfn](http://sobereva.com/multiwfn/) – wavefunction analysis
  - GROMACS – molecular dynamics simulations
  - Qdrant – vector database for RAG
  - PostgreSQL + MinIO – used by the Chainlit UI

### 3.2 Create the Conda Environment

From the project root:

```bash
cd ./OHMind

# Create the OHMind environment (uses environment.yml)
conda env create -f environment.yml

# Activate it
conda activate OHMind
```

> The `environment.yml` file includes all Python dependencies:
> - LangChain + LangGraph for agent orchestration
> - PyTorch, DGL for VAE models
> - RDKit for cheminformatics
> - FastAPI, Chainlit for web interfaces
> - Textual for TUI
> - langchain-mcp-adapters for MCP integration

### 3.3 External Software Paths

You will need to know where the following are installed on your system:

- `OHMind_ORCA` – full path to the ORCA binary
- `OHMind_MPI` – directory containing MPI binaries (e.g. `mpirun`)
- `MULTIWFN_PATH` – full path to the Multiwfn executable
- GROMACS – available on your `$PATH` (e.g. after `source gmxtools.sh`)

These are configured via environment variables (see **Section 4**).

---

## 4. Unified Workspace Layout

All heavy computation (QM, MD, PSO/HEM, Multiwfn) is organized under a **single workspace root**.

### 4.1 Workspace Root

The unified root is controlled by the environment variable:

- `OHMind_workspace`

In this project it is typically set to:

```bash
OHMind_workspace=/OHMind_workspace
```

This is defined in:

- Root `.env`
- `OHMind_agent/.env`
- `start_apps.sh` (fallback default `${ROOT_DIR}_workspace`)

### 4.2 Subdirectory Layout

Under `OHMind_workspace`, subdirectories are used for each domain:

```text
OHMind_workspace/
├── HEM/        # PSO / HEMDesign optimization results (CSV, logs, etc.)
├── QM/         # ORCA QM temporary and result files
├── MD/         # GROMACS MD simulations and outputs
└── Multiwfn/   # Multiwfn wavefunction analysis outputs
```

The corresponding environment variables are:

- `HEM_SAVE_PATH = ${OHMind_workspace}/HEM`
- `QM_WORK_DIR   = ${OHMind_workspace}/ORCA`
- `MD_WORK_DIR   = ${OHMind_workspace}/GROMACS`
- `MULTIWFN_WORK_DIR = ${OHMind_workspace}/Multiwfn`
- `WORKSPACE_ROOT = ${OHMind_workspace}` (generic root for backend code)

These are exported by:

- `.env` and `OHMind_agent/.env`
- `start_apps.sh`, which sets sensible defaults if variables are not pre‑set.

### 4.3 How `start_apps.sh` Sets Workspace Paths

From the project root:

```bash
./start_apps.sh
```

Internally, the script does (simplified):

```bash
export OHMind_workspace="${OHMind_workspace:-${ROOT_DIR}_workspace}"
export HEM_SAVE_PATH="${HEM_SAVE_PATH:-${OHMind_workspace}/HEM}"
export QM_WORK_DIR="${QM_WORK_DIR:-${OHMind_workspace}/ORCA}"
export MD_WORK_DIR="${MD_WORK_DIR:-${OHMind_workspace}/GROMACS}"
export MULTIWFN_WORK_DIR="${MULTIWFN_WORK_DIR:-${OHMind_workspace}/Multiwfn}"
```

So if you **do nothing**, it will create/use `${ROOT_DIR}_workspace` with the described subfolders. If you prefer a specific location, set `OHMind_workspace` before running the script.

---

## 5. Environment Variables & Configuration

### 5.1 Core `.env` (project root)

The root `.env` controls the multi‑agent FastAPI backend (`app.py`).
Key entries:

- LLM configuration (OpenAI‑compatible via `OPENAI_COMPATIBLE_*`)
- Qdrant URL: `QDRANT_URL`, `QDRANT_API_KEY`
- Web search: `TAVILY_API_KEY`
- MCP config: `MCP_CONFIG_PATH=/OHMind/mcp.json`
- Workspace:
  - `OHMind_workspace=/OHMind_workspace`
  - `HEM_SAVE_PATH=${OHMind_workspace}/HEM`
  - `WORKSPACE_ROOT=${OHMind_workspace}`

The backend reads these via `OHMind_agent.config.Settings` (Pydantic-based configuration management).

### 5.2 `OHMind_agent/.env`

This file is used when running the multi‑agent backend or MCP servers directly from `OHMind_agent`. It includes:

- `MCP_CONFIG_PATH` – usually the same root `mcp.json`
- `OHMind_workspace`, `HEM_SAVE_PATH`, `WORKSPACE_ROOT` – as above

### 5.3 UI `.env` (`OHMind_ui/.env`)

This configures the Chainlit + LangGraph UI:

- Logging level
- Auth (default admin user/password)
- Postgres connection
- MinIO settings
- LLM provider keys (OpenAI, Anthropic, etc.)

The UI obtains MCP server details from `OHMind_ui/.chainlit/mcp.json` (documentation only; Chainlit currently requires manual entry via the UI).

### 5.4 CLI Launch (`start_OHMind_cli.sh`)

To start the terminal user interface (TUI):

```bash
cd /OHMind
./start_OHMind_cli.sh
```

This script:
- Activates the `OHMind` conda environment
- Sets `PYTHONPATH` to the project root
- Exports workspace environment variables
- Launches `OHMind_cli` TUI application

The CLI connects to the same MCP servers as the web UI but provides a terminal-based interface with:
- Real-time streaming display
- Workspace file browser with preview
- Export to Markdown/HTML/SVG

### 5.5 MCP Configuration Files

There are two important JSON files describing MCP servers:

1. **Backend MCP config**: `mcp.json` (in project root)
   - Used by the multi‑agent backend via `OHMind_agent.config.mcp_config_path`
   - Paths in `env` now use the unified workspace layout:
     - `QM_WORK_DIR = OHMind_workspace/ORCA`
     - `MD_WORK_DIR = OHMind_workspace/GROMACS`
     - `MULTIWFN_WORK_DIR = OHMind_workspace/Multiwfn`
     - `HEM_SAVE_PATH = OHMind_workspace/HEM`

2. **UI MCP config**: `OHMind_ui/.chainlit/mcp.json`
   - Documents how to add MCP servers in Chainlit’s UI.
   - Exhibits the same workspace paths as `mcp.json`.

> The actual MCP processes are started by the backend (multi‑agent system) and by Chainlit (for UI‑side tools). Both now use the same workspace locations.

---

## 6. Starting the Backend, CLI & UI

### 6.1 Using `start_apps.sh` (Web UI, recommended)

From the project root:

```bash
cd OHMind

# Optional overrides
BACKEND_PORT=8005 \   # FastAPI backend port
PYTHON=/home/you/anaconda3/envs/OHMind/bin/python \  # Python binary
./start_apps.sh
```

This script:

- Exports `PYTHONPATH` pointing at the repo root
- Loads `OHMind_ui/.env` (for UI configuration)
- Sets `OHMind_workspace` and all derived working directories
- Starts the FastAPI backend (`app.py`) on `http://localhost:${BACKEND_PORT}`
- Writes the backend PID to `.backend.pid`
- Sets `OHMIND_BACKEND_URL` for the UI
- Starts the Chainlit UI on `http://localhost:8000`

### 6.2 Using `start_OHMind_cli.sh` (TUI, alternative)

For a terminal-based interface:

```bash
cd OHMind
./start_OHMind_cli.sh
```

The CLI provides:
- **Interactive chat** with streaming responses
- **Workspace sidebar** showing generated files in real-time
- **File preview** for text (with syntax highlighting) and images
- **Task plan visualization** with step-by-step progress
- **Export functionality** (Markdown, HTML, SVG screenshot)
- **Keyboard shortcuts**: `Ctrl+B` (toggle sidebar), `Ctrl+L` (clear chat), `Ctrl+E` (export)

The TUI connects directly to MCP servers without requiring the FastAPI backend.

### 6.3 Accessing the Web UI

After `start_apps.sh` is running, open:

```text
http://localhost:8000
```

Default login (from `OHMind_ui/.env`):

- User: `admin`
- Password: `admin`

Once logged in, you’ll see multiple workflows, including **HEM Multi‑Agent**.

---

## 7. MCP Servers Configuration (UI Side)

### 7.1 Adding MCP Servers in Chainlit

Chainlit (v2.9.0) does **not** automatically read `OHMind_ui/.chainlit/mcp.json`. Instead, that file documents the servers you should add via the UI.

**Note**: The CLI (`OHMind_cli`) automatically connects to MCP servers via the session manager and does not require manual configuration.

1. Start backend + UI (see Section 6).
2. In the UI, open the **MCP** panel (left sidebar) and click **Add server**.
3. For each server (`OHMind-Chem`, `OHMind-HEMDesign`, `OHMind-ORCA`, `OHMind-Multiwfn`, `OHMind-GROMACS`):
   - **Name**: e.g. `OHMind-ORCA`
   - **Type**: `stdio`
   - **Command**: your Python binary, e.g. `/home/you/anaconda3/envs/OHMind/bin/python`
   - **Args**: e.g. `-m OHMind_agent.MCP.ORCA.server --transport stdio`

Most environment variables (including workspace paths) are already exported by `.env` + `start_apps.sh`, so in many cases you can leave the **Env** section empty.

### 7.2 Manual MCP Server Commands (Debugging)

You can run MCP servers manually to debug issues. Examples:

```bash
# Chem
PYTHONPATH=OHMind \
  TAVILY_API_KEY=tvly-dev-... \
  RDKIT_QUIET=1 \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.Chem.server --transport stdio

# ORCA
PYTHONPATH="OHMind" \
  OHMind_ORCA="/home/you/ORCA/orca" \
  OHMind_MPI="/usr/local/bin" \
  QM_WORK_DIR="OHMind_workspace/QM" \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.ORCA.server

# HEMDesign
PYTHONPATH=OHMind \
  HEM_SAVE_PATH=OHMind_workspace/HEM \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.HEMDesign.server --transport stdio

# Multiwfn
PYTHONPATH=OHMind \
  MULTIWFN_PATH=/home/you/Multiwfn/Multiwfn \
  MULTIWFN_WORK_DIR=OHMind_workspace/Multiwfn \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.Multiwfn.server --transport stdio

# GROMACS
PYTHONPATH=OHMind \
  MD_WORK_DIR=OHMind_workspace/MD \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.GROMACS.server --transport stdio
```

Adapt the paths (`OHMind_ORCA`, `MULTIWFN_PATH`, Conda path) to your system.

### 6.3 HTTP (streamable) MCP servers for IDEs and external clients

When you use the root helper script:

```bash
cd OHMind
./start_OHMind.sh
```

the project also starts **HTTP (streamable-http)** FastMCP servers suitable for
MCP-aware IDE plugins and tools that speak the MCP streamable HTTP protocol.

The default endpoints are:

- `OHMind-Chem`      → `http://127.0.0.1:8101/`
- `OHMind-HEMDesign` → `http://127.0.0.1:8102/`
- `OHMind-ORCA`      → `http://127.0.0.1:8103/`
- `OHMind-Multiwfn`  → `http://127.0.0.1:8104/`
- `OHMind-GROMACS`   → `http://127.0.0.1:8105/`

Each server uses FastMCP's **streamable HTTP transport** with
`streamable_http_path="/"`, so the MCP endpoint lives at the **root path**. In
other words, external MCP clients should connect directly to the base URL
without appending `/mcp`.

A typical HTTP-style MCP client config entry (pseudocode) looks like:

```jsonc
"OHMind-Chem-HTTP": {
  "type": "http",
  "url": "http://127.0.0.1:8101/",
  "disabled": false
}
```

with analogous entries for `OHMind-HEMDesign-HTTP`, `OHMind-ORCA-HTTP`,
`OHMind-Multiwfn-HTTP`, and `OHMind-GROMACS-HTTP` using the ports above.

The **stdio** and **HTTP** transports are independent and can be used in
parallel: Chainlit typically uses stdio-based servers (Sections 6.1–6.2), while
IDE plugins or external MCP clients can connect to the HTTP endpoints exposed
by `start_OHMind.sh`.

---

## 7. Using the HEM Multi‑Agent Workflow

The most prominent workflow is the **HEM Multi‑Agent** system exposed via the backend and UI.

### 7.1 High‑Level Architecture

- **Supervisor agent** orchestrates:
  - **HEM agent** (PSO cation design)
  - **Chemistry agent** (general chemical reasoning)
  - **QM agent** (ORCA jobs)
  - **MD agent** (GROMACS jobs)
  - **RAG agent** (literature retrieval)
  - **Web search agent**
  - **Validation agent**

MCP servers provide tools to these agents, and all heavy computations are stored under `OHMind_workspace`.

### 7.2 Running a HEM Design Session

1. Start backend + UI (Section 5).
2. In the UI, select the **HEM Multi‑Agent** chat profile.
3. Ensure the **HEM backend URL** in chat settings points to your backend (e.g. `http://localhost:8005`).
4. Ask a design question, for example:

   > "Design new piperidinium-based cations for PBF_BB_1 backbone optimizing multi‑objective HEM performance."

5. The system will:
   - Parse your request
   - Call HEMDesign MCP tools (`optimize_hem_design`, etc.)
   - Run PSO optimization and log to `HEM_SAVE_PATH` (under `HEM/`)
   - Optionally invoke QM, MD, or Multiwfn tools as needed
   - Stream back intermediate and final results in the UI

### 7.3 Inspecting Results

- Optimization logs and CSVs are stored in:

  ```text
  OHMind_workspace/HEM
  ├── best_solutions_<BACKBONE>_<CATION>.csv
  ├── best_fitness_history_<BACKBONE>_<CATION>.csv
  └── optimization_<BACKBONE>_<CATION>.log
  ```

- QM and MD calculations write into their respective subdirectories:
  - `OHMind_workspace/QM` (with `results/` inside)
  - `OHMind_workspace/MD`

- Multiwfn analyses create folders under:
  - `OHMind_workspace/Multiwfn/<job-name>/...`

---

## 8. Troubleshooting

### 8.1 Workspace & Permissions

**Symptom:** Tools complain about missing directories or permission errors.

- Ensure the workspace root exists and is writable:

  ```bash
  mkdir -p OHMind_workspace
  chmod u+rwx OHMind_workspace
  ```

- Likewise ensure subdirectories exist (they are often auto‑created, but you can create them manually):

  ```bash
  mkdir -p "$OHMind_workspace"/HEM "$OHMind_workspace"/QM \
           "$OHMind_workspace"/MD "$OHMind_workspace"/Multiwfn
  ```

### 8.2 MCP Server Not Connecting in UI

**Symptom:** Chainlit shows MCP server connection errors.

- Check that `PYTHONPATH` and all required env vars are set (use the manual commands in Section 6.2 to test).
- Verify that the Python binary in the **Command** field is the same as your `OHMind` environment Python.
- Check for missing dependencies in that environment (e.g. `rdkit`, `pydantic`, `mcp`).

### 8.3 Backend Not Responding / 5xx Errors

- Check if the backend is running:

  ```bash
  ps aux | grep "python app.py"
  ```

- Inspect the backend log:

  ```bash
  cd OHMind
  tail -n 200 backend.log
  ```

- Look for errors related to:
  - Qdrant connectivity (`QDRANT_URL`)
  - LLM provider keys
  - MCP config path (`MCP_CONFIG_PATH`)

### 8.4 ORCA / QM Issues

**Common issues:**

- `OHMind_ORCA` path incorrect
- `QM_WORK_DIR` not writable

Check:

```bash
which orca
ls "$QM_WORK_DIR"
```

Update paths in `.env`, `mcp.json`, or shell as needed.

### 8.5 GROMACS / MD Issues

Ensure GROMACS binaries are available on the PATH and that `MD_WORK_DIR` exists. Check the GROMACS MCP README at:

```text
OHMind_agent/MCP/GROMACS/README.md
```

### 8.6 Multiwfn Issues

- Confirm `MULTIWFN_PATH` points to the Multiwfn executable.
- Confirm `MULTIWFN_WORK_DIR` is a writable directory (under `OHMind_workspace/Multiwfn`).

---

## 9. Quick Checklist

1. **Environment**
   - [ ] `conda env create -f environment.yml`
   - [ ] `conda activate OHMind`

2. **Workspace**
   - [ ] `OHMind_workspace` set (or rely on `start_apps.sh` default)
   - [ ] Writable: `HEM`, `QM`, `MD`, `Multiwfn` subdirectories

3. **External Tools**
   - [ ] ORCA installed and `OHMind_ORCA` correctly set
   - [ ] Multiwfn installed and `MULTIWFN_PATH` set
   - [ ] GROMACS available on PATH

4. **Backend + UI**
   - [ ] `./start_apps.sh` runs without errors
   - [ ] Backend reachable on `http://localhost:BACKEND_PORT`
   - [ ] UI reachable on `http://localhost:8000`

5. **MCP Servers**
   - [ ] Configured in Chainlit MCP panel (if using UI‑side MCP)
   - [ ] Manual debug commands (Section 6.2) work as expected

If all boxes are checked, you should be able to run the HEM multi‑agent workflow, perform QM/MD/Multiwfn analyses, and have all results consistently stored under `OHMind_workspace`.

---

## 10. Practical MCP & Agent Usage Examples

This section provides concrete, end‑to‑end examples for using OHMind’s MCP tools and agents in common workflows.

### 10.1 HEMDesign Optimization via UI (HEM Multi‑Agent)

This is the most user‑friendly way to run PSO‑based HEM optimization.

1. **Start backend + UI**
   - From the project root:
     ```bash
     cd OHMind
     ./start_apps.sh
     ```
   - Wait until both backend and UI are running.

2. **Open the UI**
   - Visit: `http://localhost:8000`
   - Log in with `admin` / `admin` (or your configured credentials).

3. **Select the HEM Multi‑Agent profile**
   - Click on the chat profile selector.
   - Choose **HEM Multi‑Agent**.
   - In chat settings, ensure **HEM backend URL** is correct, e.g. `http://localhost:8005`.

4. **Ask a concrete design question**
   Examples:
   - “Optimize piperidinium cations for backbone `PBF_BB_1` with multi‑objective HEM performance.”
   - “Design new imidazolium cations with high alkaline stability and conductivity.”

5. **What happens under the hood**
   - The supervisor agent interprets your request.
   - It calls into the **HEMDesign MCP server** (tool `optimize_hem_design`).
   - PSO optimization runs in the background; logs and CSVs are written to:
     ```text
     OHMind_workspace/HEM
       ├── best_solutions_<BACKBONE>_<CATION>.csv
       ├── best_fitness_history_<BACKBONE>_<CATION>.csv
       └── optimization_<BACKBONE>_<CATION>.log
     ```
   - The UI streams progress and final results back to you.

6. **Inspect results on disk**
   - After the run, inspect results e.g.:
     ```bash
     cd "$OHMind_workspace"/HEM
     ls
     # View the best solutions
     column -s, -t < best_solutions_PBF_BB_1_piperidinium.csv | less
     ```

This workflow is ideal when you want to drive optimization interactively and let the agents orchestrate tools.

### 10.2 HEMDesign Optimization via Backend API (No UI)

You can call the LangGraph backend directly (useful for scripting or integration with other systems).

1. **Ensure backend is running**
   - Either via `./start_apps.sh` or manually:
     ```bash
     cd OHMind
     uvicorn app:app --host 0.0.0.0 --port 8005
     ```

2. **Create a thread**
   ```bash
   THREAD_ID=$(curl -s -X POST \
     http://localhost:8005/threads \
     -H "Content-Type: application/json" \
     -d '{"metadata": {"purpose": "hem_optimization"}}' | jq -r '.thread_id')
   echo $THREAD_ID
   ```

3. **Run a HEM design request on that thread**
   - Example body (simple `input` form):
     ```bash
     curl -s -X POST \
       http://localhost:8005/threads/$THREAD_ID/runs \
       -H "Content-Type: application/json" \
       -d '{
         "input": {
           "content": "Optimize piperidinium cations for PBF_BB_1 backbone with multi-objective HEM performance."
         }
       }' | jq
     ```

4. **Interpret the response**
   - The returned JSON contains the final LangGraph state for that thread, including agent messages.
   - While the optimization runs asynchronously, files and logs appear in `OHMind_workspace/HEM` as described in Section 7.3.

This pattern can be adapted for programmatic batch runs by looping over backbones and cation types.

### 10.3 Using Chem + QM Agents for Property Queries (UI)

You can use the **Simple Chat** or **HEM Multi‑Agent** profile to answer chemistry questions that require QM or descriptor calculations.

1. **Select a profile**
   - Simple Chat: for general chemistry + tools.
   - HEM Multi‑Agent: for HEM‑focused workflows.

2. **Ask a question that requires QM**
   Examples:
   - “For the cation `C[N+]1(C)CCCCC1`, estimate the LUMO energy and comment on its alkaline stability.”
   - “Compare the predicted alkaline stability of these two cations: [SMILES1] vs [SMILES2].”

3. **What happens in the background**
   - The **Chemistry** / **QM** agents decide whether to call the ORCA MCP server through tools that:
     - Generate ORCA inputs
     - Run calculations in `QM_WORK_DIR` (`OHMind_workspace/QM`)
     - Extract descriptors (e.g., HOMO/LUMO) and feed them back into reasoning.

4. **Inspect QM outputs**
   - Look in:
     ```text
     OHMind_workspace/QM
       ├── temp_*          # Per‑job temporary directories
       └── results/        # Preserved results (depending on config)
     ```
   - Use ORCA / cclib tools or custom scripts to further analyze `.out` files.

### 10.4 MD (GROMACS) Workflow via Agents

The **MD agent** and GROMACS MCP server are used when you ask for polymer‑level properties under specific conditions.

Example conversation (Simple Chat or HEM Multi‑Agent):

> “Build a simple AEM polymer system with 10 chains, degree of polymerization 25, and simulate at 400 K. Estimate water uptake and ionic conductivity.”

Behind the scenes:

- The MD agent uses GROMACS MCP tools to:
  - Prepare a polymer + water system
  - Assign force fields and charges
  - Run MD using GROMACS in `MD_WORK_DIR` (`OHMind_workspace/MD`)
  - Post‑process trajectories for water uptake, swelling, and conductivity

You can inspect the MD workspace:

```bash
cd "$OHMind_workspace"/MD
ls
```

Typical contents include topology files, trajectories (`.xtc`, `.trr`), and log files, depending on the tool configuration.

### 10.5 Multiwfn Analysis Workflow

When you need detailed wavefunction analysis (electron density, population analysis, etc.), the **Multiwfn MCP server** is used.

Typical usage pattern:

1. Ask a question in the UI that requires detailed electronic analysis:
   - “For the optimized geometry of this cation, analyze charge distribution and highlight likely degradation sites.”
2. The agents:
   - Generate wavefunction files (from ORCA or other QM outputs) in `QM_WORK_DIR`.
   - Call Multiwfn MCP tools that run Multiwfn in `MULTIWFN_WORK_DIR` (`OHMind_workspace/Multiwfn`).
3. Outputs:
   - Stored under subdirectories like:
     ```text
     OHMind_workspace/Multiwfn/<job-name>/
       ├── input.*
       ├── analysis.log
       └── *.dat / *.cube  # analysis data and grids
     ```

You can visualize `.cube` data in external tools (e.g. VMD) or parse `.dat` files with Python for custom plots.

### 10.6 Using MCP Tools Directly from an MCP‑Compatible Client

If you use an MCP‑compatible environment (e.g., an IDE or LLM client that supports MCP), you can connect directly to the OHMind servers.

1. **Add the server** (example: HEMDesign)
   - Name: `OHMind-HEMDesign`
   - Type: `stdio`
   - Command: `/home/you/anaconda3/envs/OHMind/bin/python`
   - Args: `-m OHMind_agent.MCP.HEMDesign.server --transport stdio`
   - Env: often empty if you are launching from the OHMind project root with `.env` loaded; otherwise set the same variables as in Section 6.2.

2. **List available tools**
   - Your MCP client will show the tools provided by `OHMind-HEMDesign` (e.g., optimization, list backbones, show logs, kill job).

3. **Call a tool with structured input**
   - For optimization, you’ll provide arguments like:
     - `backbone`: e.g. `"PBF_BB_1"`
     - `cation_name`: e.g. `"piperidinium"`
     - `property`: `"multi"` / `"ec"` / `"ewu"` / `"esr"`
     - `num_part`, `steps`: PSO settings
     - `save_path` (optional): falls back to `HEM_SAVE_PATH`
   - The tool response will include where results are saved and how to monitor progress.

This pattern is similar for other MCP servers (`OHMind-Chem`, `OHMind-ORCA`, `OHMind-Multiwfn`, `OHMind-GROMACS`):

- Add server with `command`, `args`, and matching `env`.
- Use your MCP client’s UI to inspect available tools.
- Provide JSON‑like inputs as prompted by the tool schema.
- Inspect results in the corresponding workspace subdirectory.

### 10.7 Quick Recipes: Ready‑To‑Use Prompts

This subsection gives you copy‑paste prompts for common tasks. Use them in the Chainlit UI (Simple Chat or HEM Multi‑Agent profile).

#### 10.7.1 HEM Optimization

- **Multi‑objective piperidinium design**
  > Design new piperidinium-based cations for backbone PBF_BB_1 optimizing multi-objective HEM performance (conductivity, ESR, and water uptake). Please run PSO using your default settings and summarize the top 10 candidates.

- **Backbone/cation sweep**
  > For backbones PBF_BB_1 and PP_BB_1, design the best tetraalkylammonium cations using your HEM optimization tools. Compare the top candidates for each backbone in terms of alkaline stability, ESR, and conductivity.

#### 10.7.2 ORCA / QM Analysis

- **LUMO and alkaline stability**
  > For the cation SMILES "C[N+]1(C)CCCCC1", run a QM calculation using ORCA to estimate its LUMO energy and any other relevant stability descriptors. Then explain qualitatively what they imply for alkaline stability.

- **Comparative QM analysis**
  > Compare the predicted alkaline stability of these two cations based on QM descriptors: [SMILES1] vs [SMILES2]. Please compute or approximate LUMO energies and any other important descriptors, and provide a short conclusion.

#### 10.7.3 MD (GROMACS) Simulations

- **Small AEM system at 400 K**
  > Build a simple AEM polymer system with 10 polymer chains and degree of polymerization 25, equilibrated with water at 400 K. Run a reasonably short GROMACS MD simulation and estimate water uptake, swelling ratio, and ionic conductivity. Summarize key simulation parameters and results.

- **Parameter sweep (temperature)**
  > Using your MD tools, design a small AEM system and run short test simulations at 300 K, 350 K, and 400 K. Compare how water uptake and ionic conductivity change with temperature, and provide a brief discussion.

#### 10.7.4 Multiwfn Electronic Analysis

- **Charge distribution and hot spots**
  > For the optimized geometry of this cation [SMILES], run a Multiwfn analysis to examine charge distribution and identify likely degradation hot spots under alkaline conditions. Summarize which atoms or fragments are most vulnerable.

- **Orbital visualization request**
  > Based on the QM results for this cation [SMILES], use Multiwfn to analyze and visualize the LUMO orbital. Describe where the LUMO is localized and what that implies for degradation pathways.

#### 10.7.5 General Chem / RAG Queries

- **Literature-driven design**
  > Retrieve recent literature on cation designs for hydroxide exchange membranes with high alkaline stability. Summarize typical structural motifs and then propose 5 new candidate cations that follow those design principles.

 - **Mechanism + design loop**
  > Explain the main degradation mechanisms for quaternary ammonium cations in AEMs under alkaline conditions. Then propose new cation designs that mitigate these mechanisms, and evaluate them using your available tools.
 
 These examples should give you a solid foundation to use OHMind both interactively (via the UI) and programmatically (via the backend API or MCP‑compatible clients).

## 11. MCP Tool Reference & Prompt Recipes

| Domain | MCP server name | Summary |
| ------ | ---------------- | ------- |
| Chemistry & RAG | `OHMind-Chem` | Cheminformatics, SMILES/name conversions, functional groups, and chemistry-aware web search. |
| HEM optimization | `OHMind-HEMDesign` | PSO-based cation design, configuration validation, and optimization job/status/log management. |
| Quantum chemistry | `OHMind-ORCA` | ORCA-powered QM calculations: single-point energies, optimizations, frequencies, proton affinity, binding, and reactivity descriptors. |
| Wavefunction analysis | `OHMind-Multiwfn` | Multiwfn-based wavefunction, orbital, electron-density, aromaticity, and spectrum analysis. |
| MD simulations | `OHMind-GROMACS` | GROMACS workflows for IEM MD: building, parameterization, system setup, simulation, and trajectory/energy analysis. |

 This section summarizes the MCP servers and tools provided by OHMind and gives prompt patterns for using them from MCP-aware assistants (e.g. IDE plugins, Claude Desktop, or the OHMind UI itself).

 Unless otherwise noted, the server names match those in `.chainlit/mcp.json` and typical IDE configurations:

- **Chem server**: `OHMind-Chem`
- **HEM optimization server**: `OHMind-HEMDesign`
- **Quantum chemistry / ORCA server**: `OHMind-ORCA`
- **Wavefunction analysis / Multiwfn server**: `OHMind-Multiwfn`
- **MD simulation / GROMACS server**: `OHMind-GROMACS`

When connected through an MCP client you usually *don’t* call tools by name yourself; instead you:

- **Describe the task in natural language** and mention the relevant server ("using your OHMind-Chem tools...").
- Optionally ask the assistant to **list available tools** first, then choose the appropriate one.

The subsections below give a compact tool reference and ready-to-use prompt recipes for each server.

### 11.1 OHMind-Chem – Molecular Informatics & Web RAG

**Server name**: `OHMind-Chem`  
**Entry point**: `python -m OHMind_agent.MCP.Chem.server --transport stdio`

**Tools (Chem)**

- `MoleculeWeight` – Compute exact molecular weight from a SMILES string.
- `MoleculeAtomCount` – Count atoms of each element in a molecule.
- `MoleculeSimilarity` – Tanimoto similarity and qualitative similarity description between two SMILES.
- `FunctionalGroups` – Detect common functional groups (e.g. alcohol, amide, sulfonate) from SMILES.
- `SmilesCanonicalization` – Canonicalize a SMILES string (with options for isomeric info and atom maps).
- `MoleculeSmilesCheck` – Validate a molecular SMILES string and explain syntax issues.
- `ReactionSmilesCheck` – Validate reaction SMILES (`reactants>reagents>products`).
- `Iupac2Smiles` – Convert IUPAC name → SMILES (via PubChem, with robust error handling).
- `Smiles2Iupac` – Convert SMILES → IUPAC name.
- `Smiles2Formula` – Molecular formula from SMILES.
- `Name2Smiles` – Common/brand/chemical name → SMILES.
- `Selfies2Smiles` – SELFIES → SMILES.
- `Smiles2Selfies` – SMILES → SELFIES.
- `Smiles2Cas` – Look up approximate CAS number from SMILES (via PubChem metadata).
- `Smiles2Image` – Render a 2D structure image from SMILES with configurable width/height.
- `WebSearch` – Chemistry-aware web/RAG search (Tavily-backed) for literature, properties, etc.
- `MoleculeCaptioner` – Natural-language caption / description of a molecule from SMILES (MolT5 model).

**Prompt recipes (Chem)**

- **Property and functional group analysis**  
  > Using your OHMind-Chem MCP tools, analyze this molecule with SMILES `CC(=O)OC1=CC=CC=C1C(=O)O`.  
  > 1) Check that the SMILES is valid.  
  > 2) Report its molecular weight and formula.  
  > 3) List the functional groups and briefly explain what each group typically does chemically.

- **Name ↔ SMILES ↔ image workflow**  
  > With your OHMind-Chem tools, convert the IUPAC name "2-propanol" to SMILES, verify the SMILES is valid, and then generate a small 300×300 structure image.  
  > Return the SMILES, a short caption describing the molecule, and a link or reference to the generated image file.

- **Similarity and RAG-assisted design**  
  > Use your Chem MCP tools to compare lidocaine and procaine by SMILES.  
  > 1) Compute their structural similarity.  
  > 2) Use your web-search tool to summarize key differences in their pharmacological profiles.  
  > 3) Propose a new candidate local anesthetic scaffold and justify it.

### 11.2 OHMind-HEMDesign – HEM Optimization & Job Management

**Server name**: `OHMind-HEMDesign`  
**Entry point**: `python -m OHMind_agent.MCP.HEMDesign.server --transport stdio`

**Tools (HEMDesign)**

- `ListBackbones` – List available polymer backbones for HEM design with SMILES and identifiers.
- `ListCations` – List available cation families and initial SMILES templates.
- `ValidateConfig` – Validate a prospective optimization configuration (backbone, cation family, property mode).
- `HEMOptimizer` – Launch PSO-based optimization to design new cation structures for a given backbone/cation/property objective.
- `CheckStatus` – Inspect saved optimization results and return top solutions from CSV logs.
- `ShowLogs` – Stream recent optimization log lines (for monitoring long runs).
- `KillJob` – List running optimization jobs or terminate one by backbone/cation/job ID.

**Prompt recipes (HEMDesign)**

- **Discover design space**  
  > Using your OHMind-HEMDesign tools, list all available backbones and cation types, then recommend 2–3 promising backbone–cation combinations for alkaline-stable AEMs.  
  > Summarize why these combinations are interesting.

- **Validate and start an optimization**  
  > First validate a multi-objective optimization for backbone `PBF_BB_1` with `piperidinium` cations and property mode `multi`.  
  > If the configuration is valid, start a PSO optimization with moderate settings (e.g. ~250 particles, ~5–10 steps), saving results to a fresh directory.  
  > Explain what metrics you are optimizing and how you will interpret the final Pareto front.

- **Monitor / manage a running job**  
  > Using your HEMDesign job-management tools, find any currently running optimizations.  
  > Show me a short snippet of the latest log lines for each job, and if any look clearly stalled or failing, ask me whether to kill them and, if I agree, terminate them safely before summarizing completed jobs.

### 11.3 OHMind-ORCA – Quantum Chemistry

**Server name**: `OHMind-ORCA`  
**Entry point**: `python -m OHMind_agent.MCP.ORCA.server --transport stdio`

**Core tools (ORCA)**

- `SinglePointEnergy` – Single-point energy of a structure (XYZ) with configurable method/basis/dispersion.
- `GeometryOptimization` – Optimize geometry from XYZ; returns optimized coordinates, final energy, and result directory.
- `FrequencyCalculation` – Vibrational frequencies, IR spectrum, thermochemistry, and Gibbs free energy.
- `SmilesToXYZ` – SMILES → 3D XYZ coordinates using RDKit.

**IEM-focused tools (ORCA)**

- `ProtonAffinityCalculation` – Proton affinity and approximate pKa for acidic groups (gas and solution phase).
- `BindingEnergyCalculation` – Ion–functional group binding energies with BSSE correction and optional solvation.
- `IonicSolvationEnergy` – Solvation/hydration energies and free energies for ions or ion–water clusters.
- `ChargeAnalysis` – Mulliken, Löwdin, Hirshfeld charges; dipole/quadrupole moments.
- `TransitionStateSearch` – Transition-state search with optional frequency verification and activation energy.
- `NMRChemicalShift` – NMR shielding and chemical shifts for selected nuclei (¹H, ¹³C, ¹⁹F, ³¹P, etc.).
- `PolymerReactivity` – HOMO/LUMO energies, gaps, and conceptual DFT descriptors for monomer reactivity.

**Prompt recipes (ORCA)**

- **End‑to‑end QM descriptor pipeline**  
  > Using your OHMind-ORCA QM tools, start from the SMILES `C[N+]1(C)CCCCC1` and:  
  > 1) Convert to a reasonable 3D geometry.  
  > 2) Optimize the structure at B3LYP/def2-SVP with D3BJ.  
  > 3) Compute frequencies to confirm there are no imaginary modes.  
  > 4) Report LUMO energy and any descriptors relevant to alkaline stability, and interpret them qualitatively.

- **Proton affinity and pKa estimation**  
  > For a sulfonic-acid-containing fragment (you can build or assume a reasonable model), use your proton affinity tool to estimate gas-phase and solution-phase proton affinity and the corresponding pKa.  
  > Explain what these values imply for acid strength and membrane behavior.

- **Binding & solvation comparison**  
  > Compare the binding energy and hydration energy of OH⁻ vs Cl⁻ to a model quaternary ammonium site using your ORCA binding and solvation tools.  
  > Summarize which ion binds more strongly and how solvation competes with binding.

### 11.4 OHMind-Multiwfn – Wavefunction & Orbital Analysis

**Server name**: `OHMind-Multiwfn`  
**Entry point**: `python -m OHMind_agent.MCP.Multiwfn.server --transport stdio`

**Tools (Multiwfn)**

- `AnalyzeWavefunction` – General wavefunction diagnostics for a given input file (e.g. fchk/wfn).
- `WeakInteractionAnalysis` – RDG/NCI/IGMH/IRI analyses of noncovalent interactions.
- `AromaticityAnalysis` – Aromaticity indices including NICS and related measures.
- `ElectronDensityAnalysis` – AIM, ELF, LOL, Laplacian and related electron-density analyses.
- `OrbitalAnalysis` – Orbital compositions, energies, and populations.
- `PopulationAnalysis` – Mulliken, Hirshfeld, ADCH, RESP, CM5, MBIS and other charge schemes.
- `BondAnalysis` – Bond orders and bond strength descriptors (e.g. Mayer/Wiberg).
- `EnergyDecomposition` – LMO-EDA, SAPT and related energy-decomposition analyses.
- `SimulateSpectrum` – Simulated spectra (UV–Vis, IR, Raman, NMR, ECD, VCD).
- `MDAnalysis` – Post-processing of MD trajectories (RDFs, coordination numbers, H-bonds, etc.).
- `GenerateCubeFiles` – Generate cube files for densities, orbitals, and related scalar fields.
- `AdNDPAnalysis` – Adaptive Natural Density Partitioning analysis.
- `VisualizeOrbitals` – High-level orbital visualization and rendering orchestration.
- `QuickVisualizeHOMOLUMO` – Convenience tool to quickly visualize only HOMO/LUMO.
- `RenderOrbitals2D` – 2D slice plotting of orbitals/densities (matplotlib).
- `RenderOrbitals3D` – 3D orbital rendering with VMD/Tachyon style output.

**Prompt recipes (Multiwfn)**

- **Charge & reactive hot-spot analysis**  
  > For the optimized cation geometry from my QM calculation (assume I have already generated a suitable wavefunction file), use your Multiwfn tools to analyze charge distribution and identify likely degradation hot spots under alkaline conditions.  
  > Report which atoms or fragments are most positively charged or otherwise reactive.

- **Orbital visualization**  
  > Starting from the wavefunction of a candidate cation, generate HOMO and LUMO visualizations (both 2D slices and 3D renders).  
  > Describe where the LUMO is localized and what that suggests about degradation pathways.

- **Spectrum simulation from MD snapshot**  
  > Take a representative structure from an MD snapshot of my membrane system and use Multiwfn to simulate an approximate UV–Vis or IR spectrum, highlighting features that correlate with specific structural motifs.

### 11.5 OHMind-GROMACS – MD Workflows for IEMs

**Server name**: `OHMind-GROMACS`  
**Entry point**: `python -m OHMind_agent.MCP.GROMACS.server --transport stdio`

**High-level workflow tools (GROMACS)**

- `run_complete_iem_workflow_tool` – From monomer SMILES to a full IEM MD workflow (build polymer, parameterize, prepare system, run MD, analyze key outputs).
- `run_complete_md_simulation_tool` – Given structure/topology and basic settings, run a full EM → NVT → NPT → MD pipeline.

**Building & parameterization tools**

- `calculate_ions_per_monomer_tool` – Estimate ionizable sites per monomer from SMILES.
- `analyze_ion_exchange_groups_tool` – Advanced analysis of ion-exchange groups in monomers.
- `create_polymer_from_smiles_tool` – Build oligomer/polymer PDBs from monomer SMILES (RDKit-based).
- `create_itp_file_tool` – End-to-end workflow from polymer PDB to a true GROMACS `.itp` file (Antechamber + tleap + conversion + extraction).
- `parameterize_molecule_antechamber_tool` – Run Antechamber on a molecule to get charges/atom types.
- `prepare_mainchain_files_tool` – Produce HEAD/CHAIN/TAIL mainchain definitions from Antechamber output.
- `run_prepgen_tool` – Generate PREPI residue files from mainchain definitions.
- `build_polymer_with_tleap_tool` – Build polymer chains with tleap for topology generation.
- `convert_amber_to_gromacs_tool` – Convert AMBER topologies to GROMACS formats.
- `extract_ff_and_itp_tool` – Extract `forcefield.itp` and monomer `.itp` from a `.top` file.

**System preparation & simulation tools**

- `calculate_single_ion_system_tool` – Compute system composition and charge balance for a single-ion system.
- `create_system_topology_tool` – Build system `.top` with specified polymers, ions, water content, and water model.
- `create_packmol_input_tool` – Run PACKMOL-based initial packing of polymers and ions.
- `prepare_simulation_box_tool` – Use `gmx editconf` to define simulation box.
- `create_mdp_file_tool` – Generate MDP files (EM, NVT, NPT, MD) with chosen T, P, and timestep.
- `run_grompp_tool` – Prepare `tpr` files via `gmx grompp`.
- `run_mdrun_tool` – Execute MD runs with `gmx mdrun` and basic progress reporting.

**Analysis & configuration tools**

- `calculate_msd_tool` – Compute MSD and diffusion-related metrics from trajectories.
- `analyze_energy_tool` – Analyze energies and thermodynamic observables from `.edr` files.
- `get_water_model_info_tool` – Detailed info for a given water model (e.g. SPC/E, TIP3P) and usage notes.
- `list_available_water_models_tool` – Enumerate all configured water models, highlighting recommended ones.
- `get_current_config_tool` – Report current configuration, work directory, and default settings for the GROMACS server.
- `update_work_directory_tool` – Change the default work directory for the current MCP session.

**Prompt recipes (GROMACS)**

- **Small AEM system from SMILES**  
  > Using your OHMind-GROMACS tools, start from this monomer SMILES: `[SMILES]`.  
  > 1) Estimate ions per monomer and suggest an appropriate ion type and water model.  
  > 2) Build an oligomer, parameterize it, generate a real `.itp` file, and create a small system (e.g. 10 chains, DP 25, reasonable water uptake).  
  > 3) Run a short MD simulation at 400 K and summarize key properties such as density and qualitatively estimated conductivity.

- **Focused MD pipeline control**  
  > I already have `system_initial.pdb` and `system.top`.  
  > Use your GROMACS MCP tools to: (a) build a simulation box, (b) generate NVT and NPT MDP files with 400 K and 1 bar, (c) run grompp and mdrun for a short production run, and (d) analyze MSD and key energy terms.  
  > Return a human-readable summary of the MD setup and results.

- **Water model and work-directory management**  
  > With your configuration tools, list available water models and recommend one for hydroxide-conducting AEMs.  
  > Then update the MD work directory to a new folder under my project (e.g. `./simulations/aem_test`) and confirm the change.

### 11.6 Putting MCP Servers Together

The real power of OHMind comes from **composing multiple MCP servers**:

- **Chem → ORCA → Multiwfn** for structure generation, QM calculations, and detailed electronic analysis.
- **Chem → HEMDesign** for structure-space exploration guided by cheminformatics and literature search.
- **Chem/ORCA → GROMACS → Multiwfn** for MD-informed QM analysis (e.g. taking representative MD snapshots into QM/Multiwfn).

When prompting an MCP-aware assistant, it is usually enough to:

- Clearly state the *physical/chemical question* you want answered.
- Indicate which parts should use **HEM optimization**, **QM**, **MD**, or **wavefunction analysis**.
- Ask the assistant to **explain which tools it used** (server + tool names) so that you can reproduce or further automate the workflow later.
