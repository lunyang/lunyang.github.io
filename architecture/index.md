---
permalink: /architecture/
title: Architecture
description: "OHMind system architecture and design documentation"
nav_order: 3
has_children: true
last_updated: "2026-09-23"
---

# Architecture

Understanding the OHMind system architecture and component interactions.

- [System Overview]({% link architecture/overview.md %}) - High-level architecture
- [Multi-Agent System]({% link architecture/multi-agent-system.md %}) - Agent workflow and routing
- [State Management]({% link architecture/state-management.md %}) - AgentState and data flow
- [MCP Integration]({% link architecture/mcp-integration.md %}) - MCP protocol and servers

## Persistence and recovery

- [Recovery Memory]({% link architecture/memory.md %}): ledger, trust checks, scoped recall, and outbox replay.
- [Recovery and Policies]({% link architecture/recovery.md %}): execution boundaries, bounded retries, promotion, and rollback.
