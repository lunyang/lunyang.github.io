---
permalink: /api/workflow-api/
layout: default
title: "Workflow API Reference"
parent: "API Reference"
nav_order: 2
last_updated: "2026-09-23"
---

# Workflow API Reference

`OHMind_agent.graph.workflow.create_workflow()` compiles the multi-agent graph:

```python
create_workflow(
    llm_config,
    mcp_clients,
    retriever=None,
    session_manager=None,
    checkpointer=None,
    store=None,
    memory_service=None,
    memory_config=None,
)
```

`mcp_clients` is the legacy client map; the application passes a persistent `session_manager`. Without an explicit checkpointer, the factory uses process-local `MemorySaver` even if an environment variable elsewhere requests durable state.

## Persistence lifetime

The following is an integration pattern inside an async application that has already initialized `session_manager` and optional `retriever`:

```python
from contextlib import AsyncExitStack
from OHMind_agent.config import get_settings
from OHMind_agent.memory.lifecycle import initialize_persistence
from OHMind_agent.graph.workflow import create_workflow

async def run(session_manager, retriever=None):
    settings = get_settings()
    async with AsyncExitStack() as stack:
        resources = await initialize_persistence(settings, stack)
        workflow = create_workflow(
            settings.get_llm_config(),
            {},
            retriever,
            session_manager=session_manager,
            checkpointer=resources.checkpointer,
            store=resources.store,
            memory_service=resources.memory,
            memory_config=settings.get_memory_config(),
        )
        from langchain_core.messages import HumanMessage
        return await workflow.ainvoke(
            {"messages": [HumanMessage(content="Describe the available HEM tools.")]},
            {"configurable": {"thread_id": "example-thread"}},
        )
```

Keep the exit stack alive for the whole workflow lifetime. Reuse the compiled workflow/checkpointer across requests and use stable thread IDs. Custom callers are responsible for environment loading, session setup, scope configuration, and migrations.

## State and recovery

Use `await workflow.aget_state(config)` and iterate `workflow.aget_state_history(config)` for snapshots. `AgentState` includes structured tool executions, failure events, memory queries/references, recovery actions, validator reports, and run/policy identity; see [State Management]({% link architecture/state-management.md %}).

The current graph's general error route selects recovery and then escalates because tool-specific execution evidence is absent. It does not automatically commit an episode or patch code. The PSO tool has a separate bounded checkpoint recovery path.
