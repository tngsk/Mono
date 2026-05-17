# Mono - Markdown to Monolithic Document

Markdownファイルを、画像（Base64）やCSSが埋め込まれた**単一の自己完結型HTMLファイル**に変換するCLIツールです。ローカルでの配布や共有に最適です。

## 特徴

- **アクセシビリティ (a11y)**: WAI-ARIA対応、キーボード操作のサポート、およびロールベース設計に基づいたWeb Componentsを提供し、多様な環境での利用を想定しています。
- **単一ファイル出力**: 画像をBase64として埋め込み、外部リソース依存のないHTMLを生成（共有が容易）。
- **コードブロック**: Highlight.jsによるシンタックスハイライトと、ワンクリック「コピー」ボタンを自動付与。
- **Colabリンク自動変換**: `.ipynb` を指すリンクを検知し、Google Colabの起動バッジ付きリンク（別タブで開く）へ自動変換。
- **カスタム記法**: `{{テキスト}}` と記述すると、改行を防ぐ `nowrap` スパンに変換。
- **画像の最適化と遅延読み込み**: 画像をWebPに変換・SVGをインライン化し、非同期注入戦略によって遅延読み込みを行うことでパフォーマンスを最適化。
- **ファイルサイズ検証**: 出力ファイルのサイズを検証し、30MBを超える場合は警告・停止（`--force` でバイパス可能）。
- **セキュリティ設定（CSP）**: `config.toml` から設定を読み込み、Content-Security-Policyタグを自動設定。
- **Web Components対応**: 外部依存なしのVanilla JSによるWeb Componentsの埋め込みに対応。多彩なUIコンポーネントをMarkdown内に記述可能です。

### 利用可能な Web Components 一覧

Monoでは外部依存なしのVanilla JSによる多彩なWeb Componentsを埋め込むことができます。各コンポーネントはカスタムMarkdown記法で記述します。

#### 明示的コンポーネント

