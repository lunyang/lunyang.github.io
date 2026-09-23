---
permalink: /troubleshooting/memory-recovery/
layout: default
title: "Memory and Recovery Issues"
parent: "Troubleshooting"
nav_order: 5
last_updated: "2026-09-23"
---

# Memory and Recovery Issues

| Symptom | Check and resolution |
|---|---|
| Startup requests `STATE_DATABASE_URL` | Enable durable state only with a resolved checkpoint DSN; root/UI environment loading must match your launch path |
| Startup requests `MEMORY_DATABASE_URL` | Set a DSN or export `POSTGRES_*`, including `POSTGRES_HOST`, for the `langmem` backend |
| Missing ledger/schema tables | Apply Alembic migrations to the database actually selected for memory; Alembic uses `POSTGRES_*` |
| `vector` extension is unavailable | Use a PostgreSQL installation with pgvector; the older database-only Compose image does not include it |
| Backend restart loses conversation | Check `DURABLE_STATE_ENABLED`, the resolved database, and reuse of the exact thread ID |
| `/threads` is empty but old state exists | The thread registry is process-local; query `/threads/{id}/state` or `/history` with the saved ID |
| No memories after normal conversations | Automatic episode extraction/commit is not wired for arbitrary chat; verified tool-specific integration is required |
| No hits in shadow mode | Decision recall returns no hits by design; evaluate with `audit_recall()` |
| No hits in active mode | Check enabled backend, scope/schema/signature, trust threshold, ledger revocation, and content hashes |
| A selected recovery is escalated | General workflow selection does not execute a tool-specific repair; inspect the validator report |
| A job is failed after MCP restart | Durable records cannot restore the worker process; inspect its failure and resume from an intact optimizer checkpoint |
| Resume rejects configuration | Match saved backbone, cation, property, particle count, seed, and scoring weights; use a target step count at least as high as the saved iteration |
| Resume rejects checkpoint integrity | Use an intact checkpoint and matching resources; do not remove hash checks |
| Policy changes have no effect | Confirm which registry is wired; recreate/restart consumers of file policies after changes |

A backend `/health` response only establishes liveness. Inspect service logs, graph snapshots, `job_state.json`, optimizer checkpoints, and `recovery_trace.jsonl` as appropriate. Keep credentials out of shared logs and reports.

See [configuration]({% link configuration/memory-persistence.md %}), [state management]({% link architecture/state-management.md %}), and [recovery architecture]({% link architecture/recovery.md %}).
