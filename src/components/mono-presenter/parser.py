import re
from src.processors.base_parser import BaseComponentParser


class Parser(BaseComponentParser):
    """@[presenter]() ディレクティブを <mono-presenter> タグに変換するパーサー"""
    PATTERN = r"@\[(?:presenter)\](?:\(((?:[^()]*|\([^()]*\))*)\))?"

    def process(self, markdown_content: str) -> str:
        def replace(match):
            return "<mono-presenter></mono-presenter>"

        return re.sub(self.PATTERN, replace, markdown_content)

    def parse(self, text: str) -> str:
        return self.process(text)
