---
title: "Chemistry Agent"
description: "Specialized agent for molecular operations and chemistry tasks"
category: "agents"
tags: ["chemistry", "smiles", "molecular-properties", "cheminformatics"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# Chemistry Agent

> Expert agent for molecular operations, SMILES handling, and cheminformatics tasks.

## Table of Contents

- [Overview](#overview)
- [Capabilities](#capabilities)
- [Available Tools](#available-tools)
- [Example Prompts](#example-prompts)
- [Configuration](#configuration)
- [See Also](#see-also)

## Overview

The Chemistry Agent specializes in molecular informatics operations. It handles SMILES notation, molecular property calculations, functional group identification, and chemical nomenclature conversions.

### Expertise Areas

- SMILES notation and molecular representations
- Molecular similarity and structure analysis
- Functional group identification
- Chemical nomenclature (IUPAC, common names)
- Molecular properties (molecular weight, formula)
- Structure visualization

### MCP Server

The Chemistry Agent connects to the **OHMind-Chem** MCP server for tool access.

## Capabilities

| Capability | Description |
|------------|-------------|
| SMILES Validation | Check and canonicalize SMILES strings |
| Name Conversion | Convert between IUPAC names, common names, and SMILES |
| Property Calculation | Compute molecular weight, formula, atom counts |
| Similarity Analysis | Calculate Tanimoto similarity between molecules |
| Functional Groups | Identify functional groups in molecules |
| Structure Visualization | Generate 2D structure images |
| Molecule Captioning | Generate natural language descriptions |

## Available Tools

### `MoleculeWeight`

Compute exact molecular weight from a SMILES string.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: Molecular weight in g/mol

**Example**:
```python
# Input: "CC(=O)OC1=CC=CC=C1C(=O)O"
# Output: 180.16 g/mol (Aspirin)
```

### `MoleculeAtomCount`

Count atoms of each element in a molecule.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: Dictionary of element counts

### `MoleculeSimilarity`

Calculate Tanimoto similarity between two molecules.

**Parameters**:
- `smiles1` (str): First molecule SMILES
- `smiles2` (str): Second molecule SMILES

**Returns**: Similarity score (0-1) and qualitative description

### `FunctionalGroups`

Detect common functional groups from SMILES.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: List of identified functional groups (alcohol, amide, sulfonate, etc.)

### `SmilesCanonicalization`

Canonicalize a SMILES string.

**Parameters**:
- `smiles` (str): Input SMILES string
- `isomeric` (bool): Include stereochemistry information
- `atom_maps` (bool): Preserve atom mapping

**Returns**: Canonical SMILES string

### `MoleculeSmilesCheck`

Validate a molecular SMILES string and explain syntax issues.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: Validation result with error details if invalid

### `ReactionSmilesCheck`

Validate reaction SMILES (`reactants>reagents>products`).

**Parameters**:
- `reaction_smiles` (str): Reaction SMILES string

**Returns**: Validation result

### `Iupac2Smiles`

Convert IUPAC name to SMILES (via PubChem).

**Parameters**:
- `iupac_name` (str): IUPAC chemical name

**Returns**: SMILES string

### `Smiles2Iupac`

Convert SMILES to IUPAC name.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: IUPAC name

### `Smiles2Formula`

Get molecular formula from SMILES.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: Molecular formula (e.g., C9H8O4)

### `Name2Smiles`

Convert common/brand/chemical name to SMILES.

**Parameters**:
- `name` (str): Chemical name

**Returns**: SMILES string

### `Selfies2Smiles`

Convert SELFIES to SMILES.

**Parameters**:
- `selfies` (str): SELFIES string

**Returns**: SMILES string

### `Smiles2Selfies`

Convert SMILES to SELFIES.

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: SELFIES string

### `Smiles2Cas`

Look up approximate CAS number from SMILES (via PubChem).

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: CAS registry number

### `Smiles2Image`

Render a 2D structure image from SMILES.

**Parameters**:
- `smiles` (str): Input SMILES string
- `width` (int): Image width in pixels
- `height` (int): Image height in pixels

**Returns**: Path to generated image file

### `WebSearch`

Chemistry-aware web/RAG search (Tavily-backed).

**Parameters**:
- `query` (str): Search query

**Returns**: Search results with relevant chemistry information

### `MoleculeCaptioner`

Generate natural-language caption/description of a molecule (MolT5 model).

**Parameters**:
- `smiles` (str): Input SMILES string

**Returns**: Natural language description of the molecule

## Example Prompts

### Property and Functional Group Analysis

```
Using your OHMind-Chem MCP tools, analyze this molecule with SMILES 
`CC(=O)OC1=CC=CC=C1C(=O)O`.

1) Check that the SMILES is valid.
2) Report its molecular weight and formula.
3) List the functional groups and briefly explain what each group 
   typically does chemically.
```

### Name to SMILES to Image Workflow

```
With your OHMind-Chem tools, convert the IUPAC name "2-propanol" to SMILES, 
verify the SMILES is valid, and then generate a small 300×300 structure image.

Return the SMILES, a short caption describing the molecule, and a link or 
reference to the generated image file.
```

### Similarity and RAG-Assisted Design

```
Use your Chem MCP tools to compare lidocaine and procaine by SMILES.

1) Compute their structural similarity.
2) Use your web-search tool to summarize key differences in their 
   pharmacological profiles.
3) Propose a new candidate local anesthetic scaffold and justify it.
```

### Molecular Weight Calculation

```
What is the molecular weight of the compound with SMILES CN+(C)C1=CC=CC=C1?
```

### SMILES Validation

```
Check if this SMILES is valid: CC(C)(C)c1ccc(cc1)C(O)c2ccccc2
If valid, provide the canonical form.
```

## Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `TAVILY_API_KEY` | API key for web search | Required for WebSearch |
| `RDKIT_QUIET` | Suppress RDKit warnings | `1` |

### Tool Iteration

The Chemistry Agent supports iterative tool calling (up to 3 iterations) to handle complex queries that require multiple tool invocations.

### Fallback Response

If the LLM returns an empty response after tool execution, the agent generates a formatted response from the collected tool results:

```python
# Fallback formatting
if 'cal_molecular_weight' in collected_tool_results:
    result_parts.append(f"**Molecular Weight:** {mw_result}")
if 'identify_functional_groups' in collected_tool_results:
    result_parts.append(f"**Functional Groups:** {fg_result}")
```

## See Also

- [Agent Reference](./index.md) - Overview of all agents
- [Chem MCP Server](../mcp-servers/chem-server.md) - Tool documentation
- [SMILES Tutorial](../tutorials/qm-calculations.md) - Working with molecular structures

---
*Last updated: 2025-12-22 | OHMind v1.0.0*
