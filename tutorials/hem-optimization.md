---
title: "HEM Optimization Tutorial"
description: "Step-by-step guide to designing new cations for Hydroxide Exchange Membranes using PSO optimization"
category: "tutorials"
tags: ["tutorial", "hem", "pso", "optimization", "cation-design"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# HEM Optimization Tutorial

> Learn how to design new cations for Hydroxide Exchange Membranes using Particle Swarm Optimization (PSO).

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Part 1: Exploring the Design Space](#part-1-exploring-the-design-space)
- [Part 2: Running an Optimization](#part-2-running-an-optimization)
- [Part 3: Analyzing Results](#part-3-analyzing-results)
- [Part 4: Advanced Optimization](#part-4-advanced-optimization)
- [Expected Outputs](#expected-outputs)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [See Also](#see-also)

## Overview

**Difficulty:** 🟢 Beginner  
**Time:** 30 minutes  
**Requirements:** OHMind installed, LLM configured

In this tutorial, you will:

1. Explore available backbones and cation types
2. Run a PSO optimization to design new cations
3. Analyze and interpret the optimization results
4. Learn advanced optimization techniques

### What is HEM Optimization?

Hydroxide Exchange Membranes (HEMs) are critical components in fuel cells and electrolyzers. The performance of HEMs depends heavily on the cation structure attached to the polymer backbone. OHMind uses Particle Swarm Optimization (PSO) combined with a Junction Tree VAE to explore the chemical space and find optimal cation structures.

### Optimization Objectives

OHMind can optimize for multiple properties:

| Property | Code | Description |
|----------|------|-------------|
| Electrical Conductivity | `ec` | Ion transport efficiency |
| Electrochemical Stability Range | `esr` | Voltage window stability |
| Excess Water Uptake | `ewu` | Water management |
| Multi-objective | `multi` | Balanced optimization of all properties |

## Prerequisites

### System Setup

```bash
# Activate environment
conda activate OHMind

# Verify workspace
echo $OHMind_workspace
# Should show your workspace path

# Start the CLI
./start_OHMind_cli.sh
```

### Verify HEM Agent

The HEM agent should be available. You can verify by asking:

```
What agents and tools do you have available for HEM design?
```

**Expected response:** The agent should list HEMDesign tools including `ListBackbones`, `ListCations`, `HEMOptimizer`, etc.

## Part 1: Exploring the Design Space

### Step 1.1: List Available Backbones

First, let's see what polymer backbones are available for HEM design.

**Prompt:**
```
Using your HEMDesign tools, list all available polymer backbones 
for HEM design. Show their names and SMILES structures.
```

**Expected Output:**

The agent will return a table of backbones:

| Backbone | SMILES | Description |
|----------|--------|-------------|
| PBF_BB_1 | `[*]c1ccc(-c2ccc([*])cc2)cc1` | Polybiphenyl fluorene |
| PP_BB_1 | `[*]c1ccc([*])cc1` | Polyphenylene |
| PPO_BB_1 | `[*]Oc1ccc([*])cc1` | Poly(phenylene oxide) |
| ... | ... | ... |

### Step 1.2: List Available Cation Types

Next, explore the cation families that can be optimized.

**Prompt:**
```
List all available cation types for HEM optimization. 
Show their names and initial SMILES templates.
```

**Expected Output:**

| Cation Type | Initial SMILES | Description |
|-------------|----------------|-------------|
| piperidinium | `C[N+]1(C)CCCCC1` | 6-membered ring |
| imidazolium | `Cn1cc[n+](C)c1` | Aromatic 5-membered |
| pyrrolidinium | `C[N+]1(C)CCCC1` | 5-membered ring |
| ... | ... | ... |

### Step 1.3: Validate a Configuration

Before running optimization, validate your chosen configuration.

**Prompt:**
```
Validate an optimization configuration for:
- Backbone: PBF_BB_1
- Cation: piperidinium
- Property: multi (multi-objective)

Is this a valid combination?
```

**Expected Output:**

The agent will confirm whether the configuration is valid and explain any constraints.

## Part 2: Running an Optimization

### Step 2.1: Basic Optimization

Now let's run an actual optimization. Start with a small run to verify everything works.

**Prompt:**
```
Run a HEM optimization with these settings:
- Backbone: PBF_BB_1
- Cation type: piperidinium
- Property: multi (multi-objective)
- Particles: 100
- Steps: 3

This is a test run to verify the system works.
```

**What Happens:**

1. The HEM agent receives your request
2. It calls the `HEMOptimizer` tool
3. PSO optimization runs in the background
4. Progress is logged to the workspace
5. Results are saved as CSV files

**Expected Duration:** 2-5 minutes for a small run

### Step 2.2: Monitor Progress

While optimization runs, you can check progress.

**Prompt:**
```
Show me the latest log entries for the current HEM optimization.
```

**Expected Output:**

```
Step 1/3, max: 0.45, min: 0.12, mean: 0.28
Step 2/3, max: 0.52, min: 0.15, mean: 0.31
Step 3/3, max: 0.58, min: 0.18, mean: 0.35
```

### Step 2.3: Full Optimization Run

Once verified, run a more thorough optimization.

**Prompt:**
```
Run a full HEM optimization with these settings:
- Backbone: PBF_BB_1
- Cation type: piperidinium
- Property: multi (multi-objective)
- Particles: 200
- Steps: 10

Save results to the default workspace location.
```

**Expected Duration:** 10-20 minutes

## Part 3: Analyzing Results

### Step 3.1: Check Optimization Status

After the run completes, check the results.

**Prompt:**
```
Check the status of HEM optimization for PBF_BB_1 with piperidinium.
Show me the top 10 candidate molecules with their fitness scores.
```

**Expected Output:**

| Rank | SMILES | EC Score | EWU Score | ESR Score | Overall |
|------|--------|----------|-----------|-----------|---------|
| 1 | `CC[N+]1(CC)CCCCC1` | 0.82 | 0.75 | 0.88 | 0.81 |
| 2 | `C[N+]1(CC)CCCCC1` | 0.79 | 0.78 | 0.85 | 0.80 |
| 3 | ... | ... | ... | ... | ... |

### Step 3.2: Interpret Results

Ask the agent to explain the results.

**Prompt:**
```
Analyze the top 5 candidates from the PBF_BB_1 piperidinium optimization.
Explain:
1. What structural features make them good candidates?
2. How do their predicted properties compare?
3. Which would you recommend for experimental validation?
```

**Expected Output:**

The agent will provide:
- Structural analysis of top candidates
- Property comparisons
- Recommendations with reasoning

### Step 3.3: Visualize Candidates

Generate structure images for top candidates.

**Prompt:**
```
For the top 3 candidates from the optimization, generate 2D structure 
images and save them to the workspace.
```

**Expected Output:**

Images saved to `$OHMind_workspace/HEM/` or displayed in the interface.

## Part 4: Advanced Optimization

### Step 4.1: Single-Objective Optimization

Focus on a specific property.

**Prompt:**
```
Run a HEM optimization focused only on electrical conductivity (EC):
- Backbone: PP_BB_1
- Cation type: imidazolium
- Property: ec
- Particles: 150
- Steps: 8
```

### Step 4.2: Comparative Study

Compare different backbone-cation combinations.

**Prompt:**
```
Compare the optimization results for these combinations:
1. PBF_BB_1 + piperidinium
2. PP_BB_1 + piperidinium
3. PBF_BB_1 + imidazolium

For each, run a quick optimization (100 particles, 5 steps) and 
summarize which combination shows the most promise.
```

### Step 4.3: Constrained Optimization

Add constraints to the optimization.

**Prompt:**
```
Run a HEM optimization for PBF_BB_1 with piperidinium, but focus on 
candidates that:
1. Have molecular weight under 200 g/mol
2. Show high alkaline stability (ESR > 0.7)
3. Maintain reasonable conductivity (EC > 0.5)

Use multi-objective optimization with 200 particles for 10 steps.
```

## Expected Outputs

### File Locations

After optimization, find results in:

```
$OHMind_workspace/HEM/
├── best_solutions_PBF_BB_1_piperidinium.csv
├── best_fitness_history_PBF_BB_1_piperidinium.csv
└── optimization_PBF_BB_1_piperidinium.log
```

### CSV File Format

**best_solutions_*.csv:**

| Column | Description |
|--------|-------------|
| smiles | Candidate SMILES |
| ec_score | Electrical conductivity score |
| ewu_score | Water uptake score |
| esr_score | Stability score |
| overall_fitness | Combined fitness |
| step | Optimization step found |

**best_fitness_history_*.csv:**

| Column | Description |
|--------|-------------|
| step | Optimization step |
| max_fitness | Best fitness in swarm |
| min_fitness | Worst fitness in swarm |
| mean_fitness | Average fitness |

### Interpreting Scores

| Score Range | Interpretation |
|-------------|----------------|
| 0.8 - 1.0 | Excellent candidate |
| 0.6 - 0.8 | Good candidate |
| 0.4 - 0.6 | Moderate candidate |
| < 0.4 | Poor candidate |

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Backbone not found" | Invalid backbone name | Use `ListBackbones` to see valid names |
| "Optimization timeout" | Long computation | Increase timeout in mcp.json |
| "No results found" | Optimization didn't complete | Check logs with `ShowLogs` |
| "Permission denied" | Workspace not writable | Check `$HEM_SAVE_PATH` permissions |

### Checking Logs

```
Show me the full optimization log for PBF_BB_1 piperidinium.
```

### Killing Stuck Jobs

```
List any running HEM optimization jobs and kill any that appear stuck.
```

## Next Steps

After completing this tutorial:

1. **Try different combinations** - Explore other backbone-cation pairs
2. **Validate with QM** - Use [QM Calculations](./qm-calculations.md) to verify top candidates
3. **Run MD simulations** - Use [MD Simulations](./md-simulations.md) for property validation
4. **Search literature** - Use [Literature Search](./literature-search.md) to compare with known compounds

### Suggested Follow-up Prompts

```
For the top candidate from my optimization, run a QM calculation 
to verify its LUMO energy and alkaline stability.
```

```
Search the literature for similar cation structures and compare 
their reported properties with my optimization predictions.
```

## See Also

- [HEM Agent](../agents/hem-agent.md) - Agent capabilities
- [HEMDesign MCP Server](../mcp-servers/hem-server.md) - Available tools
- [OHPSO Module](../core-library/ohpso.md) - PSO algorithm details
- [Multi-Step Workflows](./multi-step-workflows.md) - Complex pipelines

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
