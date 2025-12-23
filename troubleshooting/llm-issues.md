---
title: LLM Provider Issues
description: "Solutions for AI model access, API errors, and response handling problems"
parent: Troubleshooting
nav_order: 3
---

# LLM Provider Issues

> Solutions for AI model access, API errors, and response handling problems

## Table of Contents

- [Overview](#overview)
- [API Key Issues](#api-key-issues)
- [Rate Limiting](#rate-limiting)
- [Model Availability](#model-availability)
- [Response Errors](#response-errors)
- [Provider-Specific Issues](#provider-specific-issues)
- [Configuration Issues](#configuration-issues)
- [See Also](#see-also)

## Overview

LLM provider issues typically fall into these categories:

| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| Authentication | 401/403 errors | Invalid or missing API key |
| Rate Limits | 429 errors | Too many requests |
| Model | Model not found | Wrong model name, unavailable |
| Response | Parsing errors | Unexpected response format |
| Configuration | Connection errors | Wrong endpoint, provider settings |

## API Key Issues

### Invalid API Key

**Symptom:**
```
AuthenticationError: Invalid API key provided
```

**Solutions:**

1. **Verify API key is set:**
   ```bash
   # Check environment variable
   echo $OPENAI_API_KEY
   
   # Or for compatible APIs
   echo $OPENAI_COMPATIBLE_API_KEY
   ```

2. **Check key format:**
   ```bash
   # OpenAI keys start with "sk-"
   # Ensure no extra whitespace
   echo "$OPENAI_API_KEY" | cat -A
   ```

3. **Set in .env file:**
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

4. **Test API key:**
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

### API Key Not Found

**Symptom:**
```
ValueError: OPENAI_API_KEY environment variable not set
```

**Solutions:**

1. **Export in shell:**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

2. **Add to .env file:**
   ```
   # In project root .env
   OPENAI_API_KEY=sk-your-key-here
   ```

3. **Load .env in Python:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Key Permissions

**Symptom:**
```
PermissionError: API key does not have access to this model
```

**Solutions:**

1. **Check API key permissions in provider dashboard**

2. **Verify model access:**
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[].id'
   ```

3. **Use a model you have access to:**
   ```
   OPENAI_MODEL=gpt-3.5-turbo  # Instead of gpt-4
   ```

## Rate Limiting

### Too Many Requests

**Symptom:**
```
RateLimitError: Rate limit exceeded. Please retry after X seconds.
```

**Solutions:**

1. **Implement exponential backoff:**
   ```python
   import time
   from tenacity import retry, wait_exponential, stop_after_attempt
   
   @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
   def call_llm(prompt):
       return llm.invoke(prompt)
   ```

2. **Reduce request frequency:**
   ```python
   import time
   
   for item in items:
       result = llm.invoke(item)
       time.sleep(1)  # Add delay between requests
   ```

3. **Use batch processing:**
   ```python
   # Process in batches with delays
   batch_size = 10
   for i in range(0, len(items), batch_size):
       batch = items[i:i+batch_size]
       results = process_batch(batch)
       time.sleep(5)  # Delay between batches
   ```

### Token Limit Exceeded

**Symptom:**
```
InvalidRequestError: This model's maximum context length is 8192 tokens
```

**Solutions:**

1. **Truncate input:**
   ```python
   def truncate_messages(messages, max_tokens=6000):
       # Keep system message and recent messages
       return messages[:1] + messages[-5:]
   ```

2. **Use a model with larger context:**
   ```
   OPENAI_MODEL=gpt-4-turbo  # 128k context
   ```

3. **Summarize conversation history:**
   ```python
   # Periodically summarize old messages
   if len(messages) > 20:
       summary = summarize(messages[:-5])
       messages = [summary] + messages[-5:]
   ```

### Quota Exceeded

**Symptom:**
```
QuotaExceededError: You have exceeded your monthly quota
```

**Solutions:**

1. **Check usage in provider dashboard**

2. **Upgrade plan or add credits**

3. **Use a different provider temporarily:**
   ```
   OPENAI_COMPATIBLE_BASE_URL=https://alternative-api.com/v1
   OPENAI_COMPATIBLE_API_KEY=your-alternative-key
   ```

## Model Availability

### Model Not Found

**Symptom:**
```
NotFoundError: The model 'gpt-4' does not exist
```

**Solutions:**

1. **Check model name:**
   ```bash
   # List available models
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[].id'
   ```

2. **Use correct model identifier:**
   ```
   # Correct names
   OPENAI_MODEL=gpt-4
   OPENAI_MODEL=gpt-4-turbo
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Check provider-specific model names:**
   ```
   # For Azure
   AZURE_DEPLOYMENT_NAME=your-deployment-name
   
   # For compatible APIs
   OPENAI_COMPATIBLE_MODEL=your-model-name
   ```

### Model Deprecated

**Symptom:**
```
DeprecationWarning: Model 'gpt-3.5-turbo-0301' is deprecated
```

**Solutions:**

1. **Update to current model:**
   ```
   # Old
   OPENAI_MODEL=gpt-3.5-turbo-0301
   
   # New
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. **Check deprecation schedule in provider docs**

### Model Overloaded

**Symptom:**
```
ServiceUnavailableError: The model is currently overloaded
```

**Solutions:**

1. **Retry with backoff:**
   ```python
   @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(3))
   def call_llm(prompt):
       return llm.invoke(prompt)
   ```

2. **Use fallback model:**
   ```python
   try:
       result = gpt4.invoke(prompt)
   except ServiceUnavailableError:
       result = gpt35.invoke(prompt)
   ```

## Response Errors

### JSON Parsing Error

**Symptom:**
```
JSONDecodeError: Expecting value: line 1 column 1
```

**Solutions:**

1. **Check response format:**
   ```python
   response = llm.invoke(prompt)
   print(f"Raw response: {response}")
   ```

2. **Handle non-JSON responses:**
   ```python
   try:
       data = json.loads(response.content)
   except json.JSONDecodeError:
       # Handle as plain text
       data = {"text": response.content}
   ```

3. **Use structured output:**
   ```python
   from langchain_core.output_parsers import JsonOutputParser
   
   parser = JsonOutputParser()
   chain = llm | parser
   ```

### Structured Output Failure

**Symptom:**
```
OutputParserException: Could not parse LLM output
```

**Solutions:**

1. **Check if provider supports structured output:**
   ```python
   # Only OpenAI and Azure support with_structured_output
   if provider in ["openai", "azure"]:
       llm = llm.with_structured_output(MySchema)
   else:
       # Use JSON parsing fallback
       llm = llm | JsonOutputParser()
   ```

2. **Improve prompt for better formatting:**
   ```python
   prompt = """Return your response as valid JSON with this structure:
   {
       "field1": "value",
       "field2": "value"
   }
   """
   ```

### Incomplete Response

**Symptom:** Response cuts off mid-sentence

**Solutions:**

1. **Increase max_tokens:**
   ```python
   llm = ChatOpenAI(max_tokens=4096)
   ```

2. **Check for finish_reason:**
   ```python
   response = llm.invoke(prompt)
   if response.response_metadata.get("finish_reason") == "length":
       # Response was truncated
       pass
   ```

### Streaming Errors

**Symptom:** Streaming stops unexpectedly

**Solutions:**

1. **Handle stream interruptions:**
   ```python
   try:
       async for chunk in llm.astream(prompt):
           yield chunk
   except Exception as e:
       logger.error(f"Stream error: {e}")
       yield AIMessage(content="[Stream interrupted]")
   ```

2. **Set appropriate timeouts:**
   ```python
   llm = ChatOpenAI(request_timeout=120)
   ```

## Provider-Specific Issues

### OpenAI Issues

**Common problems:**

1. **Organization ID required:**
   ```
   OPENAI_ORGANIZATION=org-your-org-id
   ```

2. **API version mismatch:**
   ```python
   # Use latest client
   pip install --upgrade openai
   ```

### Azure OpenAI Issues

**Common problems:**

1. **Endpoint configuration:**
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-key
   AZURE_DEPLOYMENT_NAME=your-deployment
   ```

2. **API version:**
   ```
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

### OpenAI-Compatible APIs

**Common problems:**

1. **Base URL configuration:**
   ```
   OPENAI_COMPATIBLE_BASE_URL=https://api.provider.com/v1
   OPENAI_COMPATIBLE_API_KEY=your-key
   OPENAI_COMPATIBLE_MODEL=model-name
   ```

2. **Feature compatibility:**
   ```python
   # Some features may not be supported
   # Disable structured output for incompatible APIs
   use_structured = provider in ["openai", "azure"]
   ```

### Local Models (Ollama)

**Common problems:**

1. **Ollama not running:**
   ```bash
   # Start Ollama
   ollama serve
   
   # Check status
   curl http://localhost:11434/api/tags
   ```

2. **Model not pulled:**
   ```bash
   ollama pull llama2
   ```

## Configuration Issues

### Wrong Provider Settings

**Symptom:** Connection errors or unexpected behavior

**Solutions:**

1. **Check configuration in .env:**
   ```
   # For OpenAI
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4
   
   # For Azure
   LLM_PROVIDER=azure
   AZURE_OPENAI_ENDPOINT=https://...
   AZURE_OPENAI_API_KEY=...
   AZURE_DEPLOYMENT_NAME=...
   
   # For compatible APIs
   LLM_PROVIDER=openai_compatible
   OPENAI_COMPATIBLE_BASE_URL=https://...
   OPENAI_COMPATIBLE_API_KEY=...
   OPENAI_COMPATIBLE_MODEL=...
   ```

2. **Verify settings are loaded:**
   ```python
   from OHMind_agent.config import get_settings
   settings = get_settings()
   print(settings.get_llm_config())
   ```

### SSL/TLS Errors

**Symptom:**
```
SSLError: certificate verify failed
```

**Solutions:**

1. **Update certificates:**
   ```bash
   pip install --upgrade certifi
   ```

2. **For development only (not recommended for production):**
   ```python
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
   ```

### Proxy Issues

**Symptom:** Connection timeout behind corporate proxy

**Solutions:**

1. **Set proxy environment variables:**
   ```bash
   export HTTP_PROXY=http://proxy:port
   export HTTPS_PROXY=http://proxy:port
   ```

2. **Configure in Python:**
   ```python
   import os
   os.environ["HTTP_PROXY"] = "http://proxy:port"
   os.environ["HTTPS_PROXY"] = "http://proxy:port"
   ```

## Diagnostic Script

```bash
#!/bin/bash
# llm_diagnostics.sh

echo "=== LLM Provider Diagnostics ==="

# Check environment variables
echo ""
echo "1. Environment Variables:"
echo "   LLM_PROVIDER: ${LLM_PROVIDER:-not set}"
echo "   OPENAI_API_KEY: ${OPENAI_API_KEY:+set (${#OPENAI_API_KEY} chars)}"
echo "   OPENAI_MODEL: ${OPENAI_MODEL:-not set}"

# Test OpenAI API
echo ""
echo "2. API Connectivity:"
if [ -n "$OPENAI_API_KEY" ]; then
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        https://api.openai.com/v1/models \
        -H "Authorization: Bearer $OPENAI_API_KEY")
    if [ "$response" = "200" ]; then
        echo "   ✅ OpenAI API accessible"
    else
        echo "   ❌ OpenAI API returned HTTP $response"
    fi
else
    echo "   ⚠️  OPENAI_API_KEY not set"
fi

# Test model availability
echo ""
echo "3. Model Availability:"
if [ -n "$OPENAI_API_KEY" ]; then
    models=$(curl -s https://api.openai.com/v1/models \
        -H "Authorization: Bearer $OPENAI_API_KEY" | \
        jq -r '.data[].id' 2>/dev/null | grep -E "gpt-4|gpt-3.5" | head -5)
    if [ -n "$models" ]; then
        echo "   Available models:"
        echo "$models" | sed 's/^/     - /'
    else
        echo "   ❌ Could not list models"
    fi
fi

echo ""
echo "=== Diagnostics Complete ==="
```

## See Also

- [Troubleshooting Overview](./index.md) - Main troubleshooting guide
- [Configuration Reference](../configuration/index.md) - Environment setup
- [LLM Providers](../configuration/llm-providers.md) - Provider configuration
- [Backend API](../api/backend-api.md) - API documentation

---

*Last updated: 2025-12-23 | OHMind v0.1.0*
