---
title: "Themes"
description: "Theme customization and color schemes in OHMind CLI"
category: "cli"
tags: ["cli", "themes", "colors", "customization"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: CLI Application
nav_order: 4
---

# Themes

> Scientific color themes for the OHMind CLI interface

## Table of Contents

- [Overview](#overview)
- [Available Themes](#available-themes)
- [Theme Colors](#theme-colors)
- [Agent Colors](#agent-colors)
- [Customization](#customization)
- [See Also](#see-also)

## Overview

The OHMind CLI features a modern, scientific theme system inspired by molecular visualization software and the Posting app's galaxy theme. Themes use Textual's Theme API to create cohesive color systems with automatic shade variations.

### Design Philosophy

- Dark backgrounds for reduced eye strain during long sessions
- High contrast for readability
- Agent-specific colors for visual identification
- Scientific associations (molecular orbitals, energy levels)

## Available Themes

### OHMind Scientific (Default)

The default theme with a galaxy-inspired purple palette.

```
Name: ohmind-scientific
Primary: #C45AFF (Magenta)
Background: #0F0F1F (Deep space purple-black)
Accent: #FF69B4 (Hot pink)
```

**Color Associations:**
- Primary magenta for main accents and buttons
- Deep purple background like molecular visualization software
- Hot pink for focus states and interactive elements

### OHMind Orbital

Blue/cyan focused theme inspired by molecular orbitals.

```
Name: ohmind-orbital
Primary: #4A9CFF (Blue)
Background: #0D2137 (Deep blue)
Accent: #FF79C6 (Pink)
```

**Best for:** Users who prefer cooler color temperatures.

### OHMind Synthesis

Green-focused theme with a hacker aesthetic.

```
Name: ohmind-synthesis
Primary: #00FF00 (Green)
Background: #000000 (Black)
Accent: #00FF33 (Bright green)
```

**Best for:** Users who prefer high-contrast green-on-black displays.

### OHMind Quantum

Warm sunset colors inspired by energy transitions.

```
Name: ohmind-quantum
Primary: #FF7E5F (Coral)
Background: #2B2139 (Dark purple)
Accent: #B983FF (Lavender)
```

**Best for:** Users who prefer warmer color temperatures.

## Theme Colors

### Scientific Theme Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | `#C45AFF` | Main accent, buttons, highlights |
| Secondary | `#a684e8` | Secondary elements |
| Accent | `#FF69B4` | Focus states, borders, cursors |
| Foreground | `#E8E8E8` | Text |
| Background | `#0F0F1F` | Main background |
| Surface | `#1E1E3F` | Containers, cards |
| Panel | `#2D2B55` | Elevated panels, modals |
| Boost | `#00F5D4` | Emphasis |
| Warning | `#FFD700` | Caution states |
| Error | `#FF4500` | Error states |
| Success | `#00FA9A` | Success states |

### UI Element Colors

| Element | Color | Description |
|---------|-------|-------------|
| Input cursor | `#C45AFF` | Magenta cursor |
| Footer background | `#1E1E3F` | Solid dark surface |
| Footer keys | `#C45AFF` on `#0F0F1F` | Highlighted shortcuts |
| Scrollbar | `#2D2B55` | Subtle scrollbar |
| Scrollbar hover | `#C45AFF` | Primary accent on hover |
| Border | `#3D3B65` | Subtle borders |
| Muted text | `#8080A0` | Dimmed text |

## Agent Colors

Each agent has a distinctive color for visual identification in chat responses.

| Agent | Color | Hex | Association |
|-------|-------|-----|-------------|
| Supervisor | Magenta | `#C45AFF` | Orchestration |
| HEM | Spring Green | `#00FA9A` | Molecular synthesis |
| Chemistry | Cyan | `#00F5D4` | Chemical bonds |
| QM | Gold | `#FFD700` | Energy levels |
| MD | Blue | `#4A9CFF` | Simulation |
| Multiwfn | Hot Pink | `#FF69B4` | Wavefunction |
| RAG | White | `#E8E8E8` | Knowledge |
| Web Search | Orange-Red | `#FF4500` | External resources |
| Summary | Lavender | `#a684e8` | Summarization |

### Agent Icons

| Agent | Icon | Meaning |
|-------|------|---------|
| Supervisor | 👑 | Crown for orchestration |
| HEM | 🧬 | DNA for molecular design |
| Chemistry | 🧪 | Flask for chemistry |
| QM | ⚛️ | Atom for quantum |
| MD | 💻 | Computer for simulation |
| Multiwfn | 📊 | Chart for analysis |
| RAG | 📚 | Books for literature |
| Web Search | 🌐 | Globe for web |
| Summary | 📝 | Note for summary |

## Customization

### Changing Themes

Currently, themes are set programmatically in the application. The default theme is applied on startup:

```python
# In OHMind_cli/app.py
self.theme = "ohmind-scientific"
```

### Creating Custom Themes

To create a custom theme, add a new Theme definition in `OHMind_cli/theme.py`:

```python
from textual.theme import Theme

my_custom_theme = Theme(
    name="my-custom-theme",
    primary="#YOUR_PRIMARY",
    secondary="#YOUR_SECONDARY",
    accent="#YOUR_ACCENT",
    foreground="#YOUR_FOREGROUND",
    background="#YOUR_BACKGROUND",
    surface="#YOUR_SURFACE",
    panel="#YOUR_PANEL",
    boost="#YOUR_BOOST",
    warning="#YOUR_WARNING",
    error="#YOUR_ERROR",
    success="#YOUR_SUCCESS",
    dark=True,
    variables={
        "input-cursor-background": "#YOUR_CURSOR",
        # ... additional variables
    },
)
```

Then register it in `AVAILABLE_THEMES`:

```python
AVAILABLE_THEMES = {
    "ohmind-scientific": ohmind_scientific_theme,
    "ohmind-orbital": ohmind_orbital_theme,
    "ohmind-synthesis": ohmind_synthesis_theme,
    "ohmind-quantum": ohmind_quantum_theme,
    "my-custom-theme": my_custom_theme,
}
```

### CSS Customization

Additional styling is defined in `OHMind_cli/ohmind.tcss`. This file contains:
- Widget-specific styles
- Layout rules
- Animation definitions

## Theme Variables Reference

### Input Styling

```python
"input-cursor-background": "#C45AFF",
"input-cursor-foreground": "#0F0F1F",
"input-selection-background": "#3D2B55",
```

### Footer Styling

```python
"footer-background": "#1E1E3F",
"footer-foreground": "#a684e8",
"footer-key-foreground": "#0F0F1F",
"footer-key-background": "#C45AFF",
"footer-description-foreground": "#E8E8E8",
"footer-description-background": "#1E1E3F",
```

### Scrollbar Styling

```python
"scrollbar": "#2D2B55",
"scrollbar-hover": "#C45AFF",
"scrollbar-active": "#C45AFF",
"scrollbar-background": "#1E1E3F",
```

### Border Styling

```python
"border": "#3D3B65",
"border-blurred": "#2D2B55",
```

### Text Styling

```python
"text-muted": "#8080A0",
"text-disabled": "#505070",
```

## See Also

- [CLI Overview](./index.md) - Getting started with the CLI
- [Keyboard Shortcuts](./keyboard-shortcuts.md) - Navigation shortcuts
- [Workspace Sidebar](./workspace-sidebar.md) - File browser features

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
