---
permalink: /tutorials/memory-and-recovery/
layout: default
title: "Verify Persistence and Memory"
parent: "Tutorials"
nav_order: 6
last_updated: "2026-09-23"
---

# Verify Persistence and Memory

Complete [storage setup]({% link getting-started/installation.md %}#prepare-postgresql-and-minio) and [memory configuration]({% link configuration/memory-persistence.md %}). Begin with shadow read/write modes. Run these checks on a development deployment where restarting the backend is acceptable.

## Verify graph persistence

Create a thread and keep the returned ID:

```bash
curl --fail -X POST http://localhost:8005/threads \
  -H 'Content-Type: application/json' -d '{"metadata":{"purpose":"persistence-check"}}'
```

Set the ID in your shell and submit a small request:

```bash
THREAD_ID=replace-with-returned-thread-id
curl --fail -X POST "http://localhost:8005/threads/$THREAD_ID/runs" \
  -H 'Content-Type: application/json' \
  -d '{"input":{"content":"Remember the label persistence-check for this conversation."}}'
curl --fail "http://localhost:8005/threads/$THREAD_ID/state"
curl --fail "http://localhost:8005/threads/$THREAD_ID/history"
```

The run uses your configured model and may incur its normal API cost. Save the responses. Restart the backend through your normal launcher/service procedure, then repeat the state/history requests with the **same ID**. With durable checkpoints and the same database, previous messages should remain available. Without durable state, they are lost. The thread list may be empty after restart because its registry is process-local.

## Understand the shadow check

Enabling shadow mode does not generate episodes from ordinary chat. A tool-specific integration must supply a verified `RecoveryEpisode` through `MemoryGateway.stage()` and `validate_and_commit()`. Use real validator results and evidence; do not fabricate successful records to populate the store.

Developers can evaluate retrieval using `await memory.audit_recall(query)`. In shadow mode, `await memory.recall_verified(query)` returns an empty list, so these matches do not enter recovery decisions. Scope, failure signature, schema version, confidence, and ledger hashes determine eligibility. See [developer API]({% link api/memory-recovery.md %}).

## Inspect a failure

When a general workflow error reaches recovery nodes, inspect `failure_event`, `recovery_action`, `operation_metadata.recovery_decision`, and `validator_report` in `/state`. The current general dispatch guard reports unexecuted tool-specific recovery as unvalidated and escalates it. This is expected, not proof that memory storage failed.

For execution-level checkpoint recovery, follow [Resume PSO]({% link tutorials/pso-resume.md %}). Validate its trace and outputs separately from graph persistence.

## Move to active reads

After reviewing validated episodes and retrieval scope, set `MEMORY_READ_MODE=active` and restart the application. Verified recall can then guide wired recovery consumers. This change does not add missing tool-specific dispatch, episode recording, or policy-promotion hooks.
