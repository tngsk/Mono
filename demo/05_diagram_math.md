# ダイアグラム・数式・特殊記法仕様検証

Mermaidダイアグラム、数式レンダラー、改行禁止構文、およびColabリンク変換の検証ドキュメント。

---

## Mermaid ダイアグラム（mono-mermaid）

@[mermaid]
flowchart LR
    MD[Markdown Source] --> Parser[Python Parser]
    Parser --> AST[Intermediate HTML]
    AST --> SingleHTML[Single-file HTML]
@[/mermaid]

- 構文: `@[mermaid] ... @[/mermaid]`
- 効果: テキスト定義からSVGベクター図をブラウザ上で動的描画。

---

## 数式レンダリング（Math Extension）

インライン数式: $E = mc^2$ および $\nabla \cdot \mathbf{B} = 0$

ブロック数式:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

- 構文: インライン `$式$`、ブロック `$$式$$`。
- 効果: LaTeX記法をMathML/HTMLベクター数式として描画。

---

## 拡張構文

1. **改行禁止（Nowrap）**:
   画面幅が縮小しても {{一続きで表示すべき専門用語や数式記号}} は折り返されずに1行を維持。

2. **Google Colab 起動リンク自動付与**:
   拡張子が `.ipynb` のリンク（例: `[notebook.ipynb](analysis.ipynb)`）を記述した場合、自動的にColab起動バッジ付きリンクへ置換。
