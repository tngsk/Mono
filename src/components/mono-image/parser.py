import re
from src.processors.base_parser import BaseComponentParser

class Parser(BaseComponentParser):
    # OPTIONS: url: "url", alt: "text", width: "size", height: "size"
    PATTERN = r"@\[image(?:(?:\:\s*)?([^\]]*))\](?:\(((?:[^()]*|\([^()]*\))*)\))?"
    FAST_PATH_MARKERS = ("@[image",)

    @property
    def block_level_tags(self) -> list[str]:
        return []

    def process(self, markdown_content: str) -> str:
        if "@[image" not in markdown_content:
            return markdown_content

        pattern = re.compile(self.PATTERN)

        def replacer(match: re.Match) -> str:
            bracket_content = match.group(1) or ""
            args_str = match.group(2) or ""
            label, specific_args = self.parse_bracket_content(bracket_content)
            common_args = self.parse_key_value_args(args_str)
            args = {**specific_args, **common_args}

            url, alt = self.resolve_url_and_label(label, args, ['url', 'src'], 'alt')

            width = args.get('width', '')
            height = args.get('height', '')

            style = []
            if width:
                style.append(f'width: {self.escape_html(width)};')
            if height:
                style.append(f'height: {self.escape_html(height)};')

            style_attr = f' style="{" ".join(style)}"' if style else ''

            return f'<img src="{self.escape_html(url)}" alt="{self.escape_html(alt)}"{style_attr} />'

        return pattern.sub(replacer, markdown_content)
