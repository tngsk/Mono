import markdown
from src.extensions.notes import NotesExtension


def test_notes_extraction_single_line():
    md = markdown.Markdown(extensions=[NotesExtension()])
    text = """# スライド1
<!-- ここは最初のスライドのトークスクリプトです -->
本文テキスト

---

# スライド2
<!-- note: プレフィックス付きのトークスクリプト -->
次の内容
"""
    html = md.convert(text)
    
    # HTML本文からコメントが完全に消去されていること
    assert "<!--" not in html
    assert "ここは最初のスライドのトークスクリプトです" not in html.split('<script type="application/json"')[0]
    
    # JSONスクリプトタグ内に安全に格納されていること
    assert '<script type="application/json" id="mono-speaker-notes">' in html
    assert "ここは最初のスライドのトークスクリプトです" in html
    assert "プレフィックス付きのトークスクリプト" in html
    assert "note:" not in html  # プレフィックスが除去されていること


def test_notes_extraction_multiline():
    md = markdown.Markdown(extensions=[NotesExtension()])
    text = """# 複数行テスト
<!--
1行目の説明
2行目の補足
-->
スライド本文
"""
    html = md.convert(text)
    assert '<script type="application/json" id="mono-speaker-notes">' in html
    assert "1行目の説明\\n2行目の補足" in html or "1行目の説明\n2行目の補足" in html


def test_code_block_comments_ignored():
    md = markdown.Markdown(extensions=[NotesExtension()])
    text = """# コードブロック保護
```html
<!-- これはコードブロック内のHTMLコメントなのでノートにならない -->
<div>Hello</div>
```
"""
    html = md.convert(text)
    # コードブロック内のコメントは抽出されず、ノートタグも注入されないこと
    assert "mono-speaker-notes" not in html
