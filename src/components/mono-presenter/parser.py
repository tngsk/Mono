import re
from src.processors.base_parser import BaseComponentParser


class Parser(BaseComponentParser):
    """@[presenter]() ディレクティブを <mono-presenter> タグに変換するパーサー"""
    PATTERN = r"@\[(?:presenter)\](?:\(((?:[^()]*|\([^()]*\))*)\))?"

    def parse(self, text: str) -> str:
        def replace(match):
            return "<mono-presenter></mono-presenter>"

        return re.sub(self.PATTERN, replace, text)
