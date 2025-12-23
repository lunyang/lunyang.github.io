---
title: "Keyboard Shortcuts"
description: "Complete keyboard shortcut reference for OHMind CLI"
category: "cli"
tags: ["cli", "keyboard", "shortcuts", "reference"]
last_updated: "2025-12-23"
version: "1.0.0"
parent: CLI Application
nav_order: 2
---

# Keyboard Shortcuts

> Complete reference for all keyboard shortcuts in the OHMind CLI

## Table of Contents

- [Overview](#overview)
- [Primary Shortcuts](#primary-shortcuts)
- [Navigation Shortcuts](#navigation-shortcuts)
- [Input Shortcuts](#input-shortcuts)
- [Shortcut Categories](#shortcut-categories)
- [See Also](#see-also)

## Overview

The OHMind CLI provides keyboard shortcuts for efficient navigation and control. Shortcuts are displayed in the footer bar at the bottom of the interface.

All shortcuts use standard modifier keys:
- `Ctrl` - Control key (primary modifier)
- `F1-F12` - Function keys

## Primary Shortcuts

These shortcuts are always visible in the footer and provide core functionality.

### `Ctrl+C` - Quit

Exit the application with a confirmation dialog.

- Shows confirmation screen before exiting
- Prevents accidental closure
- Cleans up MCP sessions on exit

### `Ctrl+L` - Clear

Clear the current conversation.

- Removes all messages from chat view
- Generates new thread ID
- Resets conversation state
- Shows welcome message

### `Ctrl+B` - Toggle Sidebar

Show or hide the workspace sidebar.

- Toggles sidebar visibility
- Chat view expands when sidebar hidden
- Preserves sidebar width setting
- Also hides/shows the splitter

### `Ctrl+E` - Export

Open the export dialog.

- Choose export format (Markdown, HTML, Screenshot)
- Exports to current directory
- Timestamped filenames

### `F1` - Help

Display the help screen.

- Shows available commands
- Lists keyboard shortcuts
- Displays agent information

## Navigation Shortcuts

### `Ctrl+T` - Tools

Display available MCP tools.

- Shows tools organized by server
- Lists tool names and counts
- Requires MCP servers to be connected

### `Ctrl+A` - Agents

Display available agents.

- Shows all specialized agents
- Displays agent icons and names
- Color-coded by agent type

### `Ctrl+R` - Refresh Tree

Refresh the workspace directory tree.

- Reloads file listing
- Shows newly generated files
- Updates file tree display
- Hidden from footer (power user feature)

## Input Shortcuts

Standard text input shortcuts work in the input field:

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Ctrl+A` | Select all text |
| `Ctrl+C` | Copy selected text |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+X` | Cut selected text |
| `Backspace` | Delete character before cursor |
| `Delete` | Delete character after cursor |
| `Home` | Move to start of line |
| `End` | Move to end of line |
| `←` `→` | Move cursor left/right |

## Shortcut Categories

### Application Control

| Shortcut | Action | Visible |
|----------|--------|---------|
| `Ctrl+C` | Quit application | Yes |
| `Ctrl+L` | Clear conversation | Yes |
| `F1` | Show help | Yes |

### View Control

| Shortcut | Action | Visible |
|----------|--------|---------|
| `Ctrl+B` | Toggle sidebar | Yes |
| `Ctrl+R` | Refresh file tree | No |

### Information

| Shortcut | Action | Visible |
|----------|--------|---------|
| `Ctrl+T` | Show tools | Yes |
| `Ctrl+A` | Show agents | Yes |

### Export

| Shortcut | Action | Visible |
|----------|--------|---------|
| `Ctrl+E` | Export dialog | Yes |

## Shortcut Quick Reference Card

```
┌─────────────────────────────────────────────┐
│           OHMind CLI Shortcuts              │
├─────────────────────────────────────────────┤
│  Ctrl+C    Quit (with confirmation)         │
│  Ctrl+L    Clear conversation               │
│  Ctrl+B    Toggle sidebar                   │
│  Ctrl+E    Export chat history              │
│  Ctrl+T    Show MCP tools                   │
│  Ctrl+A    Show agents                      │
│  Ctrl+R    Refresh file tree                │
│  F1        Show help screen                 │
├─────────────────────────────────────────────┤
│  Enter     Send message                     │
│  /help     Show commands                    │
│  /quit     Exit application                 │
└─────────────────────────────────────────────┘
```

## Tips

### Efficient Workflow

1. Use `Ctrl+B` to maximize chat space when not browsing files
2. Use `Ctrl+R` after agent generates files to see them immediately
3. Use `Ctrl+E` to save important conversations

### Keyboard-Only Navigation

The CLI is designed for keyboard-driven interaction:
- Tab through focusable elements
- Enter to activate buttons
- Escape to close dialogs
- Arrow keys for scrolling

### Customization

Keyboard shortcuts are defined in the application bindings and cannot be customized without modifying the source code. The bindings are defined in `OHMind_cli/app.py`:

```python
BINDINGS = [
    Binding("ctrl+c", "quit", "Quit", show=True),
    Binding("ctrl+l", "clear", "Clear", show=True),
    Binding("ctrl+b", "toggle_sidebar", "Files", show=True),
    Binding("ctrl+r", "refresh_tree", "Refresh", show=False),
    Binding("ctrl+t", "show_tools", "Tools", show=True),
    Binding("ctrl+a", "show_agents", "Agents", show=True),
    Binding("ctrl+e", "export", "Export", show=True),
    Binding("f1", "show_help", "Help", show=True),
]
```

## See Also

- [CLI Overview](./index.md) - Getting started with the CLI
- [Commands Reference](./commands.md) - Slash command documentation
- [Workspace Sidebar](./workspace-sidebar.md) - File browser features

---

*Last updated: 2025-12-23 | OHMind v1.0.0*
