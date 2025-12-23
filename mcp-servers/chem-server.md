---
title: "OHMind-Chem MCP Server"
description: "Chemistry MCP server for molecular informatics and web search"
category: "mcp-servers"
tags: ["chemistry", "smiles", "molecular-properties", "web-search"]
last_updated: "2025-12-23"
version: "1.0.0"
---

# OHMind-Chem MCP Server

> Comprehensive chemistry tools for molecular informatics, SMILES operations, property calculations, and chemistry-aware web search.

## Table of Contents

- [Overview](#overview)
- [Server Configuration](#server-configuration)
- [Tools Reference](#tools-reference)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The OHMind-Chem MCP server provides 17 tools for molecular informatics operations. It handles SMILES notation, molecular property calculations, name conversions, and chemistry-aware web search.

### Server Details

| Property | Value |
|----------|-------|
| Server Name | `OHMind-Chem` |
| Entry Point | `python -m OHMind_agent.MCP.Chem.server` |
| Tool Count | 17 |
| Dependencies | RDKit, Transformers, Requests |

### Capabilities

- SMILES validation and canonicalization
- Molecular property calculations
- Chemical name conversions (IUPAC, common names, CAS)
- Functional group identification
- Molecular similarity analysis
- Structure visualization
- Chemistry-aware web search

## Server Configuration

### Starting the Server

```bash
# stdio transport (default)
python -m OHMind_agent.MCP.Chem.server --transport stdio

# HTTP transport
python -m OHMind_agent.MCP.Chem.server --transport streamable-http --port 8101
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `PYTHONPATH` | Path to OHMind project | Yes |
| `TAVILY_API_KEY` | API key for web search | For WebSearch |
| `RDKIT_QUIET` | Suppress RDKit warnings | No |

### mcp.json Configuration

```json
{
  "OHMind-Chem": {
    "command": "python",
    "args": ["-m", "OHMind_agent.MCP.Chem.server", "--transport", "stdio"],
    "env": {
      "PYTHONPATH": "/path/to/OHMind",
      "TAVILY_API_KEY": "tvly-your-api-key",
      "RDKIT_QUIET": "1"
    }
  }
}
```

## Tools Reference

### SMILES Operations

#### `MoleculeSmilesCheck`

Validate a molecular SMILES string and explain syntax issues.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | SMILES string to validate |

**Returns**: Validation result with error details if invalid

**Example**:
```json
{
  "smiles": "CC(C)(C)c1ccc(cc1)C(O)c2ccccc2"
}
```

#### `SmilesCanonicalization`

Canonicalize a SMILES string to standard form.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |
| `isomeric` | boolean | No | Include stereochemistry (default: true) |
| `atom_maps` | boolean | No | Preserve atom mapping (default: false) |

**Returns**: Canonical SMILES string

#### `ReactionSmilesCheck`

Validate reaction SMILES format (`reactants>reagents>products`).

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `reaction_smiles` | string | Yes | Reaction SMILES string |

**Returns**: Validation result

### Molecular Properties

#### `MoleculeWeight`

Compute exact molecular weight from SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: Molecular weight in g/mol

**Example**:
```json
{
  "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"
}
// Returns: 180.16 g/mol (Aspirin)
```

#### `MoleculeAtomCount`

Count atoms of each element in a molecule.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: Dictionary of element counts

#### `Smiles2Formula`

Get molecular formula from SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: Molecular formula (e.g., C9H8O4)

#### `FunctionalGroups`

Detect common functional groups from SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: List of identified functional groups

**Detected Groups**:
- Alcohol, Aldehyde, Ketone
- Carboxylic acid, Ester, Amide
- Amine (primary, secondary, tertiary)
- Ether, Sulfonate, Phosphate
- Aromatic rings, Halides

#### `MoleculeSimilarity`

Calculate Tanimoto similarity between two molecules.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles1` | string | Yes | First molecule SMILES |
| `smiles2` | string | Yes | Second molecule SMILES |

**Returns**: Similarity score (0-1) and qualitative description

### Name Conversions

#### `Iupac2Smiles`

Convert IUPAC name to SMILES (via PubChem).

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `iupac_name` | string | Yes | IUPAC chemical name |

**Returns**: SMILES string

#### `Smiles2Iupac`

Convert SMILES to IUPAC name.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: IUPAC name

#### `Name2Smiles`

Convert common/brand/chemical name to SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Chemical name |

**Returns**: SMILES string

#### `Smiles2Cas`

Look up CAS number from SMILES (via PubChem).

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: CAS registry number

### Format Conversions

#### `Selfies2Smiles`

Convert SELFIES to SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `selfies` | string | Yes | SELFIES string |

**Returns**: SMILES string

#### `Smiles2Selfies`

Convert SMILES to SELFIES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: SELFIES string

### Visualization

#### `Smiles2Image`

Render a 2D structure image from SMILES.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |
| `width` | integer | No | Image width in pixels (default: 300) |
| `height` | integer | No | Image height in pixels (default: 300) |

**Returns**: Path to generated image file

### AI-Powered Tools

#### `MoleculeCaptioner`

Generate natural-language description of a molecule using MolT5 model.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `smiles` | string | Yes | Input SMILES string |

**Returns**: Natural language description

**Note**: Requires Transformers library and model download on first use.

### Web Search

#### `WebSearch`

Chemistry-aware web search using Tavily API.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | Search query |

**Returns**: Search results with relevant chemistry information

**Note**: Requires `TAVILY_API_KEY` environment variable.

## Usage Examples

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

## Troubleshooting

### Common Issues

#### RDKit Not Found

```
ImportError: No module named 'rdkit'
```

**Solution**: Install RDKit via conda:
```bash
conda install -c conda-forge rdkit
```

#### Transformers Not Found

```
ImportError: No module named 'transformers'
```

**Solution**: Install Transformers:
```bash
pip install transformers
```

#### WebSearch Fails

```
Error: TAVILY_API_KEY not set
```

**Solution**: Set the API key:
```bash
export TAVILY_API_KEY="tvly-your-api-key"
```

#### Invalid SMILES

```
Error: Could not parse SMILES
```

**Solution**: Use `MoleculeSmilesCheck` to validate SMILES before other operations.

### Debug Mode

Run the server with verbose logging:

```bash
PYTHONPATH=/path/to/OHMind \
  python -m OHMind_agent.MCP.Chem.server --transport stdio 2>&1 | tee chem_debug.log
```

## See Also

- [MCP Server Reference](./index.md) - Overview of all servers
- [Chemistry Agent](../agents/chemistry-agent.md) - Agent documentation
- [Configuration Reference](../configuration/mcp-config.md) - Full configuration

---
*Last updated: 2025-12-22 | OHMind v1.0.0*
