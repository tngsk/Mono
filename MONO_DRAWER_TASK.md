# Task: Load Material Symbols Font in `mono-drawer`

The `mono-drawer` component supports displaying a Material Symbol as its drawer handle icon (by using `class="material-symbols-outlined"` within its shadow DOM as seen in `src/components/mono-drawer/style.css`).
However, currently, the Material Symbols font is only fetched/injected into the global `document.html` when `mono-icon` is present.

**Constraints:**
Modifications to `src/processors/html.py` on behalf of individual components (like adding `or "mono-drawer" in found_mono_tags`) are strictly prohibited due to architectural guidelines.

**Goal:**
Please update the `mono-drawer` component to dynamically load the Material Symbols font correctly at the component level.
A common approach is adding an `@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined...');` rule at the top of `src/components/mono-drawer/style.css`.
