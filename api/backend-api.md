# Backend API Reference

> FastAPI REST endpoints for interacting with the OHMind multi-agent system

## Table of Contents

- [Overview](#overview)
- [System Endpoints](#system-endpoints)
- [Thread Management](#thread-management)
- [Run Execution](#run-execution)
- [Assistant Information](#assistant-information)
- [Request/Response Models](#requestresponse-models)
- [Error Codes](#error-codes)
- [Examples](#examples)
- [See Also](#see-also)

## Overview

The OHMind backend is a FastAPI application that provides LangGraph-compatible endpoints for multi-agent interaction. It supports both synchronous and streaming responses.

### Base Configuration

```python
# Default settings
API_HOST = "0.0.0.0"
API_PORT = 8005

# CORS enabled for all origins (development)
# Configure ALLOWED_ORIGINS for production
```

### Starting the Backend

```bash
# Using the startup script
./start_OHMind.sh

# Or manually with uvicorn
uvicorn OHMind_backend:app --host 0.0.0.0 --port 8005
```

## System Endpoints

### GET /

Root endpoint returning system status.

**Response:**

```json
{
  "name": "HEM Design Agent System",
  "version": "0.1.0",
  "status": "running",
  "mcp_clients": ["OHMind-Chem", "OHMind-HEMDesign", "OHMind-ORCA"],
  "rag_enabled": true
}
```

**Example:**

```bash
curl http://localhost:8005/
```

---

### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy"
}
```

**Example:**

```bash
curl http://localhost:8005/health
```

---

### GET /info

Graph information endpoint (LangGraph SDK compatible).

**Response:**

```json
{
  "assistant_id": "agent",
  "graph_id": "hem_design_graph",
  "name": "HEM Design Multi-Agent System",
  "description": "LangGraph-based multi-agent system for hydroxide exchange membrane design",
  "version": "0.1.0",
  "mcp_clients": ["OHMind-Chem", "OHMind-HEMDesign", "OHMind-ORCA", "OHMind-Multiwfn", "OHMind-GROMACS"],
  "rag_enabled": true,
  "agents": [
    "supervisor",
    "hem_agent",
    "chemistry_agent",
    "qm_agent",
    "md_agent",
    "rag_agent",
    "web_search_agent",
    "summary_agent"
  ]
}
```

**Example:**

```bash
curl http://localhost:8005/info
```

## Thread Management

Threads represent conversation sessions with persistent state.

### POST /threads

Create a new conversation thread.

**Request Body:**

```json
{
  "metadata": {
    "purpose": "hem_optimization",
    "user_id": "optional_user_identifier"
  }
}
```

**Response:**

```json
{
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Example:**

```bash
curl -X POST http://localhost:8005/threads \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"purpose": "testing"}}'
```

---

### GET /threads

List all threads.

**Response:**

```json
{
  "threads": [
    {
      "thread_id": "550e8400-e29b-41d4-a716-446655440000",
      "metadata": {"purpose": "hem_optimization"},
      "messages": [],
      "created_at": null
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8005/threads
```

---

### GET /threads/{thread_id}

Get thread information.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| thread_id | string | UUID of the thread |

**Response:**

```json
{
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "metadata": {"purpose": "hem_optimization"},
  "messages": [
    {"role": "user", "content": "Design new cations"},
    {"role": "assistant", "content": "I'll help you design..."}
  ]
}
```

**Error Response (404):**

```json
{
  "detail": "Thread not found"
}
```

**Example:**

```bash
curl http://localhost:8005/threads/550e8400-e29b-41d4-a716-446655440000
```

---

### GET /threads/{thread_id}/history

Get thread message history (LangGraph SDK compatible).

**Response:**

```json
[
  {
    "values": {
      "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
      ]
    },
    "next": [],
    "config": {
      "configurable": {
        "thread_id": "550e8400-e29b-41d4-a716-446655440000",
        "checkpoint_id": "checkpoint-uuid"
      }
    },
    "metadata": {},
    "created_at": null,
    "parent_config": null
  }
]
```

**Example:**

```bash
curl http://localhost:8005/threads/550e8400-e29b-41d4-a716-446655440000/history
```

---

### GET /threads/{thread_id}/state

Get current thread state.

**Response:**

```json
{
  "values": {
    "messages": [...],
    "next": "supervisor",
    "mcp_results": {},
    "current_operation": "Idle"
  },
  "next": [],
  "config": {
    "configurable": {
      "thread_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

**Example:**

```bash
curl http://localhost:8005/threads/550e8400-e29b-41d4-a716-446655440000/state
```

## Run Execution

### POST /threads/{thread_id}/runs

Execute a run (non-streaming).

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| thread_id | string | UUID of the thread |

**Request Body:**

```json
{
  "input": {
    "content": "Your message here"
  },
  "config": {
    "configurable": {}
  }
}
```

Or using LangGraph SDK format:

```json
{
  "messages": [
    {
      "type": "human",
      "content": "Your message here"
    }
  ],
  "config": {}
}
```

**Response:**

```json
{
  "run_id": "run-uuid",
  "thread_id": "thread-uuid",
  "status": "completed",
  "result": {
    "messages": [
      {"type": "human", "content": "Your message"},
      {"type": "ai", "content": "Agent response..."}
    ],
    "next": "FINISH",
    "mcp_results": {}
  },
  "tool_events": [
    {"type": "tool_start", "tool": "list_backbones", "input": "..."},
    {"type": "tool_end", "output": "..."}
  ]
}
```

**Example:**

```bash
curl -X POST http://localhost:8005/threads/550e8400-e29b-41d4-a716-446655440000/runs \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "content": "List available HEM backbones"
    }
  }'
```

---

### POST /threads/{thread_id}/runs/stream

Execute a run with streaming response (SSE).

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| thread_id | string | UUID of the thread |

**Request Body:**

```json
{
  "input": {
    "content": "Your message here"
  },
  "stream_mode": "values",
  "config": {}
}
```

**Stream Mode Options:**

| Mode | Description |
|------|-------------|
| `values` | Stream state values (default) |
| `updates` | Stream state updates |

**Response (SSE Stream):**

```
event: metadata
data: {"run_id": "run-uuid", "thread_id": "thread-uuid"}

event: custom
data: {"type": "agent_status", "agent": "supervisor", "display_name": "Supervisor Agent", "status": "active"}

event: values
data: {"event": "values", "data": {"messages": [...]}}

event: custom
data: {"type": "tool_start", "tool_name": "optimize_hem_design", "agent": "hem_agent", "input": "..."}

event: custom
data: {"type": "tool_end", "output": "Optimization started...", "agent": "hem_agent"}

event: values
data: {"messages": [...], "next": "FINISH"}

event: end
data: {"status": "completed"}
```

**SSE Event Types:**

| Event | Data Fields | Description |
|-------|-------------|-------------|
| `metadata` | run_id, thread_id | Initial run metadata |
| `values` | State object | State updates |
| `custom` | type, agent, ... | Agent/tool events |
| `error` | error, type | Error information |
| `end` | status | Stream completion |

**Custom Event Types:**

| Type | Fields | Description |
|------|--------|-------------|
| `agent_status` | agent, display_name, status | Agent activation |
| `tool_start` | tool_name, agent, input, run_id | Tool execution start |
| `tool_end` | output, agent, run_id | Tool execution end |
| `tool_error` | error, agent, run_id | Tool execution error |

**Example (curl):**

```bash
curl -N -X POST http://localhost:8005/threads/550e8400-e29b-41d4-a716-446655440000/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "content": "Optimize piperidinium cations for PBF_BB_1"
    }
  }'
```

**Example (Python with sseclient):**

```python
import requests
import sseclient
import json

def stream_response(thread_id: str, message: str):
    url = f"http://localhost:8005/threads/{thread_id}/runs/stream"
    
    response = requests.post(
        url,
        json={"input": {"content": message}},
        stream=True,
        headers={"Accept": "text/event-stream"}
    )
    
    client = sseclient.SSEClient(response)
    
    for event in client.events():
        data = json.loads(event.data)
        
        if event.event == "custom":
            event_type = data.get("type")
            if event_type == "agent_status":
                print(f"🤖 {data['display_name']} activated")
            elif event_type == "tool_start":
                print(f"🔧 Tool: {data['tool_name']}")
            elif event_type == "tool_end":
                print(f"✅ Result: {data['output'][:100]}...")
        
        elif event.event == "values":
            messages = data.get("messages", [])
            if messages:
                last_msg = messages[-1]
                if isinstance(last_msg, dict) and last_msg.get("type") == "ai":
                    print(f"💬 {last_msg['content'][:200]}...")
        
        elif event.event == "end":
            print("✨ Stream completed")
            break

# Usage
stream_response("your-thread-id", "Design new HEM cations")
```

## Assistant Information

### GET /assistants

List available assistants.

**Response:**

```json
{
  "assistants": [
    {
      "assistant_id": "agent",
      "graph_id": "hem_design_graph",
      "name": "HEM Design Assistant",
      "description": "Multi-agent system for hydroxide exchange membrane design",
      "config": {
        "configurable": {}
      },
      "metadata": {
        "created_by": "langgraph"
      },
      "capabilities": [
        "HEM optimization",
        "Chemistry operations",
        "Quantum mechanics",
        "Molecular dynamics",
        "Literature search",
        "Web search"
      ]
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8005/assistants
```

## Request/Response Models

### MessageContent

```python
class MessageContent(BaseModel):
    type: str = "text"
    text: str
```

### Message

```python
class Message(BaseModel):
    id: Optional[str] = None
    type: str = "human"  # "human" or "ai"
    content: Union[List[MessageContent], str]
```

### RunRequest

```python
class RunRequest(BaseModel):
    input: Optional[Dict[str, Any]] = None
    messages: Optional[List[Message]] = None
    config: Optional[Dict[str, Any]] = None
    stream_mode: Optional[Union[str, List[str]]] = "values"
    multitask_strategy: Optional[str] = None
```

### ThreadCreate

```python
class ThreadCreate(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
```

## Error Codes

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | Bad Request | Missing or invalid message content |
| 404 | Not Found | Thread not found |
| 500 | Internal Server Error | Workflow execution error |

### Error Response Format

```json
{
  "detail": "Error description"
}
```

### Common Error Scenarios

**Missing Message Content (400):**

```json
{
  "detail": "No message content provided"
}
```

**Thread Not Found (404):**

```json
{
  "detail": "Thread not found"
}
```

**Workflow Error (500):**

```json
{
  "detail": "MCP server connection failed: OHMind-HEMDesign"
}
```

## Examples

### Complete Workflow Example

```python
import requests
import json

BASE_URL = "http://localhost:8005"

# 1. Check system health
health = requests.get(f"{BASE_URL}/health").json()
print(f"System status: {health['status']}")

# 2. Get system info
info = requests.get(f"{BASE_URL}/info").json()
print(f"Available agents: {info['agents']}")

# 3. Create a thread
thread = requests.post(
    f"{BASE_URL}/threads",
    json={"metadata": {"purpose": "hem_design"}}
).json()
thread_id = thread["thread_id"]
print(f"Created thread: {thread_id}")

# 4. Send a message
result = requests.post(
    f"{BASE_URL}/threads/{thread_id}/runs",
    json={"input": {"content": "What backbones are available?"}}
).json()

# 5. Extract response
if "result" in result:
    messages = result["result"].get("messages", [])
    for msg in messages:
        if hasattr(msg, "type") or (isinstance(msg, dict) and msg.get("type") == "ai"):
            content = msg.get("content") if isinstance(msg, dict) else msg.content
            print(f"Assistant: {content}")

# 6. Get thread history
history = requests.get(f"{BASE_URL}/threads/{thread_id}/history").json()
print(f"Thread has {len(history)} checkpoints")
```

### HEM Optimization Example

```python
import requests
import sseclient
import json

BASE_URL = "http://localhost:8005"

# Create thread
thread = requests.post(f"{BASE_URL}/threads", json={}).json()
thread_id = thread["thread_id"]

# Start HEM optimization with streaming
response = requests.post(
    f"{BASE_URL}/threads/{thread_id}/runs/stream",
    json={
        "input": {
            "content": "Optimize piperidinium cations for PBF_BB_1 backbone with multi-objective HEM performance. Use 100 particles and 20 steps."
        }
    },
    stream=True,
    headers={"Accept": "text/event-stream"}
)

client = sseclient.SSEClient(response)

for event in client.events():
    data = json.loads(event.data)
    
    if event.event == "custom":
        if data.get("type") == "tool_start":
            print(f"🔧 Starting: {data.get('tool_name')}")
        elif data.get("type") == "tool_end":
            print(f"✅ Completed: {data.get('output', '')[:100]}")
    
    elif event.event == "end":
        print("🎉 Optimization complete!")
        break
```

### Batch Processing Example

```python
import requests
import json
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8005"

def process_backbone(backbone: str):
    """Process a single backbone optimization."""
    # Create thread
    thread = requests.post(f"{BASE_URL}/threads", json={}).json()
    thread_id = thread["thread_id"]
    
    # Run optimization
    result = requests.post(
        f"{BASE_URL}/threads/{thread_id}/runs",
        json={
            "input": {
                "content": f"Optimize piperidinium cations for {backbone} backbone"
            }
        }
    ).json()
    
    return {
        "backbone": backbone,
        "thread_id": thread_id,
        "status": result.get("status"),
        "result": result.get("result")
    }

# Process multiple backbones
backbones = ["PBF_BB_1", "PP_BB_1", "PX_BB_1"]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_backbone, backbones))

for r in results:
    print(f"{r['backbone']}: {r['status']}")
```

## See Also

- [API Overview](./index.md) - API architecture and quick start
- [Workflow API](./workflow-api.md) - LangGraph workflow details
- [Session Manager](./session-manager.md) - MCP connection management
- [Architecture Overview](../architecture/overview.md) - System architecture
- [Tutorials](../tutorials/index.md) - Step-by-step guides

---

*Last updated: 2025-12-23 | OHMind v0.1.0*
