import re
from src.processors.base_parser import BaseComponentParser

class Parser(BaseComponentParser):
    # OPTIONS: label: "text", class: "text"
    @property
    def block_level_tags(self) -> list[str]:
        return ["mono-layout"]

    def process(self, markdown_content: str) -> str:
        # Pattern to match the innermost layout (hbox / vbox as primary, hstack / vstack / row / stack as aliases)
        LAYOUT_PATTERN = r"(?s)@\[(hbox|vbox|h-box|v-box|layout-h|layout-v|hstack|vstack|row|stack)(?:(?:\:\s*)?([^\]]*))\](?:\(((?:[^()]*|\([^()]*\))*)\))?((?:(?!@\[(?:hbox|vbox|h-box|v-box|layout-h|layout-v|hstack|vstack|row|stack)).)*?)@\[(?:end|/(?:layout|hbox|vbox|h-box|v-box|layout-h|layout-v|hstack|vstack|row|stack))\]"
        pattern = re.compile(LAYOUT_PATTERN, re.IGNORECASE)

        def replacer(match: re.Match) -> str:
            raw_type = match.group(1).lower()
            if raw_type in ('hbox', 'h-box', 'layout-h', 'row', 'hstack'):
                type_name = 'hbox'
            elif raw_type in ('vbox', 'v-box', 'layout-v', 'stack', 'vstack'):
                type_name = 'vbox'
            else:
                type_name = 'hbox'
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

            # Split inner content by `:::` or `:::column`
            parts = re.split(r'\n?\s*:::(?:column)?\s*\n?', inner_content)

            items = []
            for p in parts:
                p = p.strip()
                if p:
                    items.append(f'<div class="column" markdown="1">\n{p}\n</div>')

            inner_html = "\n".join(items)

            return f'<mono-layout{attr} markdown="1">\n{inner_html}\n</mono-layout>'

        # Process from inside out with safety guard against infinite loops
        prev_content = None
        max_depth = 20
        depth = 0
        while prev_content != markdown_content and depth < max_depth:
            prev_content = markdown_content
            markdown_content = pattern.sub(replacer, markdown_content)
            depth += 1

        return markdown_content
