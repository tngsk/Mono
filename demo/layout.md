# Layout Component Demo

The `mono-layout` component is used to create flexbox-based layouts such as rows and stacks (columns).

## Usage
**Row Syntax:**
```markdown
@[hstack: <classes>]
...content...
@[/hstack]
```

**Stack Syntax:**
```markdown
@[vstack: <classes>]
...content...
@[/vstack]
```

**Column Layout:**
```markdown
:::
...
:::
```

## Simple Demos

### Two-Column Row
@[hstack]
:::
**Column 1**
Content for the first column.
:::
:::
**Column 2**
Content for the second column.
:::
@[/hstack]

### Stack Layout
@[vstack]
:::
**Top Section**
Content at the top.
:::
:::
**Bottom Section**
Content at the bottom.
:::
@[/vstack]

## Advanced Demos

### Complex Dashboard Layout
Combining rows, stacks, and components.

@[hstack]
:::
@[vstack]
:::
**Current Time**
@[clock]
:::
:::
**Quick Actions**
@[icon: "home"] @[icon: "settings"]
:::
@[/vstack]
:::
@[spacer: width: 20px]
:::
**Feedback**
@[poll: "How's the layout?", options: "Great, Needs Work"]
:::
@[/hstack]

### Media Gallery
Using a row to display multiple interactive media components side by side.

@[hstack]
:::
@[ab-test: "Design A vs B", src-a: test.svg, src-b: test_xml.svg]
:::
@[spacer: width: 10px]
:::
@[ab-test: "Design C vs D", src-a: test.svg, src-b: test_xml.svg]
:::
@[/hstack]

## Additional Examples
@[hstack](class: "gap-lg start")
:::
Col 1
:::
:::
Col 2
:::
@[/hstack]
