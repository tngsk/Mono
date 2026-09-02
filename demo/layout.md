# Layout Component Demo (hbox / vbox)

The `mono-layout` component creates flexbox-based layouts: horizontal rows (`@[hbox]`) and vertical stacks (`@[vbox]`).

## Usage

**Horizontal Box (`@[hbox]`):**
```markdown
@[hbox](class: "gap-md")
:::
Left column content...
:::
:::
Right column content...
:::
@[/hbox]
```

**Vertical Box (`@[vbox]`):**
```markdown
@[vbox](class: "center")
:::
Top section...
:::
:::
Bottom section...
:::
@[/vbox]
```

## Simple Demos

### Two-Column Horizontal Box
@[hbox](class: "gap-md")
:::
**Column 1**
Content for the first column with modern spacing.
:::
:::
**Column 2**
Content for the second column with equal flex distribution.
:::
@[/hbox]

### Vertical Box Layout
@[vbox](class: "gap-sm")
:::
**Top Section**
Content at the top.
:::
:::
**Bottom Section**
Content at the bottom.
:::
@[/vbox]

## Advanced Demos

### Dashboard Layout with Nested Boxes
@[hbox](class: "gap-md")
:::
@[vbox](class: "gap-sm")
:::
**Current Time**
@[clock]
:::
:::
**Quick Actions**
@[icon: "star"](size: "24", color: "primary")
:::
@[/vbox]
:::
:::
**Feedback**
@[poll: "How's the layout?", options: "Great, Clean, Modern"]
:::
@[/hbox]

## Modifiers
@[hbox](class: "gap-lg start")
:::
Column A (Left Aligned)
:::
:::
Column B (Left Aligned)
:::
@[/hbox]
