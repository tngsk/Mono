## 2026-05-08 - Optimized Markdown Parsing Fast Path
**Learning:** Python's `re.compile()` has an internal LRU cache, meaning micro-optimizations like moving regex compilation to class attributes offer negligible performance benefits (saving only ~1ms over 100 iterations). However, algorithmically bypassing the parsing loop entirely using a simple string `in` check (`if "@[" in content or ":::" in content:`) provides a massive performance boost (dropping processing time from ~320ms to ~27ms) when components are absent.
**Action:** When optimizing string parsing pipelines, prioritize algorithmic fast-paths that allow the application to skip expensive operations entirely, rather than attempting to micro-optimize the expensive operations themselves.

## 2026-05-16 - Optimizing Canvas Drawing Loops
**Learning:** Attaching synchronous DOM/canvas drawing methods directly to high-frequency pointer events (`mousemove`, `touchmove`) blocks the main thread, leading to visual jank and high CPU usage.
**Action:** Decouple these events by pushing coordinates to an array in the event listener, and executing the actual canvas path rendering inside a `requestAnimationFrame` loop. Always ensure that any pending points in the buffer are flushed completely on `mouseup` or `touchend` to prevent dropping the final segments of strokes.

## 2026-09-01 - Microkernel Architecture and On-Demand Asset Inlining (Zero-JS)
**Learning:** Always-including default components (like zoom, brush, sync) in single-file HTML outputs forces unnecessary template/JS bloat (30KB+) even on pure static text documents. By eliminating `always_include` and implementing on-demand tree-shaking with profile-driven presets, static documents achieve 100% Zero-JS output and drop to ~10KB file sizes.
**Action:** Keep core HTML conversion strictly minimal. Guard script tag generation so that no `<script>` or Web Component base class is injected unless interactive components are actually referenced in intermediate HTML or explicitly activated via profiles.

## 2026-09-01 - Fullscreen Fluid Typography and Container-Query Scaling
**Learning:** Hardcoded container limits (like `860px` or `80ch`) cause severe visual imbalances on large screens (1920px+ FHD and 4K displays), leaving >50% of the viewport as dead white space while text fails to fill the slide. Combining fluid CSS Grid (`min(92vw, 1750px)`), full-range fluid typography (`clamp()`), and `container-type: inline-size` with `cqi`/`vw` units allows display headings to dynamically occupy ~80% of the screen width without triggering horizontal overflow on mobile devices.
**Action:** When designing presentation-ready scroll documents, use container queries and fluid scaling formulas (`clamp(min, preferred, max)`) instead of static pixel caps, ensuring components automatically maximize screen area on projectors while preserving strict mobile constraints.

## 2026-09-02 - Non-Invasive Virtual Focus and rAF-Throttled Scroll Tracking
**Learning:** Mutating the HTML DOM structure by inserting wrapping `<section>` tags around Markdown blocks breaks parent-child CSS rules (`body > * + *`), resulting in cascading margin triple-stacking bugs (250px+ gaps) and destroying uniform flow rhythms. Keeping the DOM 100% flat and evaluating virtual slide boundaries purely in JavaScript memory via `requestAnimationFrame` maintains pristine margin architecture while enabling full ambient dimming and keyboard navigation without touching a single layout pixel.
**Action:** When implementing ambient visual focus or slide grouping on arbitrary document markup, never inject structural DOM wrapper elements. Instead, track headings/dividers in memory, apply visual classes (`.mono-ambient-dimmed`) dynamically, and throttle scroll position evaluations with `requestAnimationFrame`.

