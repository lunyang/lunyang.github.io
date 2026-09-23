---
permalink: /api/backend-api/
layout: default
title: "Backend API Reference"
parent: "API Reference"
nav_order: 1
last_updated: "2026-09-23"
---

# Backend API Reference

The combined launcher normally exposes the FastAPI backend at `http://localhost:8005`. The web UI uses port `8000`. Source: `OHMind_backend.py`.

## Endpoints

| Method | Path | Behavior |
|---|---|---|
| GET | `/` | Service identity and initialized MCP/RAG information |
| GET | `/health` | Liveness response `{"status":"healthy"}` |
| GET | `/info` | Graph/assistant metadata |
| POST | `/threads` | Create a thread; optional `metadata` object |
| GET | `/threads` | Process-local thread registry |
| GET | `/threads/{thread_id}` | Process-local metadata, 404 if absent |
| POST | `/threads/{thread_id}/runs` | Execute a request and return result/tool events |
| POST | `/threads/{thread_id}/runs/stream` | Stream run events as server-sent events |
| GET | `/assistants` | Available assistant descriptions |
| GET, POST | `/threads/{thread_id}/history` | Actual LangGraph checkpoint snapshots |
| GET | `/threads/{thread_id}/state` | Actual latest LangGraph checkpoint snapshot |

No memory/policy administration routes are implemented in this backend. Use the [Python APIs]({% link api/memory-recovery.md %}) for explicit integrations. Backend routes do not establish a multi-tenant authorization boundary; use this service within your configured deployment boundary.

## Create a thread and run

```bash
curl --fail -X POST http://localhost:8005/threads \
  -H 'Content-Type: application/json' -d '{"metadata":{}}'
```

The response contains `thread_id`. Retain it for subsequent requests:

```bash
THREAD_ID=replace-with-returned-thread-id
curl --fail -X POST "http://localhost:8005/threads/$THREAD_ID/runs" \
  -H 'Content-Type: application/json' \
  -d '{"input":{"content":"Describe the available HEM tools."}}'
```

The non-streaming response includes `run_id`, `thread_id`, `status`, `result`, and `tool_events`. A completed agent run can contain a tool failure or an asynchronously started scientific job; check the result and job status separately.

`RunRequest` accepts `input`, `messages`, `config`, `stream_mode`, and `multitask_strategy`. The current handlers construct their own graph configuration; accepting a field does not mean all LangGraph server semantics are implemented. For simple input, use `input.content`. Alternatively, send `messages` with message `type` and string content (or text-content blocks); the handler extracts the last message. Missing content produces HTTP 400.

## Streaming

Use the same body with `/runs/stream` and `curl -N`. Consume SSE `data:` frames rather than treating the response as one JSON object. The handler produces run metadata and token/tool/state/error events; clients should handle the event kinds they use and surface errors.

## Checkpoints across restarts

```bash
curl --fail "http://localhost:8005/threads/$THREAD_ID/state"
curl --fail "http://localhost:8005/threads/$THREAD_ID/history"
```

Snapshots contain `values`, `next`, `config`, `metadata`, `created_at`, `parent_config`, and `tasks`. Unknown IDs with no checkpoint and no current registry entry return 404. With PostgreSQL checkpoints enabled, state/history remain queryable by saved ID across backend restarts. The separate thread registry is not durable; `/threads` can be empty and the metadata endpoint can return 404 for a thread whose graph checkpoints still exist.

See [persistence configuration]({% link configuration/memory-persistence.md %}) and [verification tutorial]({% link tutorials/memory-and-recovery.md %}).
