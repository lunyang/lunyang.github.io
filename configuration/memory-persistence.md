---
permalink: /configuration/memory-persistence/
layout: default
title: "Memory and Persistence"
parent: "Configuration Overview"
nav_order: 5
last_updated: "2026-09-23"
---

# Memory and Persistence

The settings below are defined in `OHMind_agent/config.py`. Literature retrieval, graph checkpoints, and recovery memory are separate systems; enabling one does not enable the others.

## Settings and defaults

| Variable | Default | Meaning |
|---|---|---|
| `DURABLE_STATE_ENABLED` | `false` | Use PostgreSQL for LangGraph checkpoints |
| `STATE_DATABASE_URL` | unset | Checkpoint DSN; falls back to the resolved memory DSN |
| `MEMORY_ENABLED` | `false` | Enable the selected memory backend |
| `MEMORY_BACKEND` | `noop` | `noop` or `langmem` |
| `MEMORY_DATABASE_URL` | unset | Episode ledger and LangGraph Store DSN; falls back to `POSTGRES_*` when `POSTGRES_HOST` is set |
| `MEMORY_WRITE_MODE` | `off` | `off`, `shadow`, or `active` |
| `MEMORY_READ_MODE` | `off` | `off`, `shadow`, or `active` |
| `MEMORY_TOP_K` | `5` | Retrieval limit, 1–50 |
| `MEMORY_MIN_TRUST` | `0.8` | Confidence threshold, 0–1 |
| `MEMORY_SCHEMA_VERSION` | `1.0` | Memory namespace/schema version |
| `ACTIVE_POLICY_VERSION` | `v0` | Initial run metadata; does not itself promote a policy |
| `RECOVERY_POLICY_DIRECTORY` | `RESULTS_ROOT/OHMind_recovery_policies` | Filesystem policy registry location resolved by `get_memory_config()` |
| `RESULTS_ROOT` | repository-parent `Results/` | Scientific results root |
| `CASE_STUDY_ROOT` | `RESULTS_ROOT/OHMind_case_studies` | Case-study output root |

## Configure a first deployment

After [database preparation]({% link getting-started/installation.md %}#prepare-postgresql-and-minio), add to your private root `.env`:

```dotenv
DURABLE_STATE_ENABLED=true
MEMORY_ENABLED=true
MEMORY_BACKEND=langmem
MEMORY_WRITE_MODE=shadow
MEMORY_READ_MODE=shadow
MEMORY_TOP_K=5
MEMORY_MIN_TRUST=0.8
```

Set `STATE_DATABASE_URL` and `MEMORY_DATABASE_URL` privately, or let the combined launcher export the UI `POSTGRES_*` settings. DSNs use the form `postgresql://USER:PASSWORD@HOST:PORT/DATABASE`; encode reserved characters in credentials. Setting a DSN alone does not enable its feature.

## Database migrations

From `OHMind_ui/`, run `python -m alembic upgrade head`. The migration chain includes the trusted-memory ledger (`f41a9d2c7b10`) and policy governance (`a82c9e41d5f7`). It requires pgvector. Alembic uses `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`; it does not select its target from `MEMORY_DATABASE_URL`.

For separate UI and memory databases, set those `POSTGRES_*` variables explicitly in the migration process for each intended database. Keep credentials in the local environment. At application startup, LangGraph initializes its checkpoint/Store tables; OHMind checks that its episode ledger migration has been applied. Missing DSNs or required schemas cause initialization errors rather than successful durable operation.

## Read and write modes

| Mode | Read behavior | Write behavior |
|---|---|---|
| `off` | Recall and audit recall return no hits | No stage, commit, or revoke writes |
| `shadow` | `audit_recall()` can evaluate matches; `recall_verified()` returns no decision inputs | Candidate staging and verified commits are enabled |
| `active` | Verified recall may guide recovery selection | Candidate staging and verified commits are enabled |

Read and write modes are independent. Shadow writes are real writes, not a dry run. Shadow reads require an explicit audit call; the standard graph does not automatically log a separate shadow evaluation. Admission validation still runs on `validate_and_commit()` even when writes are off.

`MEMORY_ENABLED=false` or a `noop` backend provides no persistent recovery memory. Start with shadow modes and inspect real evidence before active reads. The standard HEM tool does not automatically wire a memory decision provider or commit recovery episodes merely because these settings are enabled.

## Persistence boundaries

Database checkpoints preserve graph state, not external worker processes. MCP connections are recreated on restart. The backend's thread registry remains process-local; retain the thread ID for `/state` and `/history` queries. See [State management]({% link architecture/state-management.md %}) and [Recovery architecture]({% link architecture/recovery.md %}).
