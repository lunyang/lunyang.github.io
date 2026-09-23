---
permalink: /architecture/memory/
layout: default
title: "Recovery Memory"
parent: "Architecture"
nav_order: 5
last_updated: "2026-09-23"
---

# Recovery Memory

OHMind keeps three different stores:

| Store | Content | Implementation |
|---|---|---|
| Literature retrieval | Scientific documents and embeddings | Qdrant |
| Workflow checkpoints | Messages, routing, tool results, and recovery state | LangGraph MemorySaver or PostgreSQL saver |
| Recovery experience | Failure signatures, actions, provenance, evidence, and validation | PostgreSQL episode ledger and LangGraph Store through `LangMemBackend` |

## Episode lifecycle

A `RecoveryEpisode` records scope, a `FailureEvent`, a `RecoveryAction`, provenance, evidence references, trust metadata, and a `ValidatorReport`. Statuses are `candidate`, `verified_success`, `verified_failure`, `rejected`, and `revoked`.

The `MemoryGateway` stages candidates and validates admission before updating the verified index. Admission requires a verified outcome and trust state, a passing deterministic validator report, hash-linked evidence references, supporting evidence IDs, and verifier identity/time. These checks validate the supplied record; domain-specific validators must establish the actual scientific or execution outcome. A plausible assistant explanation is not sufficient evidence.

The PostgreSQL ledger is authoritative. The Store holds indexed records. Ledger writes enqueue outbox operations so interrupted index updates can be replayed at startup. Revocation is recorded in the ledger and removed from the index; retrieval also consults the ledger to reject stale revoked entries and content-hash mismatches.

## Retrieval scope

`MemoryScope` includes `tenant_id`, `project_id`, `agent`, and `task_family`; the namespace also includes the schema version. Retrieval filters verified trust state, optional failure signature, and minimum confidence, then checks the authoritative episode. The Store can fall back to exact-signature filtering without an embedding index; the default initialization does not configure semantic embeddings for recovery memory.

The standard backend currently supplies `tenant_id=local` and `project_id=ohmind`. Scope fields are retrieval boundaries, not a complete multi-tenant authorization system. Integrations need consistent scope values when writing and reading episodes.

## Integration status

The graph can recall verified memory and select an allowlisted recovery action. It does not automatically turn arbitrary conversations or successful tool calls into recovery episodes. The HEM optimization path supports checkpoint retries; memory-driven PSO selection and verified episode recording require explicit runtime integration.

See [Recovery and policies]({% link architecture/recovery.md %}), [configuration]({% link configuration/memory-persistence.md %}), and [developer APIs]({% link api/memory-recovery.md %}).

Source: `OHMind_agent/memory/{models,backend,trust_gate,langmem_adapter,postgres_ledger,lifecycle}.py`.
