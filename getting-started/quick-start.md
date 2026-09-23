---
permalink: /getting-started/quick-start/
layout: default
title: "Quick Start Guide"
parent: "Getting Started"
nav_order: 1
last_updated: "2026-09-23"
---

# Quick Start Guide

Follow [Installation]({% link getting-started/installation.md %}) first: create the Conda environment, install the UI/agent dependencies, configure both `.env` files, prepare storage, and obtain scientific resources for the tools you intend to use. Setup time depends on dependencies and model availability.

## Start the web interface

From the OHMind source root, with its environment activated:

```bash
PYTHON="$(command -v python)" CHAINLIT="$(command -v chainlit)" bash start_OHMind.sh
```

Open `http://localhost:8000` and sign in with your configured administrator credentials. Check backend liveness with `curl --fail http://localhost:8005/health`.

## Start the terminal interface

```bash
PYTHON="$(command -v python)" bash start_OHMind_full.sh
```

This starts the MCP services and CLI. If services are already running, use `PYTHON="$(command -v python)" bash start_OHMind_cli.sh` instead.

## Try a small request

Ask: “Calculate the molecular weight of aspirin from SMILES `CC(=O)OC1=CC=CC=C1C(=O)O`.” Inspect the actual tool result and any reported errors.

Once HEM model resources are available, ask for a supported backbone and cation type, then start a small optimization with five particles and three steps. Record the returned job ID and output directory; starting an asynchronous job is not confirmation that it finished.

## Enable persistence separately

The default configuration disables durable state and recovery memory. For conversations that must survive backend restarts, follow [Memory and persistence]({% link configuration/memory-persistence.md %}). Use [the persistence tutorial]({% link tutorials/memory-and-recovery.md %}) to verify behavior before relying on it.

For interrupted HEM optimization, see [Resume PSO]({% link tutorials/pso-resume.md %}). Database conversation checkpoints and optimizer checkpoints serve different purposes.
