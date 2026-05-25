import re


class MarkdownComponentParser:
    """
    Template for parsing custom Markdown syntax into HTML components.
    Inspired by Mono's custom syntax parser (e.g. @[badge: label](color: "red"))
    """

    def __init__(self):
        # Example: @[badge: User](color: "primary")
        # Group 1: Label (" User")
        # Group 2: Arguments ('color: "primary"')
        self.pattern = (
            r"@\[badge(?:(?:\:\s*)?([^\]]*))\](?:\(((?:[^()]*|\([^()]*\))*)\))?"
        )

        # Output HTML template
        self.template = "<my-badge{color_attr}>{text}</my-badge>"

    def parse_key_value_args(self, args_str: str) -> dict:
        """
        Simplified parser for extracting key-value pairs (e.g., color: "primary")
        from the arguments string.
        """
        if not args_str:
            return {}

        result = {}
        # Simple split by comma (does not handle nested commas or quotes well for simplicity in template)
        parts = args_str.split(",")
        for part in parts:
            if ":" in part:
                k, v = part.split(":", 1)
                k = k.strip()
                v = v.strip()
                # Remove surrounding quotes if they exist
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                result[k] = v
        return result

    def process(self, markdown_content: str) -> str:
        """
        Finds all custom tags in the markdown and replaces them with HTML.
        """
        regex = re.compile(self.pattern)

        def replacer(match: re.Match) -> str:
            # Extract bracket content (label/text)
            bracket_content = match.group(1) or ""
            text = bracket_content.strip()

            # Extract arguments
            args_str = match.group(2)
            args = self.parse_key_value_args(args_str)

            # Build HTML attributes
            color_attr = ""
            if "color" in args:
                # Basic escaping
                safe_color = args["color"].replace('"', "&quot;")
                color_attr = f' color="{safe_color}"'

            return self.template.format(
                text=text.replace("<", "&lt;").replace(
                    ">", "&gt;"
                ),  # Basic HTML escape
                color_attr=color_attr,
            )

        return regex.sub(replacer, markdown_content)


# === Example Usage ===
if __name__ == "__main__":
    parser = MarkdownComponentParser()

    sample_markdown = """
# Hello World
Here is a normal text, and here is a @[badge: New Feature](color: "success")!
You can also use defaults like this: @[badge]
    """

    result = parser.process(sample_markdown)
    print("--- Original Markdown ---")
    print(sample_markdown.strip())
    print("\n--- Parsed HTML ---")
    print(result.strip())
