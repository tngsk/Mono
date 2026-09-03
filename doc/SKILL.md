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
* **テキストサイズ変更 (3段階流体スケール - Typography Trinity):** `attr_list` 拡張を使用し、指定のクラスを付与します。
  * 利用可能なクラス:
    * `.text-display` (看板): 2〜4文字の特大スライド見出し（画面幅を大胆に占有）
    * `.text-body` (主文): 標準の本文・段落スケール（24px基準）
    * `.text-compact` (凝縮): カラム内テキスト、注釈、キャプション（18〜20px基準）
  * 例:
    ```markdown
    問い
    {: .text-display}

    [標準の本文テキスト]{.text-body}
    [注釈・凝縮テキスト]{.text-compact}
    ```

* **レイアウト余白 (3段階スペーシング - Spacing Trinity):** `mono-layout`（`@[hbox]`, `@[vbox]`）の gap 指定。
  * `.gap-flow`: トップレベル均一余白（約112px）
  * `.gap-group`: カラム間・コンテナ余白（約48〜64px、デフォルト）
  * `.gap-item`: 微小余白（約16〜24px）
  * 例: `@[hbox]{.gap-group}`

---

## 2. 利用可能なコンポーネント一覧 (Available Components)

コンポーネントはライフサイクルおよび機能カテゴリに応じて明確に区分されています。

### A. コア・アクティブコンポーネント（優先利用）
Mono のモノリシック・プレゼンテーション表現の中核を担う、最新 3×3 トークンに完全適合したコンポーネントです。

| コンポーネント | 種類 | 説明 | 記法例・引数 |
|---|---|---|---|
| `mono-layout` | Block | 水平（`@[hbox]`）や垂直（`@[vbox]`）のレイアウト | `@[hbox]{.gap-group}\n::: 左\n:::\n::: 右\n:::\n@[/hbox]` |
| `mono-section` | Block | フルブリード背景・セクション区切り | `@[section](padding: "group")\n...コンテンツ...\n@[/section]` |
| `mono-zoom` | Auto/Inline | クリックまたは Z キーでの全画面モーダルズーム | `@[zoom]()` または `-p presentation` |
| `mono-code-block` | Auto | シンタックスハイライト・コピー付きコードブロック | フェンスコードブロック（```）から自動変換 |
| `mono-mermaid` | Block | Mermaid記法によるダイアグラム動的描画 | `@[mermaid]\ngraph TD; A-->B;\n@[/mermaid]` |
| `mono-theme` | Inline | カラーテーマ・フォント切り替えUI | `@[theme: corporate]()` |
| `mono-badge` | Inline | ステータスやカテゴリを示すバッジ | `@[badge: 重要](type: "error")` |
| `mono-icon` | Inline | Google Material Symbols ベクターアイコン表示 | `@[icon: star](size: "24", color: "primary")` |
| `mono-link` | Block | OGPリッチリンクカード | `@[link: タイトル](url: "https://example.com")` |
| `mono-brush` | Auto/Inline | 画面上への手書き描画（非推奨予定・プレゼン用） | `-p presentation` |
| `mono-image` | Inline/Block | Markdown画像記法 sugar syntax パーサー | `@[image: 説明](src: "img.png")` |

### B. インタラクティブ・教育系パッケージ (`@interactive`)
講義、双方向ワークショップ、データ収集用のオプトイン・コンポーネント群です。

| コンポーネント | 種類 | 説明 | 記法例・引数 |
|---|---|---|---|
| `mono-poll` | Block | リアルタイム単一・複数選択アンケート | `@[poll: 質問](options: "選択肢A, 選択肢B")` |
| `mono-reaction` | Block | 絵文字リアクションバー | `@[reaction](emojis: "👍,🎉,❤️")` |
| `mono-ab-test` | Block | A/Bテスト条件分岐提示・比較 | `@[ab-test](src-a: "a.png", src-b: "b.png")` |
| `mono-notebook` | Block | ブラウザ内メモ・ノートパッド | `@[notebook: メモ](id: "note-1")` |
| `mono-textfield-input` | Inline | 自由テキスト入力フォーム | `@[textfield-input: 氏名](id: "user-name")` |
| `mono-group-assignment` | Block | 参加者のランダムグループ分け | `@[group-assignment](groups: "4")` |
| `mono-session-join` | Block | セッション参加情報・QRコード表示 | `@[session-join](room: "101")` |
| `mono-account` | Inline | ユーザー認証およびセッション管理 | `@[account]()` |
| `mono-export` | Auto | 入力データ（localStorage）のJSONL/CSV書き出し | インタラクティブ要素存在時に自動付与 |

### C. 開発保留コンポーネント（新規スライドでの多用は非推奨）
既存の動作互換性のため維持されていますが、新規設計ではコアコンポーネントの利用を推奨します。
* `mono-clock`, `mono-countdown`, `mono-dice`, `mono-score`, `mono-sound`, `mono-synth` (ツール系)
* `mono-drawer`, `mono-hero`, `mono-media-grid` (レイアウト系保留)
* `mono-flipcard`, `mono-flow` (プレゼンテーション系保留)

## 3. AIによる生成時の禁止・遵守事項 (AI Generation Directives)

1. **削除済み・存在しない機能を使わない:** 削除された `mono-sync`, `mono-spacer` や、未実装の `@[video]`, `@[tabs]` 等は絶対に出力してはなりません。
2. **3×3 デザイントークンの遵守:** 余白には `.gap-flow`, `.gap-group`, `.gap-item` を、文字サイズには `.text-display`, `.text-body`, `.text-compact` を優先的に使用してください。
3. **フォーマットの厳守:** 引数のフォーマットは `キー: "値"` であり、`=` やシングルクォート `'` は避けてください。
4. **ブロック要素のネスト:** `@[hbox]` 内に別のブロック要素を配置する場合は、正しく `:::` 内に収め、構造を破壊しないよう気をつけてください。
5. **IDの一意性:** `mono-textfield-input` や `mono-notebook` など、`id` を要求するコンポーネントを複数配置する場合は、それぞれに一意のIDを割り当ててください。
