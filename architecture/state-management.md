---
permalink: /architecture/state-management/
layout: default
title: "State Management"
parent: "Architecture"
nav_order: 3
last_updated: "2026-09-23"
---

# State Management

`OHMind_agent/graph/state.py` defines `AgentState`. LangGraph's `add_messages` reducer accumulates messages; agents return updates to shared routing, tool, plan, and recovery fields.

## State fields

| Group | Fields |
|---|---|
| Conversation and routing | `messages`, `next`, `rag_context` |
| Tool execution | `mcp_results`, `tool_executions`, `artifacts` |
| Operations and errors | `current_operation`, `operation_metadata`, `error`, `retry_count` |
| Human validation | `validation_required`, `validation_approved`, `validation_message` |
| Planning | `task_plan`, `task_plan_path`, `current_step`, `completed_steps`, `task_plan_needs_approval`, `task_plan_approved` |
| Run identity | `run_id`, `project_id`, `active_policy_version` |
| Recovery memory | `memory_snapshot_id`, `failure_event`, `memory_query`, `retrieved_memory_refs`, `recovery_action`, `validator_report`, `episode_candidate_id` |

`create_initial_state(user_message)` provides defaults for standalone integrations. The backend sends the new message and run metadata with a stable `configurable.thread_id`; the shared checkpointer loads previous graph state.

## Checkpoint lifecycle

The backend initializes persistence once and reuses a compiled workflow and its checkpointer across requests. With `DURABLE_STATE_ENABLED=false`, `MemorySaver` is process-local: state is lost on backend restart. With the feature enabled and a valid PostgreSQL DSN, `AsyncPostgresSaver` stores checkpoints across restarts.

A direct `create_workflow()` call without a supplied checkpointer still falls back to `MemorySaver`. Environment flags alone do not initialize persistence for custom callers; use `initialize_persistence()` as shown in [Workflow API]({% link api/workflow-api.md %}).

## Inspecting state

For a known thread ID, `GET /threads/{thread_id}/state` returns the real latest snapshot. `GET` or `POST /threads/{thread_id}/history` returns real stored snapshots. Snapshot fields include `values`, `next`, `config`, `metadata`, `created_at`, `parent_config`, and `tasks`.

Keep the thread ID outside the process. The separate `GET /threads` registry and `GET /threads/{thread_id}` metadata are in memory and can be empty/404 after restart even when checkpoint state exists. State/history lookup uses the saved ID to read the checkpointer.

## What a checkpoint does not restore

- An MCP socket or a running external process.
- A terminated Python optimization worker.
- A UI database record unless the UI storage layer saved it.
- Scientific models, output files, or optimizer state that were never saved.

HEM jobs use `job_state.json` and optimizer JSON checkpoints separately. On service restart, previously active persisted jobs are marked failed because their worker no longer exists. Resume explicitly from a verified checkpoint when available.

See [Persistence tutorial]({% link tutorials/memory-and-recovery.md %}) and [PSO resume]({% link tutorials/pso-resume.md %}).
