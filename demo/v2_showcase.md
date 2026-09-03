# Mono v2.0 公式ショーケース

Mono v2.0 正式リリースへ向けた、新次元のプレゼンテーション体験。

---

## 新たな 3×3 デザイントークン体系
{: .text-display}

Mono v2.0 では、タイポグラフィとスペーシングが完全に再設計されました。
流体設計により、あらゆる画面サイズで一貫した美しさを提供します。

@[hbox]{.gap-flow}
:::
@[vbox]{.gap-group}
:::
**3×3 タイポグラフィ**
{: .text-large}
:::
:::
- `.text-display`: 看板見出し。迫力あるプレゼンテーション向け。
- `.text-body`: 本文。読みやすさを追求。
- `.text-compact`: 補足情報。ミニマルな情報提示に。
{: .text-body}
:::
@[/vbox]
:::
:::
@[vbox]{.gap-group}
:::
**3×3 スペーシング**
{: .text-large}
:::
:::
- `.gap-flow`: セクション間の大きな余白。
- `.gap-group`: 関連する要素のまとまり。
- `.gap-item`: 個別の要素間の密接な余白。
{: .text-compact}
:::
@[/vbox]
:::
@[/hbox]

---

## ズームコンポーネントの威力
{: .text-display}

`@[zoom]` を使用して、画像や情報をシームレスに拡大・縮小できます。

@[zoom]
:::
![Mono Dashboard](https://picsum.photos/800/400)
:::
@[/zoom]

---

## リンクとインタラクション
{: .text-display}

シームレスな体験を提供する `@[link]` コンポーネント。

@[hbox]{.gap-item}
:::
@[link: "公式ドキュメント"](url: "https://example.com", icon: "book")
:::
:::
@[link: "GitHub リポジトリ"](url: "https://github.com", icon: "github")
:::
@[/hbox]

---

## Mermaid によるダイアグラム
{: .text-display}

テキストから直接、美しい図を描画。

@[mermaid]
graph TD
    A[Markdown] -->|Parser| B(HTML)
    B --> C{View}
    C -->|Browser| D[Web]
    C -->|Print| E[PDF]
@[/mermaid]

---

## セクションコンポーネント
{: .text-display}

@[section]
:::
流体タイポグラフィと 3×3 トークンが織りなす、
新しいレイアウトの可能性。
{: .text-large}

Mono v2.0 は単なるドキュメントジェネレーターではなく、
洗練されたプレゼンテーションプラットフォームです。
{: .text-body}
:::
@[/section]
