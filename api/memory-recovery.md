---
permalink: /api/memory-recovery/
layout: default
title: "Memory and Recovery APIs"
parent: "API Reference"
nav_order: 4
last_updated: "2026-09-23"
---

# Memory and Recovery APIs

These are Python integration interfaces, not HTTP endpoints or chat commands. Run integrations in the OHMind environment from the source checkout.

## MemoryGateway

`OHMind_agent.memory.backend.MemoryGateway(backend, read_mode=..., write_mode=...)` wraps a memory backend:

| Method | Behavior |
|---|---|
| `await stage(episode)` | Stage a `RecoveryEpisode` when writes are enabled |
| `await validate_and_commit(episode)` | Apply admission checks, then persist/index when writes are enabled |
| `await recall_verified(query)` | Return verified hits only in active read mode |
| `await audit_recall(query)` | Evaluate verified recall in shadow or active mode |
| `await revoke(episode_id, reason)` | Revoke via backend when writes are enabled |

Use `MemoryQuery` and `MemoryScope` from `OHMind_agent.memory.models`; keep scope values consistent with the producer. `initialize_persistence(settings, stack)` returns the configured gateway in `resources.memory`. See [Workflow API]({% link api/workflow-api.md %}) for resource lifetime handling.

## Recovery selection and PSO execution

`choose_recovery(failure, memory_hits=(), policy_registry=None, allow_diagnosis=True)` returns a `RecoveryDecision` containing an optional action, decision source, diagnostic count, episode reference, and reason. It selects an allowlisted action; it does not perform an optimizer run.

`run_pso_step_with_recovery(optimizer, checkpoint_path=..., checkpoint_metadata=..., inference_model=..., scoring_functions=..., max_recovery_attempts=1, event_sink=None, decision_provider=None)` executes one step and validates supported timeout recovery. The callable decision provider receives a `FailureEvent`. `HEMOptimizationCore.run_optimization()` exposes `recovery_decision_provider` for explicit integrations. These advanced parameters are not public MCP tool arguments.

`PersistentRecoveryRuntime` exposes synchronous `choose`, `commit`, `revoke`, and `promote` around PostgreSQL memory and a file policy registry. Its implementation uses `asyncio.run()`; do not call those synchronous wrappers inside an already running event loop. Use the async gateway/ledger interfaces there.

## Policy registries

`RecoveryPolicyRegistry(directory)` provides `active_version`, `resolve(signature)`, `promote(episodes, min_support=2)`, and `rollback(target_version)`. Files are stored in the supplied directory. Use validated supporting episodes; rollback does not revoke memory episodes.

`PostgresRecoveryPolicyRegistry(pool, policy_id="hem_pso_recovery")` provides async `check_schema()`, `initialize()`, `active_snapshot()`, `promote(...)`, `rollback(target_version, reason=...)`, and `audit()`. See `OHMind_agent/recovery/postgres_policy.py` for promotion arguments and ledger-authority checks. Its snapshot supplies synchronous `resolve()` for the controller. Standard application setup does not automatically attach this registry.

Source contracts and integration boundaries are documented in [Recovery Memory]({% link architecture/memory.md %}) and [Recovery and Policies]({% link architecture/recovery.md %}).
