# Mono - Markdown to Monolithic Document

Markdownファイルを、画像（Base64）やCSSが埋め込まれた**単一の自己完結型HTMLファイル（Single-File HTML）**に変換する高速CLIツールです。プロジェクターでのプレゼンテーションから配布用ドキュメントまで、ローカル・オフライン環境で完全動作します。

## セットアップ

依存関係の管理には `uv` を使用します。

```bash
uv sync
```

## 主な特徴 (Mono v2.0)

- **完全オンデマンド注入 (Zero-JS)**: 使用されているWeb Componentsのみをツリーシェイキングして注入。静的ドキュメントはJavaScript不要の約10KBの極小HTMLを出力。
- **フルスクリーン流体レイアウト**: 画面幅に応じて最大1750px（画面占有率91%〜92%）までダイナミックに伸縮し、大画面プロジェクターでも無駄な余白を排したスライド表示を実現。
- **スクリーンフィリング・タイポグラフィ**: `.text-display` クラスにより、2〜3文字のキーワードが画面幅の約80%を埋め尽くす迫力のスライド見出しを生成。
- **包括的デザイントークン**: DaisyUI着想の `themes.toml` により、ライト/ダーク/コーポレート/学習用などのテーマ切り替えに全コンポーネントが即時連動。
- **単一ファイル自己完結**: 画像をWebP/Base64変換し、SVGをインライン化して単一HTML内に完結。
- **アクセシビリティ (a11y)**: WAI-ARIA対応、キーボード操作（Tab/Enter/Space/Esc）、および44x44px以上のタッチターゲットを標準装備。
- **印刷 & PDF 最適化**: `@media print` による静的フォールバックと正確な色再現（`print-color-adjust: exact`）を全コンポーネントに配備。

## 使い方

### 基本的な変換

入力ファイル名に基づいて単一HTMLが生成されます。

```bash
uv run main.py document.md
```

### 出力先とプロファイルの指定

`-p` (`--profile`) で用途に応じたプリセットを選択できます。

```bash
# プレゼンテーション用（オートズーム mono-zoom を自動有効化）
uv run main.py slides.md -o output.html -p presentation

# 完全静的ドキュメント用（Zero-JS 出力）
uv run main.py doc.md -o output.html -p static
```

### テーマの指定

```bash
# テーマを直接指定して変換（light, dark, corporate, calm-study）
uv run main.py document.md --theme dark
```

### PDF エクスポート

単一の縦長 monolithic PDF として書き出します（Playwrightが必要です）。

```bash
uv run main.py document.md --pdf -o document.pdf
```

### ファイルサイズ制限のバイパス

出力HTMLが30MBを超える場合、デフォルトではエラーになりますが `--force` で強制的に保存できます。

```bash
uv run main.py document.md --force
```

### リアルタイム同期・データ収集サーバーの起動

```bash
uv run server.py
```

---

## 利用可能な Web Components 一覧

Markdown 内で `@[コンポーネント名: ラベル](キー: "値")` 構文を用いて埋め込みます。

| コンポーネント | 種類 | 概要 | 記述例 |
|---|---|---|---|
| `mono-ab-test` | ブロック | 2つの画像やコンテンツを並べて比較・投票 | `@[ab-test](src-a: "a.png", src-b: "b.png")` |
| `mono-account` | インライン | ログイン・セッション管理UI | `@[account]()` |
| `mono-badge` | インライン | バッジ・タグ表示 | `@[badge: 重要](type: "error")` |
| `mono-clock` | ブロック | アナログ/デジタル時計 | `@[clock](format: "24h")` |
| `mono-code-block` | 自動変換 | シンタックスハイライトとコピーボタン付きコードブロック | 通常のコードブロック（```）から自動変換 |
| `mono-countdown` | ブロック | カウントダウンタイマー | `@[countdown](minutes: "5")` |
| `mono-dice` | ブロック | クリックで振れるサイコロ | `@[dice](sides: "6")` |
| `mono-drawer` | ブロック | 引き出し式サイドメニュー | `@[drawer: メニュー]()\n...コンテンツ...\n@[/drawer]` |
| `mono-flipcard` | ブロック | 表裏が反転するフラッシュカード | `@[flipcard: 問題](back: "解答")` |
| `mono-flow` | ブロック | ノードと矢印による軽量フローチャート | `@[flow]\nA -> B\n@[/flow]` |
| `mono-group-assignment` | ブロック | 参加者のランダムグループ分け | `@[group-assignment](groups: "4")` |
| `mono-hero` | ブロック | フルブリードのヒーローバナー | `@[hero: タイトル](mode: "dark")` |
| `mono-icon` | インライン | Lucide / Material アイコン表示 | `@[icon: star](size: "24", color: "primary")` |
| `mono-image` | ブロック | キャプション・ズーム対応の最適化画像 | `@[image: 説明](src: "img.png")` |
| `mono-layout` | ブロック | 横並び (`@[hstack]`) や縦並び (`@[vstack]`) | `@[hstack](class: "gap-md")\n:::左\n:::\n:::右\n:::\n@[/hstack]` |
| `mono-link` | ブロック | OGPリッチリンクカード | `@[link: タイトル](url: "https://example.com")` |
| `mono-media-grid` | ブロック | 複数メディアのレスポンシブグリッド | `@[media-grid](columns: "2")\n...画像...\n@[/media-grid]` |
| `mono-mermaid` | ブロック | Mermaid.js 記法のダイアグラム | `@[mermaid]\ngraph TD; A-->B;\n@[/mermaid]` |
| `mono-notebook` | ブロック | 永続化メモ・ノートブック領域 | `@[notebook: メモ](id: "note-1")` |
| `mono-poll` | ブロック | リアルタイム・ローカル投票コンポーネント | `@[poll: 質問](options: "選択肢A, 選択肢B")` |
| `mono-reaction` | ブロック | 絵文字リアクションバー | `@[reaction](emojis: "👍,🎉,❤️")` |
| `mono-score` | インライン | ABC記譜法による楽譜レンダリング | `@[score](notes: "C D E F")` |
| `mono-section` | ブロック | フルブリード背景セクション領域 | `@[section](padding: "md")\n...コンテンツ...\n@[/section]` |
| `mono-session-join` | ブロック | 講義・セッション参加ボタン | `@[session-join](room: "101")` |
| `mono-sound` | インライン | 音声・効果音再生ボタン | `@[sound: 再生](src: "sound.mp3")` |
| `mono-synth` | ブロック | Web Audio による対話型シンセサイザー | `@[mono-synth]()` |
| `mono-textfield-input` | インライン | 入力データ収集テキストフィールド | `@[textfield-input: 氏名](id: "user-name")` |
| `mono-theme` | インライン | テーマ切り替えセレクター | `@[theme: dark]()` |
| `mono-zoom` | 自動/明示 | 大画面オートズーム拡大機能（Zキー / クリック） | `@[zoom]()` または `-p presentation` |

## 拡張 Markdown 記法

- **改行禁止 (Nowrap)**: `{{絶対に改行させないテキスト}}`
- **テキストサイズ変更 (流体スケール)**:
  - `[特大スライド見出し]{.text-display}` （画面幅の約80%を埋め尽くす可変フォント）
  - `[大文字キーワード]{.text-xlarge}`
  - `[リード文]{.text-large}`
  - `[注釈]{.text-small}`
- **Colabリンク自動変換**: `.ipynb` ファイルへのリンクを記述すると、自動的に Google Colab 起動バッジ付きリンクへ変換されます。
