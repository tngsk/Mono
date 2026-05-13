import re
from src.processors.base_parser import BaseComponentParser

class Parser(BaseComponentParser):
    FAST_PATH_MARKERS = ("@[media-grid",)
    # OPTIONS: columns="number", rows="number", gap="css-size", fit="cover|contain"
    PATTERN = r"@\[media-grid(?:(?:\:\s*)?([^\]]*))\](?:\(((?:[^()]*|\([^()]*\))*)\))?"
    END_PATTERN = r"@\[(?:/media-grid)\]"

    @property
    def block_level_tags(self) -> list[str]:
        return ["mono-media-grid"]

    def process(self, markdown_content: str) -> str:
        # start tag
        pattern = re.compile(self.PATTERN)
        def replacer(match: re.Match) -> str:
            bracket_content = match.group(1) or ""
            args_str = match.group(2) or ""
            label, specific_args = self.parse_bracket_content(bracket_content)
            common_args = self.parse_key_value_args(args_str)
            args = {**specific_args, **common_args}

            attrs = self.get_common_attributes(args)
            if 'columns' in args:
                attrs += f' columns="{self.escape_html(args["columns"])}"'
            if 'rows' in args:
                attrs += f' rows="{self.escape_html(args["rows"])}"'
            if 'gap' in args:
                attrs += f' gap="{self.escape_html(args["gap"])}"'
            if 'fit' in args:
                attrs += f' fit="{self.escape_html(args["fit"])}"'

            return f'<mono-media-grid markdown="1"{attrs}>'

        result = pattern.sub(replacer, markdown_content)

        # end tag
        end_pattern = re.compile(self.END_PATTERN)
        result = end_pattern.sub('</mono-media-grid>', result)

        return result
