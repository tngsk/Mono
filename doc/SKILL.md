# Mono記法 (Mono Markdown Syntax) ガイドライン（AI向け）

このドキュメントは、AIアシスタントがMono専用の拡張Markdown記法（Mono記法）を正しく理解し、ユーザーの要請に応じて適切なMarkdownを出力するためのスキルセットとルールを定義するものです。

## 1. 基本ルールと構文 (Core Rules & Syntax)

Monoは標準のMarkdownを拡張し、専用のWeb Components（UI要素）を埋め込むための独自の `@` 構文を採用しています。AIは以下の構文規則を**厳密に守る**必要があります。

### A. インライン・コンポーネント (Inline Components)
閉じタグを必要としない単一の要素です。
* **構文:** `@[コンポーネント名: オプションのラベルテキスト](キー1: "値1", キー2: "値2")`
* **注意点:**
  * ラベルがない場合でも `:` は不要です： `@[image]()`
  * パラメータはカッコ `()` 内にカンマ区切りで記述します。
  * **重要:** 属性の指定には `=` ではなく `:` を使用し、値は原則としてダブルクォーテーション `"` で囲む必要はありません（例： `color: red` や `class: bg-secondary text-large`）。ただし、**値の中にカンマ（`,`）が含まれる場合**（例： `title: "Hello, World"`, JSON, 配列など）は**必ずダブルクォーテーションで囲む**必要があります。

### B. ブロックレベル・コンポーネント (Block-level Components)
内部に他のMarkdownコンテンツを含むことができる要素です。必ず対応する終了タグ `@[/コンポーネント名]` で閉じる必要があります。
* **構文:**
  ```markdown
  @[コンポーネント名](キー1: "値1")
  内部のMarkdownコンテンツ...
  @[/コンポーネント名]
  ```
* **注意:** 終了タグにはオプションを持たせないでください。

### C. レイアウト構文 (Layout Syntax: row, stack)
`mono-layout` を使用して横並び（`row`）や縦積み（`stack`）を実現します。カラムの区切りには `:::column` を使用し、最後は `:::` で閉じます。
* **構文:**
  ```markdown
  @[row](class: "gap-md center")
  :::column
  左側のコンテンツ
  :::
  :::column
  右側のコンテンツ
  :::
  @[/row]
  ```

### D. テキストフォーマット・拡張機能
* **改行禁止 (Nowrap):** テキストを `{{ }}` で囲むと、その部分での改行が禁止されます。
  * 例: `これは {{絶対に改行されない}} 文字列です。`
* **テキストサイズ変更:** `attr_list` 拡張を使用し、指定のクラスを付与します。
  * 利用可能なクラス: `.text-small` (0.5rem), `.text-large` (1.5rem), `.text-xlarge` (3rem)
  * 例: `[大きな文字]{.text-large}`

---

## 2. 利用可能なコンポーネント一覧 (Available Components)

AIは、**以下のリストに存在しないコンポーネントやパラメータを捏造（ハルシネーション）してはなりません。**

| コンポーネント | 種類 | 説明 | 引数 (OPTIONS) |
|---|---|---|---|
| `mono-ab-test` | Block | A/Bテスト（比較） | `src-a="url"`, `src-b="url"`, `title="text"` |
| `mono-account` | Inline | アカウント管理UI | なし |
| `mono-badge` | Inline | バッジ | ラベルテキスト, `color="red|blue|..."`, `soft="true|false"`, `outline="true|false"` |
| `mono-clock` | Inline | 時計 | `display="analog|digital"`, `format="24h|12h"` |
| `mono-countdown`| Inline | カウントダウン | `time="10m|2024-12-31T23:59:59"`, `color="red|blue|..."` |
| `mono-dice` | Inline | サイコロ | `number="1~6"`, `faces="4|6|8|10|12|20"` |
| `mono-drawer` | Block | ドロワー（サイドメニュー）| `label="text"`, `position="left|right"`, `open="true|false"` |
| `mono-flipcard` | Inline | フリップカード | ラベルテキスト(front_text), `answer="text"` |
| `mono-flow` | Block | フローチャート（ノードは `A -> B` のように記述） | ラベルテキスト(title), `direction="TB|LR"` |
| `mono-group-assignment` | Inline | グループ分け | `title="text"` |
| `mono-hero` | Block | ヒーローバナー | `title="text"`, `image="url"`, `mode="light|dark"`, `bg-color="#HEX"`, `text-color="#HEX"` |
| `mono-icon` | Inline | アイコン | ラベルテキスト(name), `size="16~128"`, `color="red|#HEX"`, `display="inline|block"` |
| `mono-image` | Inline | 画像 | `src="url"`, `alt="text"`, `width="size"`, `height="size"` |
| `mono-layout` | Block | レイアウト (`@[row]`, `@[stack]`) | ラベルテキスト(class), `class="text"` |
| `mono-link` | Inline | リンクカード | `url="url"`, `style="full|small|card"` |
| `mono-media-grid` | Block | メディアグリッド | `label="text"`, `columns="number"`, `rows="number"`, `gap="css-size"`, `fit="cover|contain"` |
| `mono-mermaid` | Block | Mermaid図表 | `title="text"`, `theme="default|dark|forest|..."` |
| `mono-notebook` | Inline | ノートブック入力領域 | `title="text"`, `placeholder="text"`, `id="text"` |
| `mono-poll` | Inline | 投票 | `title="text"`, `options="A,B,C"` |
| `mono-reaction` | Inline | リアクション（いいね等）| `label="text"`, `options="👍,👎"` |
| `mono-score` | Inline | 楽譜 (VexFlow) | `notes="C4 D4 E4"`, `clef="treble|bass"`, `time="4/4|3/4"`, `voices='["C4 D4", "E4 F4"]'` |
| `mono-section` | Block | セクション領域 | `title="text"`, `image="url"`, `mode="light|dark"`, `bg-color="#HEX"`, `text-color="#HEX"`, `height="px|vh"`, `width="px|vw"` |
| `mono-session-join` | Inline | セッション参加ボタン | `title="text"` |
| `mono-sound` | Inline | 音声再生ボタン | `label="text"`, `src="url"` |
| `mono-spacer` | Inline | スペーサー（空白） | `width="px|rem"`, `height="px|rem"` |
| `mono-synth` | Inline | シンセサイザー | `sample="url"`, `label="text"` |
| `mono-textfield-input` | Inline | テキスト入力 | `label="text"`, `id="text"`, `placeholder="text"`, `size="small|medium|large"` |
| `mono-theme` | Inline | テーマ設定・切り替え | ラベルテキスト(theme_name), `show_ui="true|false"`, `config="json"` |

## 3. AIによる生成時の注意点 (AI Generation Directives)

1. **存在しない機能を作らない:** 上記リストにないコンポーネント（例: `@[video]`, `@[tabs]`）は使えません。
2. **フォーマットの厳守:** 引数のフォーマットは `キー: "値"` であり、`=` やシングルクォート `'` は避けてください。
3. **ブロック要素のネスト:** `@[row]` 内に別のブロック要素を配置する場合は、正しく `:::column` 内に収め、構造を破壊しないよう気をつけてください。
4. **IDの一意性:** `mono-textfield-input` や `mono-notebook` など、`id` を要求するコンポーネントを複数配置する場合は、それぞれに一意のIDを割り当ててください。
