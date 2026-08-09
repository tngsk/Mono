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
  * **重要:** 属性の指定には `=` ではなくコロンとスペース `キー: "値"` の構文を使用します。ダブルクォーテーション `"` で囲むことが推奨されますが、値にカンマが含まれない場合は省略可能です。`=` を区切り文字として使用することは非推奨（警告ログが出力されます）ですが、既存の構文を壊さないために `ValueError` にはなりません。値の中にカンマが含まれる場合（JSONや配列など）は必ずダブルクォーテーションで囲んでください。

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
`mono-layout` を使用して横並び（`row`）や縦積み（`stack`）を実現します。マークダウンタグの `@[row]` と `@[stack]` はシンタックスエイリアスとして機能し、Web Componentの `type="hstack"` および `type="vstack"` 属性にそれぞれマッピングされて既存の内部Flexbox CSSを再利用します。カラムの区切りには `:::column` を使用し、最後は `:::` で閉じます。
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
| `mono-ab-test` | Block | A/Bテスト用のコンポーネント。2つの画像やコンテンツを並べて比較します。 | `url-a: "url"`, `url-b: "url"`, `title: "text"` |
| `mono-account` | Block | ログインなどのアカウント管理UIを表示します。 | なし |
| `mono-badge` | Inline | バッジを表示します。 | `text: "text"`, `color: "red&#124;blue&#124;..."`, `soft: "true&#124;false"`, `outline: "true&#124;false"` |
| `mono-brush` | Implicit/System | 描画オーバーレイ機能。暗黙的に全ページに組み込まれるか、特定条件で有効化されます。 | なし |
| `mono-clock` | Block | 時計を表示します。 | `display: "analog&#124;digital"`, `format: "24h&#124;12h"` |
| `mono-code-block` | Implicit/System | コードブロックコンポーネント。コードブロックが存在する場合に暗黙的に組み込まれます。 | なし |
| `mono-countdown` | Block | カウントダウンタイマーを表示します。 | `time: "10m&#124;2024-12-31T23:59:59"`, `color: "red&#124;blue&#124;..."` |
| `mono-dice` | Block | サイコロを表示し、クリックで振ることができます。 | `number: "1~6"`, `faces: "4&#124;6&#124;8&#124;10&#124;12&#124;20"` |
| `mono-drawer` | Block | 引き出し式のサイドメニュー（ドロワー）を表示します。ブロック要素。 | `label: "text"`, `position: "left&#124;right"`, `open: "true&#124;false"` |
| `mono-export` | Implicit/System | 外部エクスポート機能。`--export`オプションで強制的に有効になります。 | なし |
| `mono-flipcard` | Block | クリックまたはホバーで裏返るカード。 | `front_text: "text"`, `answer: "text"` |
| `mono-flow` | Block | フローチャート（ノードとエッジ）を表示します。 | `title: "text"`, `direction: "TB&#124;LR"` |
| `mono-group-assignment` | Block | グループ分けを行うコンポーネント。 | `title: "text"` |
| `mono-hero` | Block | ヒーローバナー領域を表示します。ブロック要素。 | `title: "text"`, `image: "url"`, `mode: "light&#124;dark"`, `bg-color: "#HEX"`, `text-color: "#HEX"` |
| `mono-icon` | Inline | アイコンを表示します。 | `name: "star&#124;heart&#124;..."`, `size: "16~128"`, `color: "red&#124;#HEX"`, `display: "inline&#124;block"` |
| `mono-image` | Block | 画像を表示します。 | `url: "url"`, `alt: "text"`, `width: "size"`, `height: "size"` |
| `mono-layout` | Block | 横並び（hstack）や縦並び（vstack）のレイアウトを構築します。ブロック要素。 | `label: "text"`, `class: "text"` |
| `mono-link` | Block | リンクカードを表示します。 | `url: "url"`, `style: "full&#124;small&#124;card"` |
| `mono-media-grid` | Block | 複数のメディアをグリッド状に配置して表示します。ブロック要素。 | `label: "text"`, `columns: "number"`, `rows: "number"`, `gap: "css-size"`, `fit: "cover&#124;contain"` |
| `mono-mermaid` | Block | Mermaid記法で図表を描画し、SVGとして埋め込みます。ブロック要素。 | `title: "text"`, `theme: "default&#124;dark&#124;forest&#124;..."` |
| `mono-notebook` | Block | 入力可能なノートブック領域を表示します。 | `title: "text"`, `placeholder: "text"`, `id: "text"` |
| `mono-poll` | Block | 投票システムを表示します。 | `title: "text"`, `options: "A,B,C"` |
| `mono-reaction` | Block | リアクション（いいね、など）ボタンを表示します。 | `label: "text"`, `options: "👍,👎"` |
| `mono-score` | Inline | 楽譜を表示します。 | `notes: "C4 D4 E4"`, `clef: "treble&#124;bass"`, `time: "4/4&#124;3/4"`, `voices: '["C4 D4", "E4 F4"]'` |
| `mono-section` | Block | セクション領域を表示します。ブロック要素。 | `title: "text"`, `image: "url"`, `mode: "light&#124;dark"`, `bg-color: "#HEX"`, `text-color: "#HEX"`, `height: "px&#124;vh"`, `width: "px&#124;vw"` |
| `mono-session-join` | Block | セッション（同期・データ収集）へ参加するボタン等を表示します。 | `title: "text"` |
| `mono-sound` | Block | 効果音や音声を再生するボタンを表示します。 | `url: "url"`, `label: "text"` |
| `mono-spacer` | Block | 空白（スペーサー）を挿入します。 | `width: "px&#124;rem"`, `height: "px&#124;rem"` |
| `mono-sync` | Implicit/System | 状態同期・通信機能。サーバーとのSSE/HTTP通信を管理し、暗黙的に組み込まれます。 | なし |
| `mono-synth` | Block | Tone.jsを用いたシンプルなシンセサイザー。OSC, Filter, ADSR, ミニ鍵盤を備えます。 | `url: "url"`, `label: "text"` |
| `mono-textfield-input` | Inline | テキスト入力フィールドを表示します。 | `label: "text"`, `id: "text"`, `placeholder: "text"`, `size: "small&#124;medium&#124;large"` |
| `mono-theme` | Block | テーマ切り替えコンポーネント。通常はMarkdownディレクティブでテーマを設定します。 | `theme_name: "light&#124;dark"`, `show_ui: "true&#124;false"`, `config: "json"`, `font_size: "16px"` |


