# Mono記法 (Mono Markdown Syntax) ガイドライン（AI向け）

このドキュメントは、AIアシスタントがMono専用の拡張Markdown記法（Mono記法）を正しく理解し、ユーザーの要請に応じて適切なMarkdownを出力するためのスキルセットとルールを定義するものです。

## 1. 基本ルールと構文 (Core Rules & Syntax)

Monoは標準のMarkdownを拡張し、専用のWeb Components（UI要素）を埋め込むための独自の `@` 構文を採用しています。AIは以下の構文規則を**厳密に守る**必要があります。

### A. インライン・コンポーネント (Inline Components)
閉じタグを必要としない単一の要素です。
* **構文:** `@[コンポーネント名: オプションのラベルテキスト](キー1: "値1", キー2: "値2"){.クラス名 #ID}`
* **括弧の役割分担:**
  * **丸括弧 `(...)`**: コンポーネント固有のデータ・機能オプション（例: `url: "..."`, `options: "..."`）
  * **波括弧 `{...}`**: CSSクラスやID（Markdown標準 `attr_list` 準拠、例: `{.error}`, `{.gap-md .center}`）
* **注意点:**
  * ラベルがない場合でも `:` は不要です： `@[image]()`
  * オプションのみの場合: `@[poll: 質問](options: "A, B")`
  * クラスのみの場合: `@[badge: 重要]{.error}`
  * 併用する場合: `@[link: タイトル](url: "https://example.com"){.large-card}`

### B. ブロックレベル・コンポーネント (Block-level Components)
内部に他のMarkdownコンテンツを含むことができる要素です。必ず対応する終了タグ `@[/コンポーネント名]` で閉じる必要があります。
* **構文:**
  ```markdown
  @[コンポーネント名](オプション1: "値1"){.クラス名}
  内部のMarkdownコンテンツ...
  @[/コンポーネント名]
  ```
* **注意:** 終了タグにはオプションを持たせないでください。

### C. レイアウト構文 (Layout Syntax: hbox, vbox)
`mono-layout` を使用して水平並び（`hbox`）や垂直並び（`vbox`）を実現します。カラムの区切りには `:::column` または `:::` を使用します。クラス指定には波括弧 `{}` または丸括弧内の `class:` が利用できます。
* **構文:**
  ```markdown
  @[hbox]{.gap-md .center}
  :::
  左側のコンテンツ
  :::
  :::
  右側のコンテンツ
  :::
  @[/hbox]
  ```

### D. テキストフォーマット・拡張機能
* **改行禁止 (Nowrap):** テキストを `{{ }}` で囲むと、その部分での改行が禁止されます。
  * 例: `これは {{絶対に改行されない}} 文字列です。`
* **テキストサイズ変更 (流体スケール):** `attr_list` 拡張を使用し、指定のクラスを付与します。
  * 利用可能なクラス:
    * `.text-display` / `.text-hero`: 2〜3文字の特大スライド見出し（画面幅の約80%を占有）
    * `.text-xlarge`: キーワード見出し
    * `.text-large`: リード文
    * `.text-small`: 注釈
  * 例:
    ```markdown
    問い
    {: .text-display}

    [大きな文字]{.text-large}
    ```

---

## 2. 利用可能なコンポーネント一覧 (Available Components)

AIは、**以下のリストに存在しないコンポーネントやパラメータを捏造（ハルシネーション）してはなりません。**

