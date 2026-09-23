---
permalink: /getting-started/installation/
layout: default
title: "Installation Guide"
parent: "Getting Started"
nav_order: 2
last_updated: "2026-09-23"
---

# Installation Guide

These instructions target the source revision described in [Documentation status]({% link release-notes.md %}). Use Linux, Conda, Python 3.10 or 3.11, and Docker Compose. Scientific workloads determine CPU, memory, GPU, and disk requirements. A fresh installation of the combined scientific and UI dependencies still needs end-to-end validation.

## Install from source

```bash
git clone https://github.com/lunyang/OHMind.git
cd OHMind
conda env create -f environment.yml
conda activate OHMind
python -m pip install poetry
cd OHMind_ui
poetry install --no-root
cd ..
```

The repository root has no editable-install metadata. Run from the source checkout. `environment.yml` and `OHMind_ui/pyproject.toml` cover different dependency groups; creating the Conda environment alone does not complete the agent/UI setup. Confirm Poetry uses the environment you intend to run.

```bash
python -c "import OHMind; print(OHMind.__version__)"
```

This checks the base package import only, not model availability or scientific correctness.

## Configure private settings

For a new checkout, copy templates without overwriting existing configuration:

```bash
cp -n .env.example .env
cp -n OHMind_ui/.env.example OHMind_ui/.env
```

Set your LLM provider credentials, model, and endpoint in the root `.env`. Configure embeddings for literature retrieval. Set an absolute `OHMind_workspace` and external-tool paths for the workflows you use.

Set independent `CHAINLIT_AUTH_SECRET`, `DEFAULT_ADMIN_PASSWORD`, `POSTGRES_PASSWORD`, and `MINIO_ROOT_PASSWORD` values in `OHMind_ui/.env`. Both files must be valid bash assignments because the combined launcher sources them, root first and UI second. Avoid empty UI variables overwriting a provider key from the root file. Real `.env` files and `users.json` stay local.

Additional accounts can be created with `python OHMind_ui/manage_users.py add --username NAME`. The current account store uses plaintext passwords; keep it private. Sign in using the configured credentials.

## Prepare PostgreSQL and MinIO

For the web UI and the current migration chain:

```bash
docker compose -f OHMind_ui/docker-compose.yml up -d postgres minio
docker compose -f OHMind_ui/docker-compose.yml ps
```

Wait for PostgreSQL to become healthy, then apply migrations:

```bash
cd OHMind_ui
python -m alembic upgrade head
cd ..
```

Use `docker-compose.yml`, whose PostgreSQL image includes **pgvector**. The older `docker-compose-db-only.yml` uses plain PostgreSQL and does not provide the extension required by the memory migration. Existing installations need a compatible database and an appropriate migration plan; changing the image does not migrate existing data.

Alembic reads `POSTGRES_*` settings from the environment/UI `.env`, not `MEMORY_DATABASE_URL`. If memory uses a separate database, explicitly target that database when applying its migrations. See [Memory and persistence configuration]({% link configuration/memory-persistence.md %}).

## Model and scoring resources

HEM optimization needs the following authorized resources in `OHMind/OHPSO/data/`:

| Files | Purpose |
|---|---|
| `chembl_fps.npy` | Substructure scoring, loaded at module import |
| `cation_latent_alkaline.npy`, `PairAlkaline.pt` | Alkaline stability |
| `scalerEC.pkl`, `EffectConduc.pt` | Conductivity |
| `scalerEWU.pkl`, `EffectWU.pt` | Water uptake |
| `scalerESR.pkl`, `EffectSR.pt` | Swelling ratio |

These files are not distributed in the inspected Git tree. Verified public download locations and checksums have not yet been provided. A new clone is therefore not a self-contained scientific installation. The tracked JT-VAE checkpoint and vocabularies do not replace these scoring resources. Consult the code repository's `docs/local-setup.md` for the resource inventory.

## External software setup

| Component | Used for | Configuration |
|---|---|---|
| ORCA and matching MPI | Quantum chemistry | `OHMind_ORCA`, `OHMind_MPI` |
| GROMACS | Molecular dynamics | Make `gmx` available on `PATH` |
| Multiwfn | Wavefunction analysis | `MULTIWFN_PATH` |
| Qdrant and embeddings | Literature retrieval | `QDRANT_URL` or `QDRANT_PATH`, embedding provider settings |

Obtain scientific executables from their maintainers and follow their installation and licensing instructions. Set absolute paths. Configure only workflows you intend to run; a working chat session does not verify these tools.

## Start and verify

```bash
PYTHON="$(command -v python)" CHAINLIT="$(command -v chainlit)" bash start_OHMind.sh
```

The launcher starts the backend, five MCP services, and Chainlit. Open `http://localhost:8000`. The backend normally uses `8005`; MCP services use `8101–8105`. Review `OHMind_logs/` for service-specific failures.

```bash
curl --fail http://localhost:8005/health
```

A healthy backend response is a liveness check. Test the intended tools separately with a small workload before a long optimization or simulation.

For terminal usage, `PYTHON="$(command -v python)" bash start_OHMind_full.sh` starts MCP services and the CLI. Use `start_OHMind_cli.sh` when MCP services are already running. Explicit interpreter overrides avoid developer-machine defaults in the launchers.
