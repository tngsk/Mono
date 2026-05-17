import re
import glob

def minify_css(css: str) -> str:
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', css)
    css = re.sub(r'[\n\r\t]', '', css)
    return css.strip()

def minify_html(html: str) -> str:
    html = re.sub(r'<!--(.*?)-->', '', html, flags=re.DOTALL)
    html = re.sub(r'>\s+<', '><', html)
    html = re.sub(r'^\s+|\s+$', '', html, flags=re.MULTILINE)
    html = html.replace('\n', '')
    return html.strip()

def minify_js(js: str) -> str:
    # Remove multiline comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    lines = []
    for line in js.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('//'):
            continue
        lines.append(line)
    return '\n'.join(lines)

import os
total_orig = 0
total_min = 0

for file in glob.glob('src/components/*/*.css', recursive=True) + glob.glob('src/templates/**/*.css', recursive=True):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    total_orig += len(content)
    total_min += len(minify_css(content))

for file in glob.glob('src/components/*/*.html', recursive=True) + glob.glob('src/templates/**/*.html', recursive=True):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    total_orig += len(content)
    total_min += len(minify_html(content))

for file in glob.glob('src/components/*/*.js', recursive=True) + glob.glob('src/templates/**/*.js', recursive=True):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    total_orig += len(content)
    total_min += len(minify_js(content))

print(f"Original: {total_orig}, Minified: {total_min}, Saved: {total_orig - total_min}")
