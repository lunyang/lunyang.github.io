---
permalink: /tutorials/pso-resume/
layout: default
title: "Resume PSO Optimization"
parent: "Tutorials"
nav_order: 7
last_updated: "2026-09-23"
---

# Resume PSO Optimization

This workflow needs the scientific resources from [Installation]({% link getting-started/installation.md %}#model-and-scoring-resources) and a working HEM MCP service. It does not require recovery memory or a conversation database.

## Start a small job

Ask the agent to use `optimize_hem_design` with explicit values, for example:

```json
{
  "backbone": "PBF_BB_1",
  "cation_name": "piperidinium",
  "property": "multi",
  "num_part": 5,
  "steps": 3,
  "seed": 42,
  "save_path": "/absolute/path/to/hem-runs"
}
```

These are MCP tool arguments, not a standalone HTTP endpoint. Confirm the backbone and cation are supported in your checkout. The tool starts a background job and returns its actual run directory. Record that path and the job ID.

## Inspect progress

Use the HEM status and log tools for the returned directory. The run records `job_state.json`, a checkpoint (normally `checkpoints/optimizer.json`), and an optimization log. Recovery events are appended to `recovery_trace.jsonl` when they occur. A missing trace on a run with no recovery events is not itself an error.

Checkpoints are saved before iteration and after completed steps. They contain optimizer/swarm state, random-generator state, and configuration metadata with integrity checks. They do not bundle inference models or scoring functions. Matching external resources must still be available.

## Resume an interrupted run

Only resume after confirming the old worker has stopped. Keep the original checkpoint as evidence and submit `optimize_hem_design` again with the same backbone, cation, property, particle count, seed, and scoring weights. Add:

```json
{
  "resume_from": "/absolute/path/to/original-run/checkpoints/optimizer.json",
  "steps": 5
}
```

This fragment supplements the full original arguments. **`steps` is the total target iteration count**, not the number of additional steps. A checkpoint at iteration 3 with `steps=5` performs two further iterations. A target below the checkpoint iteration is rejected.

The core checks saved metadata against the requested configuration and rejects mismatches. Hash/schema failures require an intact checkpoint, not bypassing validation. The resumed tool call creates a new job/run directory; use the returned location to follow the new job.

## Verify completion or recovery

Inspect the terminal job status, result files, and checkpoint iteration. An automatic timeout retry records `failure_diagnosed`; a successful retry also records `post_recovery_validation` with checks for exactly one iteration of progress, valid checkpoint reload, and respected retry budget. The default retry budget is one per step in the core, not an exposed `optimize_hem_design` argument.

A seed records Python/NumPy randomness and supports provenance, but does not guarantee bitwise reproducibility across GPU, model, or library changes. Memory-based decision selection and episode recording require explicit integration; ordinary checkpoint retries do not automatically create learned policies.
