---
permalink: /api/
title: API Reference
description: "Comprehensive API documentation for integrating with OHMind programmatically"
nav_order: 10
has_children: true
last_updated: "2026-09-23"
---

# API Reference

| Interface | Purpose |
|---|---|
| [Backend API]({% link api/backend-api.md %}) | Thread/run endpoints, server-sent events, actual state/history snapshots |
| [Workflow API]({% link api/workflow-api.md %}) | Compile and reuse the graph with correctly scoped persistence resources |
| [Session Manager]({% link api/session-manager.md %}) | MCP connections and tool distribution |
| [Memory and Recovery APIs]({% link api/memory-recovery.md %}) | Verified memory, recovery decisions, PSO runtime hooks, and policy registries |

The combined launcher uses `http://localhost:8005` for the backend and `http://localhost:8000` for the web UI. Run setup first, then use the request examples in the backend reference.

The backend has no built-in per-user authentication; the Chainlit UI has its own login. Configure deployment access appropriately. Use your configured UI credentials rather than a default password.

Run responses and checkpoint snapshots have endpoint-specific structures. Stream responses contain SSE frames; accepting LangGraph-shaped request fields does not implement every LangGraph server feature. Refer to the actual endpoint contract before integrating a client.

Durable checkpoints require explicit configuration. Keep thread IDs: thread metadata/list entries remain process-local even when state/history persist. Recovery memory and policy interfaces are Python APIs, not additional HTTP routes.
