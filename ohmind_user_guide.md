---
layout: default
title: OHMind User Guide
permalink: /ohmind-user-guide/
nav_order: 2
has_children: false
---

# OHMind User Guide
{: .no_toc }

A practical tutorial for installing, configuring, and using the OHMind platform for AI‑driven cation design and HEM (Hydroxide Exchange Membrane) workflows.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. Overview

**OHMind** is an AI‑driven toolkit for cation design and HEM research. It includes:

- **Core library**: `OHMind/` (VAE, PSO, QM, MD, reaction models, etc.)
- **Multi‑agent backend**: `OHMind_agent/` (FastAPI + LangGraph multi‑agent system)
- **Web UI**: `OHMind_ui/` (Chainlit + LangGraph frontend)
- **MCP servers**: Chemistry, ORCA, Multiwfn, GROMACS, HEMDesign

This guide walks you through:

1. Installation and environment setup
2. Workspace layout and unified result storage
3. Configuring environment variables and MCP servers
4. Starting the backend and UI
5. Running typical workflows (especially HEM multi‑agent)
6. Debugging MCP servers and troubleshooting

---

## 2. Installation & Environment

### 2.1 Prerequisites

- Linux (tested on Ubuntu‑like systems)
- Conda (Anaconda or Miniconda)
- GPU with CUDA (recommended)
- Optional but recommended external tools:
  - [ORCA](https://orcaforum.kofo.mpg.de/app.php/portal) – quantum chemistry
  - [Multiwfn](http://sobereva.com/multiwfn/) – wavefunction analysis
  - GROMACS – molecular dynamics
  - Qdrant – vector database
  - PostgreSQL + MinIO – used by the Chainlit UI

### 2.2 Create the Conda Environment

From the project root:

```bash
cd /media/polyai/8T/MyResearch/CationDesign/OHMind

# Create the OHMind environment (uses environment.yml)
conda env create -f environment.yml

# Activate it
conda activate OHMind
```

> The `environment.yml` file pins most Python dependencies (PyTorch, DGL, RDKit, FastAPI, Chainlit, etc.).

### 2.3 External Software Paths

You will need to know where the following are installed on your system:

- `OHMind_ORCA` – full path to the ORCA binary
- `OHMind_MPI` – directory containing MPI binaries (e.g. `mpirun`)
- `MULTIWFN_PATH` – full path to the Multiwfn executable
- GROMACS – available on your `$PATH` (e.g. after `source gmxtools.sh`)

These are configured via environment variables (see **Section 4**).

---

## 3. Unified Workspace Layout

All heavy computation (QM, MD, PSO/HEM, Multiwfn) is organized under a **single workspace root**.

### 3.1 Workspace Root

The unified root is controlled by the environment variable:

- `OHMind_workspace`

In this project it is typically set to:

```bash
OHMind_workspace=/media/polyai/8T/MyResearch/CationDesign/OHMind_workspace
```

This is defined in:

- Root `.env`
- `OHMind_agent/.env`
- `start_apps.sh` (fallback default `${ROOT_DIR}_workspace`)

### 3.2 Subdirectory Layout

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
- `QM_WORK_DIR   = ${OHMind_workspace}/QM`
- `MD_WORK_DIR   = ${OHMind_workspace}/MD`
- `MULTIWFN_WORK_DIR = ${OHMind_workspace}/Multiwfn`
- `WORKSPACE_ROOT = ${OHMind_workspace}` (generic root for backend code)

These are exported by:

- `.env` and `OHMind_agent/.env`
- `start_apps.sh`, which sets sensible defaults if variables are not pre‑set.

### 3.3 How `start_apps.sh` Sets Workspace Paths

From the project root:

```bash
./start_apps.sh
```

Internally, the script does (simplified):

```bash
export OHMind_workspace="${OHMind_workspace:-${ROOT_DIR}_workspace}"
export HEM_SAVE_PATH="${HEM_SAVE_PATH:-${OHMind_workspace}/HEM}"
export QM_WORK_DIR="${QM_WORK_DIR:-${OHMind_workspace}/QM}"
export MD_WORK_DIR="${MD_WORK_DIR:-${OHMind_workspace}/MD}"
export MULTIWFN_WORK_DIR="${MULTIWFN_WORK_DIR:-${OHMind_workspace}/Multiwfn}"
```

So if you **do nothing**, it will create/use `${ROOT_DIR}_workspace` with the described subfolders. If you prefer a specific location, set `OHMind_workspace` before running the script.

---

## 4. Environment Variables & Configuration

### 4.1 Core `.env` (project root)

The root `.env` controls the multi‑agent FastAPI backend (`app.py`).
Key entries:

- LLM configuration (OpenAI‑compatible via `OPENAI_COMPATIBLE_*`)
- Qdrant URL: `QDRANT_URL`, `QDRANT_API_KEY`
- Web search: `TAVILY_API_KEY`
- MCP config: `MCP_CONFIG_PATH=/media/polyai/8T/MyResearch/CationDesign/OHMind/mcp.json`
- Workspace:
  - `OHMind_workspace=/media/polyai/8T/MyResearch/CationDesign/OHMind_workspace`
  - `HEM_SAVE_PATH=${OHMind_workspace}/HEM`
  - `WORKSPACE_ROOT=${OHMind_workspace}`

The backend reads these via `OHMind_agent.config.Settings`.

### 4.2 `OHMind_agent/.env`

This file is used when running the multi‑agent backend or MCP servers directly from `OHMind_agent`. It includes:

- `MCP_CONFIG_PATH` – usually the same root `mcp.json`
- `OHMind_workspace`, `HEM_SAVE_PATH`, `WORKSPACE_ROOT` – as above

### 4.3 UI `.env` (`OHMind_ui/.env`)

This configures the Chainlit + LangGraph UI:

- Logging level
- Auth (default admin user/password)
- Postgres connection
- MinIO settings
- LLM provider keys (OpenAI, Anthropic, etc.)

The UI obtains MCP server details from `OHMind_ui/.chainlit/mcp.json` (documentation only; Chainlit currently requires manual entry via the UI).

### 4.4 MCP Configuration Files

There are two important JSON files describing MCP servers:

1. **Backend MCP config**: `mcp.json` (in project root)
   - Used by the multi‑agent backend via `OHMind_agent.config.mcp_config_path`
   - Paths in `env` now use the unified workspace layout:
     - `QM_WORK_DIR = /media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/QM`
     - `MD_WORK_DIR = /media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/MD`
     - `MULTIWFN_WORK_DIR = /media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/Multiwfn`
     - `HEM_SAVE_PATH = /media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/HEM`

2. **UI MCP config**: `OHMind_ui/.chainlit/mcp.json`
   - Documents how to add MCP servers in Chainlit’s UI.
   - Exhibits the same workspace paths as `mcp.json`.

> The actual MCP processes are started by the backend (multi‑agent system) and by Chainlit (for UI‑side tools). Both now use the same workspace locations.

---

## 5. Starting the Backend & UI

### 5.1 Using `start_apps.sh` (recommended)

From the project root:

```bash
cd /media/polyai/8T/MyResearch/CationDesign/OHMind

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

### 5.2 Accessing the UI

After `start_apps.sh` is running, open:

```text
http://localhost:8000
```

Default login (from `OHMind_ui/.env`):

- User: `admin`
- Password: `admin`

Once logged in, you’ll see multiple workflows, including **HEM Multi‑Agent**.

---

## 6. MCP Servers Configuration (UI Side)

### 6.1 Adding MCP Servers in Chainlit

Chainlit (v2.9.0) does **not** automatically read `OHMind_ui/.chainlit/mcp.json`. Instead, that file documents the servers you should add via the UI.

1. Start backend + UI (see Section 5).
2. In the UI, open the **MCP** panel (left sidebar) and click **Add server**.
3. For each server (`OHMind-Chem`, `OHMind-HEMDesign`, `OHMind-ORCA`, `OHMind-Multiwfn`, `OHMind-GROMACS`):
   - **Name**: e.g. `OHMind-ORCA`
   - **Type**: `stdio`
   - **Command**: your Python binary, e.g. `/home/you/anaconda3/envs/OHMind/bin/python`
   - **Args**: e.g. `-m OHMind_agent.MCP.ORCA.server --transport stdio`

Most environment variables (including workspace paths) are already exported by `.env` + `start_apps.sh`, so in many cases you can leave the **Env** section empty.

### 6.2 Manual MCP Server Commands (Debugging)

You can run MCP servers manually to debug issues. Examples:

```bash
# Chem
PYTHONPATH=/media/polyai/8T/MyResearch/CationDesign/OHMind \
  TAVILY_API_KEY=tvly-dev-... \
  RDKIT_QUIET=1 \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.Chem.server --transport stdio

# ORCA
PYTHONPATH="/media/polyai/8T/MyResearch/CationDesign/OHMind" \
  OHMind_ORCA="/home/you/ORCA/orca" \
  OHMind_MPI="/usr/local/bin" \
  QM_WORK_DIR="/media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/QM" \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.ORCA.server

# HEMDesign
PYTHONPATH=/media/polyai/8T/MyResearch/CationDesign/OHMind \
  HEM_SAVE_PATH=/media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/HEM \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.HEMDesign.server --transport stdio

# Multiwfn
PYTHONPATH=/media/polyai/8T/MyResearch/CationDesign/OHMind \
  MULTIWFN_PATH=/home/you/Multiwfn/Multiwfn \
  MULTIWFN_WORK_DIR=/media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/Multiwfn \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.Multiwfn.server --transport stdio

# GROMACS
PYTHONPATH=/media/polyai/8T/MyResearch/CationDesign/OHMind \
  MD_WORK_DIR=/media/polyai/8T/MyResearch/CationDesign/OHMind_workspace/MD \
  /home/you/anaconda3/envs/OHMind/bin/python -m OHMind_agent.MCP.GROMACS.server --transport stdio
```

Adapt the paths (`OHMind_ORCA`, `MULTIWFN_PATH`, Conda path) to your system.

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
  mkdir -p /media/polyai/8T/MyResearch/CationDesign/OHMind_workspace
  chmod u+rwx /media/polyai/8T/MyResearch/CationDesign/OHMind_workspace
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
  cd /media/polyai/8T/MyResearch/CationDesign/OHMind
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
     cd /media/polyai/8T/MyResearch/CationDesign/OHMind
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
     cd /media/polyai/8T/MyResearch/CationDesign/OHMind
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

These examples should give you a solid foundation to use OHMind both interactively (via the UI) and programmatically (via the backend API or MCP‑compatible clients).
