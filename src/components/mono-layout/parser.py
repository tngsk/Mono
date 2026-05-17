import re
from src.processors.base_parser import BaseComponentParser

class Parser(BaseComponentParser):
    # OPTIONS: label="text", class="text"
    @property
    def block_level_tags(self) -> list[str]:
        return ["mono-layout"]

    def process(self, markdown_content: str) -> str:
        # Pattern to match the innermost layout
        # (?:(?!@\[(?:hstack|vstack|row|stack)).)*? ensures we don't match across nested layouts
        LAYOUT_PATTERN = r"(?s)@\[(hstack|vstack|row|stack)(?:(?:\:\s*)?([^\]]*))\](?:\(((?:[^()]*|\([^()]*\))*)\))?((?:(?!@\[(?:hstack|vstack|row|stack)).)*?)@\[(?:end|/(?:layout|hstack|vstack|row|stack))\]"
        pattern = re.compile(LAYOUT_PATTERN, re.IGNORECASE)

        def replacer(match: re.Match) -> str:
            type_name = match.group(1).lower()
            if type_name == "row":
                type_name = "hstack"
            elif type_name == "stack":
                type_name = "vstack"

            bracket_content = match.group(2)
            args_str = match.group(3)
            inner_content = match.group(4)

            label, specific_args = self.parse_bracket_content(bracket_content)
            common_args = self.parse_key_value_args(args_str)
            args = {**specific_args, **common_args}

            classes = label.strip() if label else ""
            if 'class' in args:
                classes = args['class']

            attr = f' type="{type_name}"'
            if classes:
                attr += f' class="{classes}"'

            common_attr = self.get_common_attributes(args)
            if common_attr:
                attr += common_attr

            # Split by `:::`
            parts = re.split(r'\n?\s*:::\s*\n?', inner_content)

            items = []
            for p in parts:
                p = p.strip()
                if p:
                    items.append(f'<div class="column" markdown="1">\n{p}\n</div>')

            inner_html = "\n".join(items)

            return f'<mono-layout{attr} markdown="1">\n{inner_html}\n</mono-layout>'

        # Process from inside out
        prev_content = None
        while prev_content != markdown_content:
            prev_content = markdown_content
            markdown_content = pattern.sub(replacer, markdown_content)

        return markdown_content