| コンポーネント | 概要 | 記述例 | オプション |
|---|---|---|---|
| `mono-ab-test` | A/Bテスト用のコンポーネント。2つの画像やコンテンツを並べて比較します。 | `@[ab-test](src-a: "img1.png", src-b: "img2.png")` | `src-a="url"`<br>`src-b="url"`<br>`title="text"` |
| `mono-account` | ログインなどのアカウント管理UIを表示します。 | `@[account]()` | なし |
| `mono-badge` | バッジを表示します。 | `@[badge: "New!"](color: "red")` | `text="text"`<br>`color="red|blue|..."`<br>`soft="true|false"`<br>`outline="true|false"` |
| `mono-clock` | 時計を表示します。 | `@[clock](display: "analog")` | `display="analog|digital"`<br>`format="24h|12h"` |
| `mono-countdown` | カウントダウンタイマーを表示します。 | `@[countdown](time: "60", color: "red")` | `time="10m|2024-12-31T23:59:59"`<br>`color="red|blue|..."` |
| `mono-dice` | サイコロを表示し、クリックで振ることができます。 | `@[dice](number: 2, faces: 6)` | `number="1~6"`<br>`faces="4|6|8|10|12|20"` |
| `mono-drawer` | 引き出し式のサイドメニュー（ドロワー）を表示します。ブロック要素。 | `@[drawer](position: "left", open: "false")\n...コンテンツ...\n@[/drawer]` | `label="text"`<br>`position="left|right"`<br>`open="true|false"` |
| `mono-flipcard` | クリックまたはホバーで裏返るカード。 | `@[flipcard: "Front Text"](answer: "Back Text")` | `front_text="text"`<br>`answer="text"` |
| `mono-flow` | フローチャート（ノードとエッジ）を表示します。 | `@[flow: "フロー"](direction: "LR")<br>A -> B<br>@[/flow]` | `title="text"`<br>`direction="TB|LR"` |
| `mono-group-assignment` | グループ分けを行うコンポーネント。 | `@[group-assignment](title: "グループ分け")` | `title="text"` |
| `mono-hero` | ヒーローバナー領域を表示します。ブロック要素。 | `@[hero](bg-color: "#000", text-color: "#fff")\n...コンテンツ...\n@[/hero]` | `title="text"`<br>`image="url"`<br>`mode="light|dark"`<br>`bg-color="#HEX"`<br>`text-color="#HEX"` |
| `mono-icon` | アイコンを表示します。 | `@[icon: star](size: "24", color: "yellow")` | `name="star|heart|..."`<br>`size="16~128"`<br>`color="red|#HEX"`<br>`display="inline|block"` |
| `mono-image` | 画像を表示します。 | `@[image]()` | `src="url"`<br>`alt="text"`<br>`width="size"`<br>`height="size"` |
| `mono-layout` | 横並び（hstack）や縦並び（vstack）のレイアウトを構築します。ブロック要素。 | `@[hstack]\n:::\n左側コンテンツ\n:::\n右側コンテンツ\n@[/hstack]` | `label="text"`<br>`class="text"` |
| `mono-link` | リンクカードを表示します。 | `@[link]()` | `url="url"`<br>`style="full|small|card"` |
| `mono-media-grid` | 複数のメディアをグリッド状に配置して表示します。ブロック要素。 | `@[media-grid]()\n...コンテンツ...\n@[/media-grid]` | `label="text"`<br>`columns="number"`<br>`rows="number"`<br>`gap="css-size"`<br>`fit="cover|contain"` |
| `mono-mermaid` | Mermaid記法で図表を描画し、SVGとして埋め込みます。ブロック要素。 | `@[mermaid]\ngraph TD;\nA-->B;\n@[/mermaid]` | `title="text"`<br>`theme="default|dark|forest|..."` |
| `mono-notebook` | 入力可能なノートブック領域を表示します。 | `@[notebook](title: "メモ", placeholder: "入力してください")` | `title="text"`<br>`placeholder="text"`<br>`id="text"` |
| `mono-poll` | 投票システムを表示します。 | `@[poll](title: "好きな言語は？", options: "Python, JavaScript")` | `title="text"`<br>`options="A,B,C"` |
| `mono-reaction` | リアクション（いいね、など）ボタンを表示します。 | `@[reaction](options: "👍, 👎")` | `label="text"`<br>`options="👍,👎"` |
| `mono-score` | 楽譜を表示します。 | `@[score](clef: "treble", notes: "C4 D4 E4")` | `notes="C4 D4 E4"`<br>`clef="treble|bass"`<br>`time="4/4|3/4"`<br>`voices='["C4 D4", "E4 F4"]'` |
| `mono-section` | セクション領域を表示します。ブロック要素。 | `@[section](bg-color: "#f0f0f0")\n...コンテンツ...\n@[/section]` | `title="text"`<br>`image="url"`<br>`mode="light|dark"`<br>`bg-color="#HEX"`<br>`text-color="#HEX"`<br>`height="px|vh"`<br>`width="px|vw"` |
| `mono-session-join` | セッション（同期・データ収集）へ参加するボタン等を表示します。 | `@[session-join](title: "参加する")` | `title="text"` |
| `mono-sound` | 効果音や音声を再生するボタンを表示します。 | `@[sound](src: "audio.mp3", label: "再生")` | `label="text"`<br>`src="url"` |
| `mono-spacer` | 空白（スペーサー）を挿入します。 | `@[spacer](width: "10px", height: "20px")` | `width="px|rem"`<br>`height="px|rem"` |
| `mono-synth` | Tone.jsを用いたシンプルなシンセサイザー。OSC, Filter, ADSR, ミニ鍵盤を備えます。 | `@[mono-synth: sample="asset-test.wav"]()` | `sample="url"`<br>`label="text"` |
| `mono-textfield-input` | テキスト入力フィールドを表示します。 | `@[textfield](placeholder: "テキストを入力", size: "large")` | `label="text"`<br>`id="text"`<br>`placeholder="text"`<br>`size="small|medium|large"` |
| `mono-theme` | テーマ切り替えコンポーネント。通常はMarkdownディレクティブでテーマを設定します。 | `@[theme: dark]()` | `theme_name="light|dark"`<br>`show_ui="true|false"`<br>`config="json"` |

