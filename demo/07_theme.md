# テーマ切り替えコンポーネント（mono-theme）仕様検証

`themes.toml` に定義されたCSS変数の動的切り替えUIの検証ドキュメント。

---

## セレクターの配置

@[theme: light]()

- 構文: `@[theme: デフォルトテーマ名]()`
- 効果: ドキュメント上部にテーマ選択ドロップダウンを配置。
- 動作仕様: 選択時に `<html>` 要素の `data-theme` 属性（`light`, `dark`, `corporate`, `calm-study` 等）を書き換え、全デザイントークン変数を一括更新。

---

## テーマ検証用パレット

@[hbox]{.gap-group}
:::
**Primary Color Block**
CSS変数 `--color-primary` に連動。
:::
:::
**Base Content Block**
CSS変数 `--color-base-content` および `--color-base-100` に連動。
:::
@[/hbox]
