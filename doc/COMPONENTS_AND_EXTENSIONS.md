# Components & Extensions Development Guide

This document defines the core specification for developing interactive Web Components and Markdown extensions for the Mono framework.

## 1. Extension Development Guidelines

To extend the standard Python-Markdown processing, add modules to `src/extensions/`.

1.  Create a new Python file in `src/extensions/` (e.g., `my_extension.py`).
2.  Create a class inheriting from `markdown.extensions.Extension` and implement the `extendMarkdown` method to register processors.
3.  Define a `makeExtension(**kwargs)` function at the end of the module that returns an instance of your extension.
4.  Ensure it is loaded by adding it to the `MARKDOWN_EXTENSIONS` list in `src/constants.py` or loading it dynamically.

## 2. Component Development Architecture

Custom UI elements are built as Web Components inside `src/components/`.

### 2.1. Directory Structure
Component directories must use kebab-case (e.g., `mono-my-component`) and include:
*   `parser.py`: Python logic to parse the custom Markdown directive into an HTML tag.
*   `script.js`: Vanilla JS implementation (Shadow DOM or Light DOM logic).
*   `style.css`: Styles for the component's encapsulated Shadow DOM.
*   `content.css`: Global styles scoped to the component's tag name for styling slotted Light DOM elements.
*   `template.html`: The HTML template, wrapped in `<template id="[component-name]-template">`.

### 2.2. CSS Architecture Specification (Shadow vs. Light DOM)
To resolve styling conflicts between encapsulated UI and slotted Markdown content:

*   **`style.css` (Shadow DOM):** Defines styles for the component itself (`:host`) and its internal UI structure. Avoid `::slotted` for styling deeply nested children.
*   **`content.css` (Light DOM):** Defines styles for the Markdown content slotted into the component (e.g., `h1`, `p`, `pre`).
    *   **Rule:** You **MUST** scope these styles using the component's tag name as the parent selector to prevent global CSS leaks.
    *   **Good:** `mono-hero h1 { font-size: 3rem; }`
    *   **Bad:** `h1 { font-size: 3rem; }`
*   **Build Injection:** Python injects `style.css` into `{COMPONENTS_CSS}` within the component's template, while `content.css` from all used components are aggregated and injected globally into the `<head>`.

## 3. Markdown Directive Syntax

Components are invoked using the `@[]` syntax.

**Inline or Empty Components:**
`@[component-name: optional_label, key1: "value1"](style_key: "value2")`
*   `[...]`: Component-specific configuration options.
*   `(...)`: Style-related options (e.g., `class`, `padding`).

**Block-level Components:**
Use an explicit closing tag that includes the component name. Avoid ambiguous tags like `@[end]`.
```markdown
@[my-component](bg-color: "#f0f0f0")
Inner Markdown content here.
@[/my-component]
```

### Parser Implementation Example
Inherit from `BaseComponentParser` in `src/processors/base_parser.py`:

```python
import re
from src.processors.base_parser import BaseComponentParser

class Parser(BaseComponentParser):
    START_PATTERN = r"@\[my-component(?:\:\s*([^\]]*))?\](?:\(((?:[^()]*|\([^()]*\))*)\))?"
    END_PATTERN = r"@\[/my-component\]"

    @property
    def block_level_tags(self) -> list[str]:
        return ["mono-my-component"]

    def process(self, markdown_content: str) -> str:
        # Custom logic utilizing self.parse_key_value_args...
        pass
```

## 4. Component Behavior (State Machine)

Interactive components extend `MonoInteractiveElement` (or `MonoBaseElement`) for consistent lifecycle management.

1.  **Initialization (`connectedCallback`)**: Attaches to the DOM, parses attributes, and restores prior state using `this.loadState(key)`. Do not call `super.connectedCallback()` when extending `MonoBaseElement`.
2.  **Authentication (`mono-auth-changed`)**: Listens for global authentication events to enable/disable features.
3.  **Interaction**: User interaction updates the state.
4.  **Storage / Sync**: State changes are saved locally using `this.saveState(key, data)` (which handles Mono versioning) and broadcast via CustomEvents (e.g., `mono:vote` or `mono-data`) to be picked up by `mono-sync` for server transmission.

## 5. System Components vs Explicit Components

*   **Explicit Components:** Components like `mono-poll`, `mono-hero`, and `mono-layout` require explicit `@[]` syntax in the Markdown.
*   **Implicit/System Components:** Components like `mono-brush`, `mono-code-block`, `mono-sync`, and `mono-export` are automatically injected by the system based on content or flags. Note: The system injection approach for some components is planned for deprecation in favor of explicit architectural approaches.