## 3. AIによる生成時の注意点 (AI Generation Directives)

1. **存在しない機能を作らない:** 上記リストにないコンポーネント（例: `@[video]`, `@[tabs]`）は使えません。
2. **フォーマットの厳守:** 引数のフォーマットは `キー: "値"` であり、`=` やシングルクォート `'` は避けてください。
3. **ブロック要素のネスト:** `@[row]` 内に別のブロック要素を配置する場合は、正しく `:::column` 内に収め、構造を破壊しないよう気をつけてください。
4. **IDの一意性:** `mono-textfield-input` や `mono-notebook` など、`id` を要求するコンポーネントを複数配置する場合は、それぞれに一意のIDを割り当ててください。

## 4. AIへの追加指示・アドバイス (Additional Directives & Advice)

ユーザーが「コンポーネントの変換結果を変更したい」と要求してきた場合や、機能追加を検討する際には以下の点に注意してアドバイスを行ってください：

1. **Pythonによるパースの仕組み (Parser Logic)**
   * 各コンポーネントは `src/components/コンポーネント名/parser.py` というファイルで処理されます。
   * Markdown中の `@[コンポーネント名]` という記述を `re.sub` などの正規表現で検索し、Web Component用のカスタムHTMLタグ（例: `<mono-badge>`）に置換するのが基本的な流れです。
   * インライン要素は `PATTERN` を用いてパースされます。ブロック要素は `END_PATTERN` の存在、または `end|` トークンにマッチするか、`block_level_tags` プロパティを持つことで識別されます。これらを持たないコンポーネントはインライン要素と見なされます。
   * **高速化 (Fast Path):** Markdownのパース処理を高速化するため、各コンポーネントパーサーは `FAST_PATH_MARKERS = ("@[image",)` などのクラス属性を定義します。このマーカーがMarkdown文字列内に存在しない場合、重い正規表現の評価をスキップします。

2. **フロントエンドの実装 (Web Components Logic)**
   * 置換されたHTMLタグは、ブラウザ側で `src/components/コンポーネント名/script.js` (Web Components実装) や `style.css` (スタイリング)、`template.html` (HTML構造) によって具体的なUIとしてレンダリングされます。※以前は`index.js`でしたが、現在は`script.js`と`template.html`に分離されていることが多いです。
   * **自動ディスカバリ:** 新しく作成した Web Component をプロジェクトに追加する場合、`ComponentRegistry` による自動ディスカバリが行われます。各コンポーネントのディレクトリ（例: `src/components/<component_name>/manifest.json`）に `manifest.json` を作成し、`interactive`, `always_include`, `requires_icons` などのブール型プロパティを定義してケーパビリティを登録する必要があります。
   * デザインやUIの挙動を変えたい場合は、Pythonの `parser.py` を変更するのではなく、Web Componentsの実装である `script.js`、`template.html` や `style.css` の変更を検討してください。
   * **重要:** UIやインタラクションの変更を行った際は、自動テストだけでなく Playwright 等を用いたスクリーンショットによる**視覚的な検証（Visual Verification）**を必ず実施してください。