#### 暗黙的・システムコンポーネント

これらのコンポーネントはオプションやサーバー構成によって自動的に組み込まれます。

- `mono-brush`: 描画オーバーレイ機能。暗黙的に全ページに組み込まれるか、特定条件で有効化されます。
- `mono-code-block`: コードブロックコンポーネント。コードブロックが存在する場合に暗黙的に組み込まれます。
- `mono-export`: 外部エクスポート機能。`--export`オプションで強制的に有効になります。
- `mono-sync`: 状態同期・通信機能。サーバーとのSSE/HTTP通信を管理し、暗黙的に組み込まれます。

## セットアップ

依存管理に `uv` を使用します。

```bash
uv sync
```

## 使い方

### 基本的な変換
入力ファイル名に基づいて `document.html` が生成されます。

```bash
uv run main.py document.md
```

### カスタムCSSを埋め込む
複数のCSSファイルを指定して埋め込むことができます。

```bash
uv run main.py document.md -c style.css theme.css
```

### 出力ファイルの指定と詳細ログ
`-o` で出力先を指定し、`-v` で変換プロセスの詳細なログを確認します。

```bash
uv run main.py document.md -o docs/index.html -v
```

### HTMLタグの除外処理
指定したタグ（およびその中身）を出力HTMLから削除します。

```bash
uv run main.py document.md -e hr div
```

### カスタムテンプレートを使用する
カスタムのHTMLテンプレートを指定して変換します。

```bash
uv run main.py document.md -t custom_template.html
```

### ファイルサイズ制限をバイパスする
出力HTMLが30MBを超える場合、デフォルトではエラーになりますが `--force` で強制的に保存できます。

```bash
uv run main.py document.md --force
```

### 同期・データ収集サーバーの起動
同期機能（スクロール同期など）やデータ収集（投票結果など）を使用する場合は、付属のFastAPIサーバーを起動します。

```bash
uv run server.py
```
サーバーはデフォルトで `http://0.0.0.0:8000` で起動し、API (`/api/sync/stream`) とデータ収集API (`/api/data`) を提供します。

---

すべてのオプションを確認するにはヘルプを参照してください：

```bash
uv run main.py --help
```

## 変更ログ

- `mono-icon`コンポーネントの追加
- `mono-spacer`コンポーネントによる水平/垂直スペーシングのサポート
- デスクトップアプリの設計ドキュメントの最終化
- GIFアニメーションサポートツールの設計ドキュメント追加
- 効果音コンポーネント `mono-sound` の追加
- ディレクトリ構造の `src/` 配下へのリファクタリング
- 描画オーバーレイのための `mono-brush` コンポーネント追加
- 方向ベースのレイアウトシステム `mono-layout` の追加

### セキュリティ設定と環境変数

FastAPI サーバー (`server.py`) は、`config.toml` によって CORS ポリシーを設定できますが、環境変数 `ENVIRONMENT` を用いてセキュリティレベルを動的に変更します。

- **ローカル開発時 (デフォルト設定)**:
  `ENVIRONMENT` が設定されていない、または `development` などの場合、ローカルでの動作やテストを優先し、すべてのメソッド・ヘッダーを許可し、`config.toml` に設定された任意のオリジン（`null` などを含む）を受け入れます。
- **本番環境への展開 (`ENVIRONMENT=production`)**:
  サーバーを本番環境やリモートにデプロイする際は、必ず環境変数 `ENVIRONMENT=production` を設定してください。これにより、`config.toml` から危険なオリジン（`*` や `null`）が自動的に除外され、許可される HTTP メソッド (`GET`, `POST`, `OPTIONS`) やヘッダーが厳格に制限されます。
