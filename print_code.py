import sys
with open("src/processors/markdown.py", "r") as f:
    content = f.read()

import re

match_convert = re.search(r"def convert_markdown_to_html[\s\S]*", content)
print(match_convert.group(0))