3. **新しいオプションの追加 (Adding New Options)**
   * ユーザーが新しいオプションを追加したい場合は、以下の対応が必要です：
     1. `parser.py` の `# OPTIONS:` コメントに追加する。ここで記述した内容はドキュメント生成やエディタスニペット生成に使用されるため、**必ずコロンを用いたキー・バリュー形式（例: `image: "url", mode: "light|dark"`）で正確に記述**してください（`=`は使用不可）。コンポーネントがオプションを受け付けない場合は、`# OPTIONS:` の後に何も書かないか空にすることで、ドキュメントに「オプションなし」として正しく反映されます。
     2. `parser.py` 内で、属性をHTMLタグのプロパティとして引き継ぐようロジックを修正する。
     3. `script.js` 内でそのプロパティ（`this.getAttribute('新しい属性')`）を受け取り、UIに反映させる。
     4. 変更後は必ず `scripts/update_readme.py` を実行し、`README.md` のドキュメントを最新状態に更新してください。

4. **コンポーネントのテスト (Testing)**
   * 新しいコンポーネントの追加や既存の変更を行う場合、`tests/components/` ディレクトリにテストファイルを作成・更新することを推奨します。
   * コンポーネントのテストは、「基本機能」「オプションが一切指定されていない場合の挙動」「`# OPTIONS:` に記載されたすべてのオプションが指定された場合の挙動」の3つのシナリオを網羅的にカバーする必要があります。

5. **オプションの変更とスニペットの自動更新 (Snippets Generation)**
   * `src/components/*/parser.py` の `# OPTIONS:` コメントを変更した場合、VS Code や Zed 向けのエディタスニペットを必ず更新してください。
   * 更新には `scripts/generate_snippets.py` スクリプトを実行し、生成されたスニペットファイルもコミットに含める必要があります。

6. **URLや引数の安全な解決 (URL and Argument Resolution)**
   * Markdownの省略記法（例: `@[image: url]`）とキーワード引数（例: `@[image](src: "url")`）の双方を安全かつ一貫して処理するため、コンポーネントパーサーでは `BaseComponentParser.resolve_url_and_label()` を使用してください。また、`title` などのプロパティが省略ラベル構文で渡されてもキーワード引数として渡されても正しく評価されるようにフォールバック（例: `if 'title' in args: title = args['title']`）を実装してください。
   * インラインコンポーネントのブラケット内容やキー・バリュー引数をパースする際は、URLプロトコルの一部であるコロン（例: `://`）がキー・バリューの区切り文字として誤ってパースされないようにスキップする処理を行ってください。
   * ローカルファイルパスや属性内のURLを解決する際は、Markdownプロセッサが付与する可能性のあるエンコードを元に戻すため、必ず `urllib.parse.unquote` でデコードを行ってください。
   * 外部URLを `urllib.request.urlopen` 等でフェッチする際は、非ASCII文字が含まれている可能性を考慮し、`urllib.parse.quote` 等を用いて安全にASCIIエンコードを行い、`UnicodeEncodeError` を防いでください。

7. **入力要素における一意のID管理 (Managing Persistent IDs)**
   * `mono-textfield-input` や `mono-notebook` などの入力コンポーネントでは、再描画時にデータが失われないよう、必ず恒久的なID（例: UUID）をMarkdownに記述してください。
   * エディタ（VS Code や Zed など）では `${UUID}` 変数を含むスニペットを利用することで、コンポーネント配置時に自動で一意のIDを注入できます。

8. **Shadow DOMとスタイリング (Web Components vs Static Utilities)**
   * MonoのWeb ComponentsはShadow DOM（`MonoBaseElement`経由）を利用してカプセル化されています。
   * TailwindなどのグローバルなユーティリティクラスはShadow DOM内に浸透しないため、UIのスタイリングには`themes.toml`で定義されたCSS変数（例: `var(--color-primary)`）を活用してください。

## 5. コンポーネントの変換結果を変更したい場合のアドバイス (Advice for Modifying Conversion Results)

もしAI自身が「コンポーネントの変換結果（HTMLやスタイル）を変更したい」と判断した場合、あるいはユーザーからそのように要求された場合は、以下の指針に従って提案や実装を行ってください。

