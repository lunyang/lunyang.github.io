---
permalink: /release-notes/
layout: default
title: Documentation Status
nav_order: 12
last_updated: "2026-09-23"
---

# Documentation Status

## Source baseline

This update was prepared on 2026-09-23 against local OHMind source HEAD `9d40a2647f2ce864d6c3e60a1e6053f3cb265237`, including the memory/recovery implementation introduced in `f642897a720aa6278d5c0170cefcfaac87bfa71b`. Installation instructions also use the local configuration-template and setup-document changes awaiting publication. These identifiers record the inspected source; they are not a claim that this revision is available from the public default branch.

The separately prepared clean source tree has HEAD `c14f8f8915eac6441aff25e829d3890d36f17315`, with the feature under rewritten commit `ab8c932edef4e6cdf4334b0dfe5ffb9f6b49025c`. Its README predates the current local README. Reconcile the release tree before presenting these instructions as a published software release. No new software version number is assigned by this documentation update.

## Updated capabilities

- Optional PostgreSQL LangGraph checkpoints and real state/history API responses.
- A trusted recovery-episode ledger, scoped recall, hash checks, revocation, and index outbox replay.
- Separate read/write modes, including shadow evaluation.
- Allowlisted failure-recovery selection and explicit escalation where execution evidence is absent.
- Bounded PSO timeout recovery, hash-checked optimizer checkpoints, explicit resume, and durable job records.
- File and PostgreSQL policy registries with promotion, version history, and rollback through developer interfaces.

## Current limits

General workflow recovery does not automatically execute every proposed action or admit new episodes. The standard HEM tool uses checkpoint recovery; memory-driven decisions and episode recording require explicit runtime integration. The standard backend uses a file policy registry, not the PostgreSQL policy registry automatically.

The thread metadata/list registry remains process-local. Durable graph state can be queried after restart using a retained thread ID. Persisted optimization records do not keep worker processes alive.

Scientific scoring resources listed in [Installation]({% link getting-started/installation.md %}#model-and-scoring-resources) are not distributed in the inspected Git tree, and public download/checksum instructions are not yet available. A clean end-to-end application installation remains to be verified. The inspected code repository has no root LICENSE file; distribution terms need to be settled before declaring a licensed release.

## Documentation verification scope

New operational instructions and changed interfaces were checked against source. Existing scientific chapters retain their own examples; this update does not constitute rerunning every simulation, external-tool workflow, or model benchmark. Maintainer build and publication instructions are in the documentation repository README.
