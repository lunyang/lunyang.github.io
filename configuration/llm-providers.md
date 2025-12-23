---
title: "LLM Providers"
description: "Guide to configuring LLM providers in OHMind including OpenAI, Azure OpenAI, and OpenAI-compatible APIs"
category: "configuration"
tags: ["llm", "openai", "azure", "configuration", "api"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: Configuration Overview
nav_order: 3
---

# LLM Providers

> Complete guide to configuring Large Language Model providers in OHMind, including OpenAI, Azure OpenAI, and OpenAI-compatible APIs.

## Table of Contents

- [Overview](#overview)
- [Provider Priority](#provider-priority)
- [OpenAI-Compatible APIs](#openai-compatible-apis)
- [Direct OpenAI](#direct-openai)
- [Azure OpenAI](#azure-openai)
- [Model Selection](#model-selection)
- [Embedding Models](#embedding-models)
- [Rate Limiting](#rate-limiting)
- [Testing Configuration](#testing-configuration)
- [See Also](#see-also)

## Overview

OHMind supports multiple LLM providers through a unified configuration system. The system automatically detects which provider is configured and uses the appropriate client.

**Supported Providers:**

| Provider | Use Case | Configuration Prefix |
|----------|----------|---------------------|
| OpenAI-Compatible | Third-party APIs, local models | `OPENAI_COMPATIBLE_*` |
| Direct OpenAI | Standard OpenAI API | `OPENAI_API_KEY` |
| Azure OpenAI | Enterprise deployments | `AZURE_OPENAI_*` |

## Provider Priority

When multiple providers are configured, OHMind uses this priority order:

1. **Azure OpenAI** (if `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` are set)
2. **OpenAI-Compatible** (if `OPENAI_COMPATIBLE_API_KEY` and `OPENAI_COMPATIBLE_BASE_URL` are set)
3. **Direct OpenAI** (if `OPENAI_API_KEY` is set)

To use a specific provider, only configure that provider's variables.

## OpenAI-Compatible APIs

The most flexible option, supporting many providers with OpenAI-compatible endpoints.

### Configuration

```bash
OPENAI_COMPATIBLE_API_KEY=your-api-key
OPENAI_COMPATIBLE_BASE_URL=https://api.provider.com/v1
OPENAI_COMPATIBLE_MODEL=model-name
OPENAI_COMPATIBLE_EMBEDDING_MODEL=embedding-model-name
```

### Supported Providers

#### OpenRouter

Access multiple models through a single API.

```bash
OPENAI_COMPATIBLE_API_KEY=sk-or-v1-your-key
OPENAI_COMPATIBLE_BASE_URL=https://openrouter.ai/api/v1
OPENAI_COMPATIBLE_MODEL=anthropic/claude-3.5-sonnet
OPENAI_COMPATIBLE_EMBEDDING_MODEL=openai/text-embedding-3-large
```

**Popular models on OpenRouter:**
- `anthropic/claude-3.5-sonnet` - Best for complex reasoning
- `openai/gpt-4o` - OpenAI's latest
- `google/gemini-pro-1.5` - Google's multimodal model
- `meta-llama/llama-3.1-70b-instruct` - Open-source option

#### Together AI

High-performance inference for open models.

```bash
OPENAI_COMPATIBLE_API_KEY=your-together-key
OPENAI_COMPATIBLE_BASE_URL=https://api.together.xyz/v1
OPENAI_COMPATIBLE_MODEL=meta-llama/Llama-3.1-70B-Instruct-Turbo
OPENAI_COMPATIBLE_EMBEDDING_MODEL=togethercomputer/m2-bert-80M-8k-retrieval
```

**Recommended models:**
- `meta-llama/Llama-3.1-70B-Instruct-Turbo` - Fast, capable
- `mistralai/Mixtral-8x22B-Instruct-v0.1` - Strong reasoning
- `Qwen/Qwen2-72B-Instruct` - Multilingual support

#### Groq

Ultra-fast inference with custom hardware.

```bash
OPENAI_COMPATIBLE_API_KEY=gsk_your-groq-key
OPENAI_COMPATIBLE_BASE_URL=https://api.groq.com/openai/v1
OPENAI_COMPATIBLE_MODEL=llama-3.1-70b-versatile
```

**Available models:**
- `llama-3.1-70b-versatile` - Best quality
- `llama-3.1-8b-instant` - Fastest
- `mixtral-8x7b-32768` - Long context

#### DeepSeek

Cost-effective reasoning models.

```bash
OPENAI_COMPATIBLE_API_KEY=sk-your-deepseek-key
OPENAI_COMPATIBLE_BASE_URL=https://api.deepseek.com/v1
OPENAI_COMPATIBLE_MODEL=deepseek-chat
```

**Models:**
- `deepseek-chat` - General purpose
- `deepseek-reasoner` - Enhanced reasoning

#### Local Models (Ollama)

Run models locally with Ollama.

```bash
# First, start Ollama and pull a model
# ollama pull llama3.1:70b

OPENAI_COMPATIBLE_API_KEY=ollama
OPENAI_COMPATIBLE_BASE_URL=http://localhost:11434/v1
OPENAI_COMPATIBLE_MODEL=llama3.1:70b
```

**Setup Ollama:**

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models
ollama pull llama3.1:70b
ollama pull nomic-embed-text  # For embeddings

# Start server (usually automatic)
ollama serve
```

#### Local Models (LM Studio)

Use LM Studio's local server.

```bash
OPENAI_COMPATIBLE_API_KEY=lm-studio
OPENAI_COMPATIBLE_BASE_URL=http://localhost:1234/v1
OPENAI_COMPATIBLE_MODEL=local-model
```

#### vLLM

High-throughput serving for production.

```bash
OPENAI_COMPATIBLE_API_KEY=token
OPENAI_COMPATIBLE_BASE_URL=http://localhost:8000/v1
OPENAI_COMPATIBLE_MODEL=meta-llama/Llama-3.1-70B-Instruct
```

## Direct OpenAI

Standard OpenAI API configuration.

### Configuration

```bash
OPENAI_API_KEY=sk-your-openai-key
DEPLOYMENT_NAME=gpt-4o
EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
```

### Available Models

| Model | Context | Best For |
|-------|---------|----------|
| `gpt-4o` | 128K | Complex reasoning, multimodal |
| `gpt-4o-mini` | 128K | Cost-effective, fast |
| `gpt-4-turbo` | 128K | Previous generation |
| `gpt-3.5-turbo` | 16K | Simple tasks, lowest cost |

### Embedding Models

| Model | Dimensions | Best For |
|-------|------------|----------|
| `text-embedding-3-large` | 3072 | Highest quality |
| `text-embedding-3-small` | 1536 | Good balance |
| `text-embedding-ada-002` | 1536 | Legacy support |

## Azure OpenAI

Enterprise deployment through Azure.

### Configuration

```bash
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2024-02-15-preview
DEPLOYMENT_NAME=your-gpt4-deployment
EMBEDDING_DEPLOYMENT_NAME=your-embedding-deployment
```

### Setup Steps

1. **Create Azure OpenAI Resource:**
   - Go to Azure Portal
   - Create "Azure OpenAI" resource
   - Note the endpoint URL

2. **Deploy Models:**
   - In Azure OpenAI Studio, deploy models
   - Note deployment names (not model names)

3. **Get API Key:**
   - In Azure Portal, go to your resource
   - Keys and Endpoint → Copy Key 1

### Deployment Names

Azure uses deployment names, not model names:

```bash
# If you deployed gpt-4o as "my-gpt4-deployment"
DEPLOYMENT_NAME=my-gpt4-deployment

# If you deployed text-embedding-ada-002 as "my-embedding"
EMBEDDING_DEPLOYMENT_NAME=my-embedding
```

### API Versions

| Version | Status | Features |
|---------|--------|----------|
| `2024-02-15-preview` | Recommended | Latest features |
| `2024-05-01-preview` | Preview | Newest capabilities |
| `2023-12-01-preview` | Stable | Production ready |

## Model Selection

### Recommended Models by Task

| Task | Recommended Model | Alternative |
|------|-------------------|-------------|
| Complex reasoning | `gpt-4o`, `claude-3.5-sonnet` | `llama-3.1-70b` |
| Fast responses | `gpt-4o-mini`, `llama-3.1-8b` | `mixtral-8x7b` |
| Code generation | `gpt-4o`, `deepseek-coder` | `codellama-70b` |
| Long context | `gpt-4o`, `claude-3.5-sonnet` | `gemini-pro-1.5` |
| Cost-sensitive | `gpt-4o-mini`, `llama-3.1-8b` | `deepseek-chat` |

### Model Parameters

Configure model behavior:

```bash
# In .env
MAX_TOKENS=4096      # Maximum response length
TEMPERATURE=0.7      # Creativity (0.0-1.0)
```

**Temperature Guidelines:**

| Value | Use Case |
|-------|----------|
| 0.0-0.3 | Factual, deterministic responses |
| 0.4-0.7 | Balanced creativity and accuracy |
| 0.8-1.0 | Creative, varied responses |

## Embedding Models

Embedding models are used for the RAG system's vector search.

### Configuration

```bash
# OpenAI-Compatible
OPENAI_COMPATIBLE_EMBEDDING_MODEL=text-embedding-3-large

# Direct OpenAI
EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large

# Azure OpenAI
EMBEDDING_DEPLOYMENT_NAME=your-embedding-deployment
```

### Recommended Embedding Models

| Provider | Model | Dimensions |
|----------|-------|------------|
| OpenAI | `text-embedding-3-large` | 3072 |
| OpenAI | `text-embedding-3-small` | 1536 |
| Together | `togethercomputer/m2-bert-80M-8k-retrieval` | 768 |
| Ollama | `nomic-embed-text` | 768 |

### Embedding Considerations

- **Dimension consistency**: Use the same embedding model for indexing and querying
- **Re-indexing**: Changing embedding models requires re-indexing documents
- **Local vs. API**: Local models (Ollama) avoid API costs for large document sets

## Rate Limiting

### Handling Rate Limits

OHMind handles rate limits automatically, but you can optimize:

```bash
# Reduce concurrent requests
MAX_TOKENS=2048  # Smaller responses

# Use faster/cheaper models for simple tasks
OPENAI_COMPATIBLE_MODEL=gpt-4o-mini
```

### Provider Rate Limits

| Provider | Typical Limits |
|----------|----------------|
| OpenAI | 10K-90K TPM (varies by tier) |
| Azure | Configurable per deployment |
| OpenRouter | Varies by model |
| Together | 600 RPM free tier |
| Groq | 30 RPM free tier |

### Strategies

1. **Use streaming**: Reduces perceived latency
2. **Batch requests**: Combine related queries
3. **Cache responses**: For repeated queries
4. **Fallback models**: Use cheaper models for simple tasks

## Testing Configuration

### Verify LLM Configuration

```python
from OHMind_agent.config import get_settings

settings = get_settings()
llm_config = settings.get_llm_config()

print(f"Provider: {llm_config['provider']}")
print(f"Model: {llm_config.get('model', llm_config.get('deployment_name'))}")
```

### Test API Connection

```python
from langchain_openai import ChatOpenAI

# For OpenAI-Compatible
llm = ChatOpenAI(
    api_key="your-key",
    base_url="https://api.provider.com/v1",
    model="model-name"
)

response = llm.invoke("Hello, world!")
print(response.content)
```

### Verify Embedding Configuration

```python
from OHMind_agent.config import get_settings

settings = get_settings()
embedding_config = settings.get_embedding_config()

print(f"Provider: {embedding_config['provider']}")
print(f"Model: {embedding_config.get('model', embedding_config.get('deployment_name'))}")
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "No LLM configuration found" | Set at least one provider's credentials |
| "Invalid API key" | Verify key is correct and has permissions |
| "Model not found" | Check model name spelling and availability |
| "Rate limit exceeded" | Wait or upgrade API tier |
| "Context length exceeded" | Reduce `MAX_TOKENS` or use longer-context model |

### Debug Mode

Enable verbose logging:

```bash
LOG_LEVEL=DEBUG
```

### API Key Security

- Never commit API keys to version control
- Use environment variables or `.env` files
- Add `.env` to `.gitignore`
- Rotate keys periodically

## See Also

- [Configuration Overview](./index.md) - Configuration system overview
- [Environment Variables](./environment-variables.md) - All environment variables
- [LLM Issues](../troubleshooting/llm-issues.md) - Troubleshooting guide
- [RAG Agent](../agents/rag-agent.md) - Literature search configuration

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