1. **修正箇所の特定 (Identifying the Modification Target)**
   * **見た目やスタイルの変更:** 基本的に `src/components/コンポーネント名/style.css` を変更します。`parser.py` は触りません。
   * **HTML構造やインタラクションの変更:** `src/components/コンポーネント名/template.html` と `script.js` (または `index.js`) を変更します。
   * **マークダウンからの引数の受け渡し方法の変更:** `src/components/コンポーネント名/parser.py` の正規表現や `get_html` メソッドを変更し、同時に `# OPTIONS:` コメントも更新します。

2. **Shadow DOM を考慮したスタイリング (Styling with Shadow DOM in mind)**
   * MonoのコンポーネントはShadow DOMを利用しています。外部のCSS（Tailwindなど）はコンポーネント内部には適用されません。
   * コンポーネント内の要素のスタイルを変更する場合は、そのコンポーネント専用の `style.css` 内に記述してください。
   * コンポーネント外部（ページ全体）からスタイルを制御可能にしたい場合は、CSS変数（例: `var(--my-custom-color)`）を `style.css` 内で受け取るように設計し、`parser.py` でインラインスタイルとしてそのCSS変数を流し込む手法が有効です。
   * **テーマとの統合:** アラートや背景など、柔らかい背景色や境界線が必要なUI要素をデザインする際は、`-content` 変数を使用するのではなく、CSSの `color-mix()` とセマンティックなベース変数（例: `var(--color-info)`, `var(--color-warning)`）を組み合わせて使用してください。これにより `themes.toml` で定義されたテーマとの一貫性が保たれます。
   * **インライン要素の配置:** テキスト内に自然に流し込むインラインWeb Component（例: `mono-badge`）をデザインする際は、内部のサイズ（`font-size`, `height`, `padding` など）に相対的な `em` 単位を使用し、`:host` 要素に `vertical-align: baseline;` を適用することで、ベースラインへの整列とプロポーショナルなスケーリングを保証してください。
   * **スロット化されたコンテンツの無効化:** Web Component 内にスロット化された Markdown コンテンツ（例: `mono-layout` のカラム）が、Markdown パーサーによって自動挿入された `<p>` や `<br>` タグによって Flexbox や Grid レイアウトを崩す場合は、`content.css` を使用してこれらを無効化してください（例: `<p>` に `display: contents;`、`<br>` に `display: none;`）。
   * **PDFエクスポートと印刷レイアウト:** PDF エクスポート用の Mono コンポーネントを構築する際は、`@media print` CSS ルールを使用して対話型の要素（動画コントロールやテキスト入力など）を `display: none` で隠し、静的な視覚的フォールバックを提供してください。また、PDF へのコードコピー時に文字化けや不要な空白を防ぐため、コードブロックは（`highlight.js` などの）シンタックスハイライトを使わずプレーンな `<pre><code>` タグに依存させ、macOS等の印刷時の文字化けを防ぐため、`font-family` にはAppleのシステム等幅フォント（`ui-monospace` や `SF Mono`）を使用せず、直接 `Menlo`, `Consolas` またはジェネリックな `monospace` を指定してください。
   * **全画面スライドレイアウト:** Mono 内で全画面表示のプレゼンテーション用スライド（例: `mono-section` や `mono-hero`）を作成する場合は、`--component-grid-column: 1 / -1;` を適用してデフォルトの中央揃えグリッドからブレイクアウトさせ、高さを `100vh` に設定してください。

3. **互換性の維持 (Maintaining Compatibility)**
   * `parser.py` を変更して新しい引数を追加する際は、既存のマークダウン記法が壊れないよう、オプショナルな引数として実装してください（例: `args.get('new_param', 'default_value')`）。
   * **正規表現の安全性:** インラインラベルやパラメータがオプショナルな場合（例: `@[theme]()` と `@[theme: dark]()`）、正規表現ではコロンや周囲の空白を厳格に要求するのではなく、明示的にオプショナルになるよう（例: `(?:(?:\:\s*)?([^\]]*))`）設計してください。
   * `parser.py` でタグ構造を変更する場合（特にブロック要素）は、正規表現（`START_PATTERN` / `END_PATTERN`）の意図しないマッチや破滅的バックトラック（Catastrophic Backtracking）を防ぐため、十分に注意してテストを行ってください。特に、ブロックレベルコンポーネントをテストする際は、Markdown 入力に常に終了タグ（例: `@[/flow]`）が含まれていることを確認してください。終了タグを省略すると、ネストされた量指定子によってパース処理が無限に停止するリスクがあります。
   * HTML属性（OpenGraphのディスクリプション等）として挿入されるフェッチ済みのメタデータをPython-Markdownで処理させる場合、パーサーが段落区切りとして解釈してHTMLタグ構造を壊さないように、必ず改行文字（`\n`, `\r`）を取り除くか置換してください。
