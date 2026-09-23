---
permalink: /architecture/recovery/
layout: default
title: "Recovery and Policies"
parent: "Architecture"
nav_order: 6
last_updated: "2026-09-23"
---

# Recovery and Policies

## General workflow failures

The graph routes eligible agent errors through:

```text
failure_classifier → memory_recall → recovery_controller
  → outcome_validator → recovery_escalation → END
```

The controller prefers verified memory, then a promoted policy, then a fresh diagnostic mapping. It escalates when no allowed action is available. The current general workflow validator deliberately returns `passed=false`: selecting an action is not proof that a tool-specific repair ran. The failure, proposed action, and validation report remain in checkpoint state for inspection.

## Allowed actions

| Action | Purpose | Execution boundary |
|---|---|---|
| `REINDEX_JTVAE_BATCH` | Rebuild compact node indexing for a JT-VAE batch | Explicit batch-level dispatcher/validator integration; not arbitrary source editing |
| `RESUME_PSO_CHECKPOINT` | Resume an optimizer from its saved state | Tool-specific PSO controller loads and validates the checkpoint |

## PSO timeout recovery

`run_pso_step_with_recovery()` handles `FunctionTimedOut`, with one retry per step by default. It reloads the checkpoint at the failed step's starting iteration. Recovery passes only after exactly one iteration of progress and successful checkpoint hash/schema reload, within the retry budget. Other errors or exhausted budgets propagate as failures.

The HEM tool calls this path through `HEMOptimizationCore`. Its normal invocation does not pass `recovery_decision_provider`; it uses fresh diagnosis. A custom integration can supply a trusted-memory/policy selector and record a validated episode afterward. See [PSO resume tutorial]({% link tutorials/pso-resume.md %}).

## Policy governance

Two implementations exist, with different integration points:

| Registry | Storage | Current use |
|---|---|---|
| `RecoveryPolicyRegistry` | `active_policy.json`, immutable files in `versions/`, `policy_history.jsonl` | Standard graph via the resolved policy directory; `PersistentRecoveryRuntime` |
| `PostgresRecoveryPolicyRegistry` | Database versions, active pointer, evidence and audit records | Explicit developer integration; not automatically selected by `MEMORY_BACKEND=langmem` |

The file registry's promotion requires matching verified-success episodes with passing validators, an allowed action, and at least two distinct supporting episodes from independent runs by default. Supporting actions for the signature must agree. Promotion records source episode IDs/hashes. Rollback activates a previous snapshot, including the empty `v0` state, and appends history.

The PostgreSQL registry additionally checks ledger authority and uses transactional policy operations; its rollback requires a reason. Do not assume a file-policy rollback changes a PostgreSQL registry or vice versa. Restart/recreate file-registry consumers after an external policy change so they reload the selected state.

There is no public policy-management HTTP endpoint or built-in CLI slash command in the inspected backend. Policy changes use the [Python interfaces]({% link api/memory-recovery.md %}).

Source: `OHMind_agent/recovery/` and `OHMind_agent/graph/workflow.py`.
