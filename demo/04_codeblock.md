# コードブロック拡張（mono-code-block）仕様検証

フェンスコードブロックの `<mono-code-block>` 自動変換および機能検証ドキュメント。

---

## 自動変換仕様
Markdownの標準フェンス記法（```）を検出し、パーサーが自動的に `<mono-code-block>` タグを付与。

```python
import sys
from pathlib import Path

def convert(source: Path) -> str:
    """Markdownファイルを読み込み単一HTMLを返却"""
    if not source.exists():
        raise FileNotFoundError(f"Missing: {source}")
    return source.read_text(encoding="utf-8")
```

---

## 主な機能
1. **Light DOM 構造維持**: 元の `<pre><code>` を破壊せずスロットにマウントし、SEOおよびテキスト選択性を担保。
2. **コピー機能**: ヘッダー右側のボタン押下でクリップボードへコード文字列を転送。
3. **印刷対応**: `@media print` 時にコピーボタンおよびヘッダーUIを非表示化し、コード本体のみを用紙幅に合わせて出力。
