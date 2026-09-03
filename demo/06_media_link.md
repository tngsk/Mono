# メディア・アイコン・バッジ・リンク仕様検証

インラインおよびブロック表示用の軽量UIコンポーネントの検証ドキュメント。

---

## アイコン（mono-icon）およびバッジ（mono-badge）

@[hbox]{.gap-item}
:::
@[icon: terminal](size: "24", color: "primary")
@[badge: CLI Core](type: "info")
:::
:::
@[icon: verified](size: "24", color: "success")
@[badge: Pass](type: "success")
:::
:::
@[icon: warning](size: "24", color: "warning")
@[badge: Deprecated](type: "warning")
:::
@[/hbox]

- `mono-icon`: Google Material Symbols フォントアイコンを描画。
- `mono-badge`: ステータス表示用バッジ（info, success, warning, error）。

---

## リンクカード（mono-link）

@[link: Python Packaging User Guide](url: "https://packaging.python.org", icon: "code")

- 構文: `@[link: タイトル](url: "URL", icon: "アイコン名")`
- 効果: 外部リンクをタイトル・アイコン・ドメイン表示付きのカード形式でレンダリング。

---

## 画像最適化（mono-image）

@[image: サンプル画像](src: "https://picsum.photos/600/300")

- 構文: `@[image: キャプション](src: "パスまたはURL")`
- 効果: ローカル画像の場合はBase64/WebP形式で単一HTMLに埋め込み、オフライン動作を保証。
