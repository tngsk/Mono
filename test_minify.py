import re

def minify_css(css: str) -> str:
    # コメント削除
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # 構造文字の周りの空白削除
    css = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', css)
    # 改行とタブ削除
    css = re.sub(r'[\n\r\t]', '', css)
    # 連続する空白を1つに
    css = re.sub(r'\s+', ' ', css)
    return css.strip()

def minify_js(js: str) -> str:
    # 複数行コメント削除 (文字列内にあると壊れる可能性があるので簡易的に)
    # js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    lines = []
    for line in js.split('\n'):
        line = line.strip()
        if line and not line.startswith('//'):
            lines.append(line)
    return '\n'.join(lines)

def minify_html(html: str) -> str:
    # <!-- --> コメント削除
    html = re.sub(r'<!--(.*?)-->', '', html, flags=re.DOTALL)
    # タグ間の空白削除
    html = re.sub(r'>\s+<', '><', html)
    return html.strip()

css = """
/*
 * Base Theme
 */
:root {
    --bg-color: #fff;
    --text-color: #333; /* Default text */
}

body {
    margin: 0;
    padding: 0;
}
"""

print(minify_css(css))

js = """
// Initialize
function init() {
    /*
       Block comment
    */
    const a = 1;
    // single line
    const b = "http://example.com";
    return a + b;
}
"""
print(minify_js(js))

html = """
<div class="container">
    <!-- header -->
    <header>
        <h1>Title</h1>
    </header>
</div>
"""
print(minify_html(html))
