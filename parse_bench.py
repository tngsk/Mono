import time
import re

def method1(markdown_content):
    blocks = {}
    counter = 0

    def replace_fenced(match: re.Match) -> str:
        nonlocal counter
        placeholder = f"@@FENCED_CODE_BLOCK_{counter}@@"
        blocks[placeholder] = match.group(0)
        counter += 1
        return placeholder

    # 複数行のコードブロックを保護 (``` または ~~~)
    fenced_pattern = re.compile(r'(?s)(^[ \t]*(`{3,}|~{3,}).*?\n[ \t]*\2[ \t]*(?=\n|$))', re.MULTILINE)
    processed = fenced_pattern.sub(replace_fenced, markdown_content)

    def replace_inline(match: re.Match) -> str:
        nonlocal counter
        placeholder = f"@@INLINE_CODE_BLOCK_{counter}@@"
        blocks[placeholder] = match.group(0)
        counter += 1
        return placeholder

    # インラインのコードブロックを保護
    inline_pattern = re.compile(r'(`+)(.*?)\1')
    processed = inline_pattern.sub(replace_inline, processed)

    return processed, blocks

def method2(markdown_content):
    blocks = {}
    counter = 0
    processed = markdown_content

    if "```" in processed or "~~~" in processed:
        def replace_fenced(match: re.Match) -> str:
            nonlocal counter
            placeholder = f"@@FENCED_CODE_BLOCK_{counter}@@"
            blocks[placeholder] = match.group(0)
            counter += 1
            return placeholder

        # 複数行のコードブロックを保護 (``` または ~~~)
        fenced_pattern = re.compile(r'(?s)(^[ \t]*(`{3,}|~{3,}).*?\n[ \t]*\2[ \t]*(?=\n|$))', re.MULTILINE)
        processed = fenced_pattern.sub(replace_fenced, processed)

    if "`" in processed:
        def replace_inline(match: re.Match) -> str:
            nonlocal counter
            placeholder = f"@@INLINE_CODE_BLOCK_{counter}@@"
            blocks[placeholder] = match.group(0)
            counter += 1
            return placeholder

        # インラインのコードブロックを保護
        inline_pattern = re.compile(r'(`+)(.*?)\1')
        processed = inline_pattern.sub(replace_inline, processed)

    return processed, blocks

content = "This is a simple document without any code blocks! " * 1000

start = time.perf_counter()
for _ in range(100):
    method1(content)
print(f"protect1: {time.perf_counter() - start:.4f}s")

start = time.perf_counter()
for _ in range(100):
    method2(content)
print(f"protect2: {time.perf_counter() - start:.4f}s")
