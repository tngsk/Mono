# Components & Extensions Development Guide

This document defines the core specification for developing interactive Web Components and Markdown extensions for the Mono framework (v2.0).

## 1. Extension Development Guidelines

To extend standard Python-Markdown processing, add modules to `src/extensions/`.

1. Create a new Python file in `src/extensions/` (e.g., `my_extension.py`).
2. Create a class inheriting from `markdown.extensions.Extension` and implement the `extendMarkdown` method to register processors.
3. Define a `makeExtension(**kwargs)` function at the end of the module that returns an instance of your extension.
4. Ensure it is registered in `MARKDOWN_EXTENSIONS` list in `src/constants.py`.

## 2. Component Development Architecture

Custom UI elements are built as encapsulated Web Components inside `src/components/`.

### 2.1. Directory Structure
Component directories must use kebab-case (e.g., `mono-my-component`) and include:
* `parser.py`: Python logic to parse the custom Markdown directive into an HTML tag (`<mono-my-component>`).
* `script.js`: Vanilla JS implementation extending `MonoInteractiveElement` or `MonoBaseElement`.
* `style.css`: Styles for the component's encapsulated Shadow DOM.
* `template.html`: The HTML template, wrapped in `<template id="[component-name]-template">`.
* `content.css` (Optional): Global styles scoped to the component's tag name for styling slotted Light DOM elements.

### 2.2. Design System & Design Tokens
All component styling must strictly reference design tokens defined in `themes.toml` and `base.css`:
* **Border Radii:** `var(--radius-sm, 0.125rem)`, `var(--radius-md, 0.25rem)`, `var(--radius-lg, 0.5rem)`
* **Shadows:** `var(--shadow-sm)`, `var(--shadow-md)`, `var(--shadow-lg)`
* **Colors:** `var(--color-base-content)`, `var(--color-base-100)`, `var(--color-base-200)`, `var(--color-primary)`, `var(--border-color)`
* **Spacing:** `var(--spacing-xs)`, `var(--spacing-sm)`, `var(--spacing-md)`, `var(--spacing-lg)`, `var(--spacing-xl)`

### 2.3. Print & PDF Standardization
All components must include `@media print` rules in their `style.css`:
* Apply `-webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;` to background elements.
* Hide purely interactive/transient UI controls (`display: none`) and render clean static visual fallbacks.

## 3. Markdown Directive Syntax

Components are invoked using the `@[]` syntax.

**Inline Components:**
`@[component-name: optional_label](key: "value")`

**Block-level Components:**
Use an explicit closing tag with the component name:
```markdown
@[my-component](option: "value")
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
        # Parsing logic...
        pass
```

## 4. Component Behavior & State Management

Interactive components must extend `MonoInteractiveElement` (`src/templates/core/mono-interactive-element.js`):
1. **Lifecycle (`connectedCallback`)**: Attaches Shadow DOM and initializes state.
2. **Persistent Storage**: Save data into `localStorage` using keys prefixed with `mono_`.
3. **Graceful Degradation**: Enclose storage and dynamic operations in `try...catch` blocks to ensure standalone operation in restricted environments.
4. **Touch Target Accessibility**: Interactive clickable elements must maintain a minimum bounding size of `44x44px` (`min-width: 2.75rem; min-height: 2.75rem`).
