## 2026-05-08 - Optimized Markdown Parsing Fast Path
**Learning:** Python's `re.compile()` has an internal LRU cache, meaning micro-optimizations like moving regex compilation to class attributes offer negligible performance benefits (saving only ~1ms over 100 iterations). However, algorithmically bypassing the parsing loop entirely using a simple string `in` check (`if "@[" in content or ":::" in content:`) provides a massive performance boost (dropping processing time from ~320ms to ~27ms) when components are absent.
**Action:** When optimizing string parsing pipelines, prioritize algorithmic fast-paths that allow the application to skip expensive operations entirely, rather than attempting to micro-optimize the expensive operations themselves.

## 2026-05-16 - Optimizing Canvas Drawing Loops
**Learning:** Attaching synchronous DOM/canvas drawing methods directly to high-frequency pointer events (`mousemove`, `touchmove`) blocks the main thread, leading to visual jank and high CPU usage.
**Action:** Decouple these events by pushing coordinates to an array in the event listener, and executing the actual canvas path rendering inside a `requestAnimationFrame` loop. Always ensure that any pending points in the buffer are flushed completely on `mouseup` or `touchend` to prevent dropping the final segments of strokes.
