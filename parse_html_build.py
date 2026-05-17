import re
import sys
from pathlib import Path

# Try testing on base.css and other assets
base_css = Path("src/templates/core/base.css").read_text()
print(f"base.css original size: {len(base_css)}")

def minify_css_content(css):
    # Remove comments (multi-line)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove spaces around structural characters
    css = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', css)
    # Remove newlines, returns, tabs
    css = re.sub(r'[\n\r\t]', '', css)
    # Collapse multiple spaces
    css = re.sub(r'\s+', ' ', css)
    # Remove final semicolon in blocks
    css = re.sub(r';\}', '}', css)
    return css.strip()

print(f"base.css minified size: {len(minify_css_content(base_css))}")

base_js = Path("src/templates/core/mono-base-element.js").read_text()
print(f"mono-base-element.js original size: {len(base_js)}")

def minify_js_content(js):
    # Remove single line comments
    js = re.sub(r'//.*', '', js)
    # Remove multi line comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    # Remove new lines and tabs
    js = re.sub(r'[\n\r\t]', ' ', js)
    # Reduce multiple spaces
    js = re.sub(r'\s+', ' ', js)
    return js.strip()

print(f"mono-base-element.js minified size: {len(minify_js_content(base_js))}")
