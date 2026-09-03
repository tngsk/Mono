# 3×3 デザイントークン仕様検証

タイポグラフィおよびスペーシングの3段階トークン体系の表示検証用ドキュメント。

---

## タイポグラフィトークン
{: .text-display}

### .text-display（看板見出し）
大画面プロジェクターおよび広幅ディスプレイ向けの見出し。画面幅に応じて動的にスケーリング（`clamp(2.5rem, 1.8rem + 3.5vw, 5.5rem)`）。

### .text-body（標準本文）
通常の段落および本文テキスト。可読性を保つ流体サイズ（`clamp(1.125rem, 1rem + 0.5vw, 1.5rem)`）。
{: .text-body}

### .text-compact（凝縮テキスト）
カラム内配置、表組み、注釈向けの小型テキスト（`clamp(0.95rem, 0.85rem + 0.35vw, 1.25rem)`）。
{: .text-compact}

---

## スペーシングトークン（レイアウトギャップ）
{: .text-display}

@[hbox]{.gap-flow}
:::
**gap-flow**
セクション間の垂直リズムに準拠した最大余白（均一112px相当）。
{: .text-compact}
:::
:::
**gap-group**
関連する情報ブロック間の標準余白（約64px相当）。
{: .text-compact}
:::
:::
**gap-item**
要素間の密接な余白（約23px相当）。
{: .text-compact}
:::
@[/hbox]