| コンポーネント | 種類 | 説明 | 引数 (OPTIONS) |
|---|---|---|---|
| `mono-ab-test` | Block | A/Bテスト用のコンポーネント。2つの画像やコンテンツを並べて比較します。 | `url-a: "url"`, `url-b: "url"`, `title: "text"` |
| `mono-account` | Inline | ログインなどのアカウント管理UIを表示します。 | なし |
| `mono-badge` | Inline | バッジを表示します。 | `text: "text"`, `type: "info&#124;success&#124;warning&#124;error"`, `color: "red&#124;blue&#124;..."` |
| `mono-clock` | Block | 時計を表示します。 | `display: "analog&#124;digital"`, `format: "24h&#124;12h"` |
| `mono-code-block` | Auto | コードブロックコンポーネント。フェンスコードブロックから自動変換されます。 | なし |
| `mono-countdown` | Block | カウントダウンタイマーを表示します。 | `minutes: "5"`, `time: "10m&#124;2024-12-31T23:59:59"`, `color: "red&#124;blue&#124;..."` |
| `mono-dice` | Block | サイコロを表示し、クリックで振ることができます。 | `sides: "6"`, `number: "1~6"` |
| `mono-drawer` | Block | 引き出し式のサイドメニュー（ドロワー）を表示します。ブロック要素。 | `label: "text"`, `position: "left&#124;right"`, `open: "true&#124;false"` |
| `mono-flipcard` | Block | クリックまたはホバーで裏返るカード。 | `front_text: "text"`, `back: "text"`, `answer: "text"` |
| `mono-flow` | Block | フローチャート（ノードとエッジ）を表示します。 | `title: "text"`, `direction: "TB&#124;LR"` |
| `mono-group-assignment` | Block | グループ分けを行うコンポーネント。 | `groups: "4"`, `title: "text"` |
| `mono-hero` | Block | ヒーローバナー領域を表示します。ブロック要素。 | `title: "text"`, `image: "url"`, `mode: "light&#124;dark"` |
| `mono-icon` | Inline | アイコンを表示します。 | `name: "star&#124;heart&#124;..."`, `size: "16~128"`, `color: "primary&#124;success&#124;..."` |
| `mono-image` | Block | 画像を表示します。 | `src: "url"`, `alt: "text"`, `width: "size"`, `height: "size"` |
| `mono-layout` | Block | 水平枠（hbox）や垂直枠（vbox）のレイアウトを構築します。ブロック要素。 | `label: "text"`, `class: "text"` |
| `mono-link` | Block | リンクカードを表示します。 | `url: "url"`, `style: "full&#124;small&#124;card"`, `description: "text"`, `image: "url"` |
| `mono-media-grid` | Block | 複数のメディアをグリッド状に配置して表示します。ブロック要素。 | `columns: "number"`, `rows: "number"`, `gap: "css-size"`, `fit: "cover&#124;contain"` |
| `mono-mermaid` | Block | Mermaid記法で図表を描画し、SVGとして埋め込みます。ブロック要素。 | `title: "text"`, `theme: "default&#124;dark&#124;forest&#124;..."` |
| `mono-notebook` | Block | 入力可能なノートブック領域を表示します。 | `title: "text"`, `placeholder: "text"`, `id: "text"` |
| `mono-poll` | Block | 投票システムを表示します。 | `title: "text"`, `options: "A,B,C"` |
| `mono-reaction` | Block | リアクション（いいね、など）ボタンを表示します。 | `emojis: "👍,🎉,❤️"`, `label: "text"` |
| `mono-score` | Inline | 楽譜を表示します。 | `notes: "C4 D4 E4"`, `clef: "treble&#124;bass"`, `time: "4/4&#124;3/4"` |
| `mono-section` | Block | セクション領域を表示します。ブロック要素。 | `title: "text"`, `image: "url"`, `mode: "light&#124;dark"`, `padding: "sm&#124;md&#124;lg"` |
| `mono-session-join` | Block | セッション（同期・データ収集）へ参加するボタン等を表示します。 | `room: "text"`, `title: "text"` |
| `mono-sound` | Inline | 効果音や音声を再生するボタンを表示します。 | `src: "url"`, `label: "text"` |
| `mono-synth` | Block | Web Audio による対話型シンセサイザー。 | `label: "text"` |
| `mono-textfield-input` | Inline | テキスト入力フィールドを表示します。 | `label: "text"`, `id: "text"`, `placeholder: "text"`, `size: "small&#124;medium&#124;large"` |
| `mono-theme` | Inline | テーマ切り替えコンポーネント。 | `theme_name: "light&#124;dark&#124;corporate&#124;calm-study"` |
| `mono-zoom` | Auto/Inline | オートズームコンポーネント（Zキーまたはクリックで拡大）。 | なし |

## 3. AIによる生成時の注意点 (AI Generation Directives)

1. **存在しない機能を作らない:** 上記リストにないコンポーネント（例: `@[video]`, `@[spacer]`, `@[tabs]`）は使えません。
2. **フォーマットの厳守:** 引数のフォーマットは `キー: "値"` であり、`=` やシングルクォート `'` は避けてください。
3. **ブロック要素のネスト:** `@[hstack]` 内に別のブロック要素を配置する場合は、正しく `:::` 内に収め、構造を破壊しないよう気をつけてください。
4. **IDの一意性:** `mono-textfield-input` や `mono-notebook` など、`id` を要求するコンポーネントを複数配置する場合は、それぞれに一意のIDを割り当ててください。
5. **プロファイルへの配慮:** プレゼンテーション用スライドを生成する場合は、大見出しに `.text-display` や `.text-xlarge` を活用し、オートズーム（`mono-zoom`）が映える視覚的構造を意識してください。
