---
title: "Workspace Setup"
description: "Guide to setting up the OHMind workspace directory structure, Qdrant vector database, permissions, and storage requirements"
category: "configuration"
tags: ["workspace", "directory", "qdrant", "storage", "setup"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# Workspace Setup

> Complete guide to setting up the OHMind unified workspace, including directory structure, Qdrant vector database, permissions, and storage requirements.

## Table of Contents

- [Overview](#overview)
- [Workspace Root Configuration](#workspace-root-configuration)
- [Directory Structure](#directory-structure)
- [Creating the Workspace](#creating-the-workspace)
- [Qdrant Vector Database](#qdrant-vector-database)
- [Permissions](#permissions)
- [Storage Requirements](#storage-requirements)
- [Automatic Setup](#automatic-setup)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

OHMind uses a unified workspace directory to organize all computational outputs. This centralized approach ensures:

- **Consistent organization**: All results in predictable locations
- **Easy backup**: Single directory to backup
- **Cross-agent access**: All agents can find and use results
- **Clean separation**: Project code separate from generated data

## Workspace Root Configuration

### Environment Variable

Set the workspace root using the `OHMind_workspace` environment variable:

```bash
# In .env
OHMind_workspace=/data/ohmind_workspace
```

### Derived Paths

Subdirectory paths are derived from the workspace root:

```bash
# These are set automatically if not explicitly defined
HEM_SAVE_PATH=${OHMind_workspace}/HEM
QM_WORK_DIR=${OHMind_workspace}/ORCA
MD_WORK_DIR=${OHMind_workspace}/GROMACS
MULTIWFN_WORK_DIR=${OHMind_workspace}/Multiwfn
WORKSPACE_ROOT=${OHMind_workspace}
```

### Custom Subdirectory Paths

Override individual paths if needed:

```bash
# Custom paths (optional)
HEM_SAVE_PATH=/fast-ssd/hem_results
QM_WORK_DIR=/scratch/orca_calculations
MD_WORK_DIR=/large-storage/md_simulations
```

## Directory Structure

### Standard Layout

```
$OHMind_workspace/
├── HEM/                        # HEM optimization results
│   ├── best_solutions_*.csv    # Top candidate molecules
│   ├── best_fitness_history_*.csv  # Optimization progress
│   └── optimization_*.log      # Detailed logs
│
├── ORCA/                       # Quantum chemistry calculations
│   ├── temp_<job-id>/          # Per-job working directories
│   │   ├── input.inp           # ORCA input file
│   │   ├── input.out           # ORCA output
│   │   └── input.gbw           # Wavefunction file
│   └── results/                # Preserved final results
│
├── GROMACS/                    # Molecular dynamics simulations
│   ├── <system-name>/          # Per-system directories
│   │   ├── *.pdb               # Structure files
│   │   ├── *.top               # Topology files
│   │   ├── *.mdp               # Parameter files
│   │   ├── *.tpr               # Run input files
│   │   ├── *.xtc, *.trr        # Trajectory files
│   │   └── *.edr               # Energy files
│   └── analysis/               # Post-processing results
│
├── Multiwfn/                   # Wavefunction analysis
│   └── <job-name>/             # Per-analysis directories
│       ├── input.*             # Input files
│       ├── analysis.log        # Analysis log
│       ├── *.dat               # Data files
│       └── *.cube              # Cube files for visualization
│
└── qdrant_db/                  # Vector database (if local mode)
    ├── collection/             # Document collections
    └── snapshots/              # Database snapshots
```

### HEM Directory Details

```
HEM/
├── best_solutions_PBF_BB_1_piperidinium.csv
├── best_solutions_PP_BB_1_imidazolium.csv
├── best_fitness_history_PBF_BB_1_piperidinium.csv
├── optimization_PBF_BB_1_piperidinium.log
└── ...
```

**File naming convention:** `<type>_<backbone>_<cation>.<ext>`

### ORCA Directory Details

```
ORCA/
├── temp_abc123/                # Active calculation
│   ├── input.inp               # ORCA input
│   ├── input.out               # Output (during/after run)
│   ├── input.gbw               # Wavefunction
│   ├── input.xyz               # Optimized geometry
│   └── input_property.txt      # Extracted properties
├── temp_def456/                # Another calculation
└── results/                    # Archived results
    └── cation_opt_20241223/    # Named result set
```

### GROMACS Directory Details

```
GROMACS/
├── aem_system_001/
│   ├── polymer.pdb             # Initial structure
│   ├── system.top              # System topology
│   ├── em.mdp                  # Energy minimization params
│   ├── nvt.mdp                 # NVT equilibration params
│   ├── npt.mdp                 # NPT equilibration params
│   ├── md.mdp                  # Production MD params
│   ├── em.tpr                  # EM run input
│   ├── md.xtc                  # Production trajectory
│   └── md.edr                  # Energy data
└── analysis/
    ├── msd_analysis.xvg        # Mean square displacement
    └── rdf_analysis.xvg        # Radial distribution function
```

### Multiwfn Directory Details

```
Multiwfn/
├── cation_charge_analysis/
│   ├── input.fchk              # Input wavefunction
│   ├── charges.txt             # Computed charges
│   └── analysis.log            # Multiwfn output
├── orbital_visualization/
│   ├── homo.cube               # HOMO orbital cube
│   ├── lumo.cube               # LUMO orbital cube
│   └── orbital_energies.dat    # Orbital energy data
└── nci_analysis/
    ├── nci.cube                # NCI surface
    └── rdg.dat                 # Reduced density gradient
```

## Creating the Workspace

### Manual Creation

```bash
# Create workspace root
mkdir -p /data/ohmind_workspace

# Create subdirectories
mkdir -p /data/ohmind_workspace/{HEM,ORCA,GROMACS,Multiwfn,qdrant_db}

# Set permissions
chmod -R u+rwx /data/ohmind_workspace
```

### Using Environment Variables

```bash
# Set workspace root
export OHMind_workspace=/data/ohmind_workspace

# Create all directories
mkdir -p "$OHMind_workspace"/{HEM,ORCA,GROMACS,Multiwfn,qdrant_db}
```

### Verification

```bash
# Check structure
tree -L 2 $OHMind_workspace

# Expected output:
# /data/ohmind_workspace
# ├── GROMACS
# ├── HEM
# ├── Multiwfn
# ├── ORCA
# └── qdrant_db
```

## Qdrant Vector Database

### Local Mode (Recommended for Single-User)

Store the vector database in the workspace:

```bash
# In .env
QDRANT_PATH=${OHMind_workspace}/qdrant_db
# Leave QDRANT_URL unset
```

**Advantages:**
- No separate server required
- Simple backup (just copy the directory)
- Works offline

**Directory structure:**

```
qdrant_db/
├── collections/
│   └── ohmind_papers/          # Document collection
│       ├── segments/           # Vector segments
│       └── wal/                # Write-ahead log
├── aliases/
└── raft_state.json
```

### Server Mode (Multi-User or Production)

Connect to a Qdrant server:

```bash
# In .env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-api-key  # If authentication enabled
# Leave QDRANT_PATH unset
```

**Starting Qdrant Server:**

```bash
# Using Docker
docker run -p 6333:6333 -p 6334:6334 \
  -v /data/qdrant_storage:/qdrant/storage \
  qdrant/qdrant

# Or using the binary
./qdrant --storage-path /data/qdrant_storage
```

### Initializing the Vector Store

The RAG system automatically creates collections when first used:

```python
from OHMind_agent.rag.vectorstore import get_vectorstore

# This creates the collection if it doesn't exist
vectorstore = get_vectorstore()
```

### Ingesting Documents

```bash
# Ingest scientific papers
python OHMind_agent/scripts/ingest_papers.py \
  --input-dir /path/to/papers \
  --collection ohmind_papers
```

## Permissions

### Required Permissions

| Directory | Permission | Reason |
|-----------|------------|--------|
| `$OHMind_workspace` | `rwx` | Create subdirectories |
| `HEM/` | `rwx` | Write optimization results |
| `ORCA/` | `rwx` | Write calculation files |
| `GROMACS/` | `rwx` | Write simulation files |
| `Multiwfn/` | `rwx` | Write analysis files |
| `qdrant_db/` | `rwx` | Database operations |

### Setting Permissions

```bash
# Set ownership (if needed)
sudo chown -R $USER:$USER $OHMind_workspace

# Set permissions
chmod -R u+rwx $OHMind_workspace

# Verify
ls -la $OHMind_workspace
```

### Multi-User Setup

For shared workspaces:

```bash
# Create group
sudo groupadd ohmind_users

# Add users to group
sudo usermod -aG ohmind_users user1
sudo usermod -aG ohmind_users user2

# Set group ownership
sudo chown -R :ohmind_users $OHMind_workspace

# Set group permissions
chmod -R g+rwx $OHMind_workspace

# Set sticky bit to preserve group ownership
chmod g+s $OHMind_workspace
```

## Storage Requirements

### Minimum Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| HEM results | 100 MB | 1 GB |
| ORCA calculations | 1 GB | 10 GB |
| GROMACS simulations | 10 GB | 100 GB |
| Multiwfn analysis | 500 MB | 5 GB |
| Qdrant database | 500 MB | 5 GB |
| **Total** | **~12 GB** | **~120 GB** |

### Storage by Task Type

| Task | Typical Size | Notes |
|------|--------------|-------|
| Single HEM optimization | 1-10 MB | CSV + logs |
| Single QM calculation | 10-100 MB | Depends on basis set |
| Short MD simulation | 100 MB - 1 GB | Depends on trajectory saving |
| Long MD simulation | 1-10 GB | Full trajectory |
| Multiwfn analysis | 10-100 MB | Cube files can be large |

### Cleanup Strategies

#### Automatic Cleanup

Some MCP servers support automatic cleanup of temporary files:

```python
# ORCA server cleans temp directories after successful completion
# Configure retention in server settings
```

#### Manual Cleanup

```bash
# Remove old ORCA temp directories (older than 7 days)
find $QM_WORK_DIR/temp_* -type d -mtime +7 -exec rm -rf {} \;

# Remove old GROMACS trajectories (keep only last 5)
cd $MD_WORK_DIR
ls -t *.xtc | tail -n +6 | xargs rm -f

# Compress old results
find $OHMind_workspace -name "*.log" -mtime +30 -exec gzip {} \;
```

#### Archiving

```bash
# Archive completed projects
tar -czvf project_archive_$(date +%Y%m%d).tar.gz \
  $OHMind_workspace/HEM/completed_* \
  $OHMind_workspace/ORCA/results/*

# Move to cold storage
mv project_archive_*.tar.gz /archive/ohmind/
```

## Automatic Setup

### Using start_apps.sh

The startup script automatically sets up workspace paths:

```bash
./start_apps.sh
```

**What it does:**

```bash
# Sets default workspace if not defined
export OHMind_workspace="${OHMind_workspace:-${ROOT_DIR}_workspace}"

# Sets subdirectory paths
export HEM_SAVE_PATH="${HEM_SAVE_PATH:-${OHMind_workspace}/HEM}"
export QM_WORK_DIR="${QM_WORK_DIR:-${OHMind_workspace}/ORCA}"
export MD_WORK_DIR="${MD_WORK_DIR:-${OHMind_workspace}/GROMACS}"
export MULTIWFN_WORK_DIR="${MULTIWFN_WORK_DIR:-${OHMind_workspace}/Multiwfn}"
```

### Setup Script

Create a setup script for new installations:

```bash
#!/bin/bash
# setup_workspace.sh

# Configuration
WORKSPACE_ROOT="${1:-/data/ohmind_workspace}"

echo "Setting up OHMind workspace at: $WORKSPACE_ROOT"

# Create directories
mkdir -p "$WORKSPACE_ROOT"/{HEM,ORCA,GROMACS,Multiwfn,qdrant_db}

# Set permissions
chmod -R u+rwx "$WORKSPACE_ROOT"

# Create .env template
cat > "$WORKSPACE_ROOT/.env.template" << EOF
OHMind_workspace=$WORKSPACE_ROOT
HEM_SAVE_PATH=$WORKSPACE_ROOT/HEM
QM_WORK_DIR=$WORKSPACE_ROOT/ORCA
MD_WORK_DIR=$WORKSPACE_ROOT/GROMACS
MULTIWFN_WORK_DIR=$WORKSPACE_ROOT/Multiwfn
QDRANT_PATH=$WORKSPACE_ROOT/qdrant_db
EOF

echo "Workspace created successfully!"
echo "Add these to your .env file:"
cat "$WORKSPACE_ROOT/.env.template"
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Permission denied" | Insufficient permissions | `chmod -R u+rwx $OHMind_workspace` |
| "No space left on device" | Disk full | Clean up old files or expand storage |
| "Directory not found" | Workspace not created | Run setup script or create manually |
| "Cannot write to workspace" | Read-only filesystem | Check mount options |

### Diagnostic Commands

```bash
# Check workspace exists and is writable
test -w "$OHMind_workspace" && echo "Writable" || echo "Not writable"

# Check disk space
df -h "$OHMind_workspace"

# Check permissions
ls -la "$OHMind_workspace"

# Check environment variables
env | grep -E "^(OHMind|HEM|QM|MD|MULTIWFN|WORKSPACE)"
```

### Recovery

If workspace becomes corrupted:

```bash
# Backup existing data
cp -r $OHMind_workspace ${OHMind_workspace}.backup

# Recreate structure
rm -rf $OHMind_workspace
mkdir -p $OHMind_workspace/{HEM,ORCA,GROMACS,Multiwfn,qdrant_db}

# Restore data selectively
cp -r ${OHMind_workspace}.backup/HEM/* $OHMind_workspace/HEM/
# ... repeat for other directories
```

## See Also

- [Configuration Overview](./index.md) - Configuration system overview
- [Environment Variables](./environment-variables.md) - All environment variables
- [Installation Issues](../troubleshooting/installation-issues.md) - Setup problems
- [RAG Agent](../agents/rag-agent.md) - Vector database usage

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
