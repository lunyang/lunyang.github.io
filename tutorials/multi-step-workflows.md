---
title: "Multi-Step Workflows Tutorial"
description: "Advanced guide to combining multiple OHMind agents for complex computational chemistry pipelines"
category: "tutorials"
tags: ["tutorial", "advanced", "workflow", "multi-agent", "pipeline"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# Multi-Step Workflows Tutorial

> Learn how to combine multiple OHMind agents for complex, end-to-end computational chemistry workflows.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Workflow 1: Literature-Guided Design](#workflow-1-literature-guided-design)
- [Workflow 2: Design-to-Validation Pipeline](#workflow-2-design-to-validation-pipeline)
- [Workflow 3: Comprehensive Property Prediction](#workflow-3-comprehensive-property-prediction)
- [Workflow 4: Comparative Analysis](#workflow-4-comparative-analysis)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

**Difficulty:** 🔴 Advanced  
**Time:** 90 minutes  
**Requirements:** All external software configured (ORCA, GROMACS, Multiwfn)

In this tutorial, you will:

1. Chain multiple agents for complex tasks
2. Build end-to-end design-to-validation pipelines
3. Combine computational methods for comprehensive analysis
4. Learn workflow orchestration best practices

### Why Multi-Step Workflows?

Real research problems often require multiple computational approaches:

```mermaid
graph LR
    A[Literature] --> B[Design]
    B --> C[QM Validation]
    C --> D[MD Simulation]
    D --> E[Analysis]
    E --> F[Report]
```

OHMind's multi-agent architecture enables seamless transitions between:
- **RAG Agent** → Literature search and synthesis
- **HEM Agent** → Molecular design and optimization
- **Chemistry Agent** → Structure manipulation
- **QM Agent** → Electronic structure calculations
- **MD Agent** → Dynamics simulations
- **Multiwfn Agent** → Wavefunction analysis

## Prerequisites

### Full System Configuration

Ensure all components are configured:

```bash
# Check all paths
echo "ORCA: $OHMind_ORCA"
echo "Multiwfn: $MULTIWFN_PATH"
echo "Workspace: $OHMind_workspace"

# Verify GROMACS
gmx --version

# Check Qdrant (for RAG)
echo "Qdrant: ${QDRANT_PATH:-$QDRANT_URL}"
```

### Start the Interface

```bash
cd OHMind
./start_OHMind_cli.sh
```

## Workflow 1: Literature-Guided Design

### Objective

Use literature insights to guide HEM optimization, then validate top candidates.

### Step 1: Literature Research

**Prompt:**
```
Search the literature for the most stable cation types for AEMs.
Identify:
1. Top 3 cation families by stability
2. Key structural features for stability
3. Recommended design principles
```

**Expected Output:**

```
Literature Analysis:

Top Cation Families:
1. Spirocyclic piperidinium (best stability)
2. N-alkyl piperidinium (good balance)
3. Sterically hindered imidazolium (good conductivity)

Key Structural Features:
- No β-hydrogens on N-substituents
- Steric protection around nitrogen
- Saturated ring systems preferred

Design Principles:
- Use bulky alkyl groups (ethyl, isopropyl)
- Avoid benzylic positions
- Consider spirocyclic architectures
```

### Step 2: Guided Optimization

**Prompt:**
```
Based on the literature findings, run HEM optimization for:
- Backbone: PBF_BB_1
- Cation type: piperidinium (literature-recommended)
- Property: multi-objective
- Particles: 200
- Steps: 10

Focus on candidates with structural features identified in literature.
```

**Expected Duration:** 15-20 minutes

### Step 3: QM Validation

**Prompt:**
```
For the top 3 candidates from the optimization:
1. Run geometry optimization at B3LYP/def2-SVP
2. Calculate LUMO energies
3. Compare with literature stability criteria (LUMO > -2.0 eV)
4. Rank by predicted stability
```

**Expected Output:**

| Rank | SMILES | LUMO (eV) | Stability |
|------|--------|-----------|-----------|
| 1 | CC[N+]1(CC)CCCCC1 | -1.85 | ✓ Good |
| 2 | C[N+]1(CC)CCCCC1 | -2.05 | ~ Marginal |
| 3 | C[N+]1(C)CCCCC1 | -2.25 | ✗ Concerning |

### Step 4: Final Report

**Prompt:**
```
Summarize the literature-guided design workflow:
1. Literature insights used
2. Optimization results
3. QM validation findings
4. Final recommendations

Format as a brief research report.
```

## Workflow 2: Design-to-Validation Pipeline

### Objective

Complete pipeline from molecular design through multi-level validation.

### Step 1: Initial Design

**Prompt:**
```
Design a new piperidinium cation for AEMs with these requirements:
1. High predicted alkaline stability
2. Molecular weight < 200 g/mol
3. Synthesizable from common precursors

Generate 5 candidate structures with SMILES.
```

### Step 2: Property Screening

**Prompt:**
```
For the 5 candidate cations:
1. Calculate molecular weight
2. Estimate synthetic accessibility
3. Check for problematic functional groups
4. Rank by overall suitability

Eliminate any that don't meet criteria.
```

### Step 3: QM Characterization

**Prompt:**
```
For the remaining candidates, run QM calculations:
1. Geometry optimization (B3LYP/def2-SVP)
2. Frequency calculation (verify minimum)
3. Property extraction:
   - HOMO/LUMO energies
   - Charges on nitrogen
   - Dipole moment

Create a comparison table.
```

**Expected Duration:** 30-45 minutes for multiple molecules

### Step 4: Detailed Analysis

**Prompt:**
```
For the best candidate from QM screening:
1. Run Multiwfn analysis on the wavefunction
2. Visualize LUMO orbital
3. Identify potential degradation sites
4. Calculate electrophilicity index
```

### Step 5: MD Validation

**Prompt:**
```
Build a small AEM system with the best candidate:
1. Create polymer (DP=10, 3 chains)
2. Add water (λ=15)
3. Run 500 ps MD at 400 K
4. Calculate OH⁻ diffusion coefficient
5. Estimate conductivity
```

**Expected Duration:** 30-45 minutes

### Step 6: Comprehensive Report

**Prompt:**
```
Generate a comprehensive validation report for the best candidate:

Include:
1. Structure and properties
2. QM results (energies, orbitals, charges)
3. Wavefunction analysis (degradation sites)
4. MD results (diffusion, conductivity)
5. Comparison with literature values
6. Recommendation for experimental synthesis
```

## Workflow 3: Comprehensive Property Prediction

### Objective

Multi-scale property prediction combining QM and MD methods.

### Step 1: Select Target

**Prompt:**
```
I want to comprehensively characterize this cation for AEM use:
SMILES: CC[N+]1(CC)CCCCC1 (N,N-diethylpiperidinium)

Create a characterization plan covering:
1. Electronic properties (QM)
2. Thermodynamic properties (QM)
3. Transport properties (MD)
4. Stability assessment
```

### Step 2: Electronic Structure

**Prompt:**
```
Run electronic structure calculations:
1. Optimize geometry at B3LYP-D3BJ/def2-TZVP
2. Calculate:
   - Frontier orbital energies
   - Atomic charges (Hirshfeld)
   - Dipole and quadrupole moments
   - Electrostatic potential
```

### Step 3: Thermochemistry

**Prompt:**
```
Calculate thermochemical properties:
1. Frequency calculation for ZPE
2. Gibbs free energy at 298 K and 400 K
3. Proton affinity (if applicable)
4. Solvation energy in water
```

### Step 4: Wavefunction Analysis

**Prompt:**
```
Perform detailed wavefunction analysis with Multiwfn:
1. Natural population analysis
2. Bond order analysis
3. Electron localization function (ELF)
4. Identify reactive sites
```

### Step 5: Transport Properties

**Prompt:**
```
Run MD simulations for transport properties:
1. Build hydrated system (λ=20)
2. Equilibrate at 400 K
3. Production run (1 ns)
4. Calculate:
   - OH⁻ diffusion coefficient
   - Water diffusion coefficient
   - Ionic conductivity (Nernst-Einstein)
```

### Step 6: Stability Assessment

**Prompt:**
```
Assess alkaline stability based on all calculations:
1. LUMO energy and localization (QM)
2. Charge distribution (QM/Multiwfn)
3. Reactive site identification (Multiwfn)
4. Compare with stable reference compounds

Provide stability rating and confidence level.
```

### Step 7: Property Summary

**Prompt:**
```
Create a comprehensive property card for the cation:

| Property | Value | Method | Confidence |
|----------|-------|--------|------------|
| LUMO | ? eV | DFT | High |
| Conductivity | ? mS/cm | MD | Medium |
| Stability | ? | Multi-method | High |
...

Include comparison with literature benchmarks.
```

## Workflow 4: Comparative Analysis

### Objective

Compare multiple cation designs using consistent methodology.

### Step 1: Define Candidates

**Prompt:**
```
I want to compare these 4 cation types for AEM applications:
1. Piperidinium: C[N+]1(C)CCCCC1
2. Pyrrolidinium: C[N+]1(C)CCCC1
3. Imidazolium: Cn1cc[n+](C)c1
4. Morpholinium: C[N+]1(C)CCOCC1

Create a systematic comparison plan.
```

### Step 2: Consistent QM Calculations

**Prompt:**
```
For all 4 cations, run identical QM calculations:
- Method: B3LYP-D3BJ/def2-SVP
- Geometry optimization
- Frequency verification
- Property extraction

Ensure consistent settings for fair comparison.
```

### Step 3: Parallel MD Simulations

**Prompt:**
```
For all 4 cations, run comparable MD simulations:
- Same polymer backbone (PBF_BB_1)
- Same DP (15) and chain count (3)
- Same water content (λ=15)
- Same temperature (400 K)
- Same duration (500 ps)

Extract diffusion coefficients for comparison.
```

### Step 4: Comparative Analysis

**Prompt:**
```
Create a comprehensive comparison of all 4 cations:

| Property | Piperidinium | Pyrrolidinium | Imidazolium | Morpholinium |
|----------|--------------|---------------|-------------|--------------|
| LUMO (eV) | | | | |
| N charge | | | | |
| D(OH⁻) | | | | |
| σ (mS/cm) | | | | |
| Stability | | | | |

Identify the best candidate for each property and overall.
```

### Step 5: Trade-off Analysis

**Prompt:**
```
Analyze the trade-offs between the cation types:
1. Stability vs. conductivity
2. Synthesis complexity vs. performance
3. Cost vs. benefit

Create a recommendation matrix for different applications:
- High-stability applications
- High-conductivity applications
- Cost-sensitive applications
```

## Best Practices

### Workflow Design

1. **Plan ahead** - Outline all steps before starting
2. **Save checkpoints** - Note intermediate results
3. **Use consistent methods** - Same level of theory for comparisons
4. **Document everything** - Keep prompts and outputs

### Prompt Engineering

**Good multi-step prompt:**
```
I'm running a design-to-validation workflow. We've completed:
1. ✓ Literature search (piperidinium recommended)
2. ✓ HEM optimization (top candidate: CC[N+]1(CC)CCCCC1)
3. Current: QM validation

For step 3, run geometry optimization and calculate LUMO energy.
Then we'll proceed to step 4 (MD simulation).
```

**Avoid:**
```
Do everything at once - optimize, run QM, run MD, analyze.
```

### Resource Management

| Task | Typical Time | Memory |
|------|--------------|--------|
| HEM optimization | 10-20 min | 4 GB |
| QM optimization | 5-15 min | 2 GB |
| QM frequencies | 10-30 min | 4 GB |
| MD equilibration | 10-20 min | 2 GB |
| MD production | 30-60 min | 2 GB |

### Error Recovery

If a step fails:

```
Step 3 (QM calculation) failed with SCF convergence error.
Let's try:
1. Use a different initial guess
2. Increase SCF iterations
3. Try a smaller basis set first

Then continue with the workflow.
```

## Troubleshooting

### Common Multi-Step Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Lost context | Long workflow | Summarize progress periodically |
| Inconsistent results | Different methods | Use same settings throughout |
| Timeout | Long calculations | Break into smaller steps |
| Missing files | Workflow interruption | Check workspace for intermediates |

### Workflow Recovery

```
My workflow was interrupted after step 3. The QM results are in 
$QM_WORK_DIR/temp_abc123/. Resume from step 4 using those results.
```

### Debugging Complex Workflows

```
The MD simulation in my workflow gave unexpected results.
Show me:
1. The system composition
2. The simulation parameters
3. The energy profile

Let's diagnose the issue before continuing.
```

## See Also

- [HEM Optimization](./hem-optimization.md) - Design basics
- [QM Calculations](./qm-calculations.md) - QM methods
- [MD Simulations](./md-simulations.md) - MD methods
- [Literature Search](./literature-search.md) - Research integration
- [Agent Reference](../agents/index.md) - Agent capabilities

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
