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

Markdown 内で `@[コンポーネント名: ラベル](オプション){.クラス}` 構文を用いて埋め込みます（`(...)` は機能オプション、`{...}` はCSSクラス）。

### 主要コンポーネント（Mono コア）

| コンポーネント | 種類 | 概要 | 記述例 |
|---|---|---|---|
| `mono-layout` | ブロック | 水平枠 (`@[hbox]`) や垂直枠 (`@[vbox]`) の配置 | `@[hbox]{.gap-group}\n::: 左\n:::\n::: 右\n:::\n@[/hbox]` |
| `mono-section` | ブロック | フルブリード背景・セクション領域 | `@[section](padding: "group")\n...コンテンツ...\n@[/section]` |
| `mono-zoom` | 自動/明示 | 大画面オートズーム拡大機能（Zキー / クリック） | `@[zoom]()` または `-p presentation` |
| `mono-code-block` | 自動変換 | シンタックスハイライトとコピーボタン付きコードブロック | 通常のコードブロック（```）から自動変換 |
| `mono-mermaid` | ブロック | Mermaid.js 記法のダイアグラム | `@[mermaid]\ngraph TD; A-->B;\n@[/mermaid]` |
| `mono-theme` | インライン | テーマ切り替えセレクター | `@[theme: dark]()` |
| `mono-badge` | インライン | バッジ・タグ表示 | `@[badge: 重要](type: "error")` |
| `mono-icon` | インライン | Google Material Symbols アイコン表示 | `@[icon: star](size: "24", color: "primary")` |
| `mono-link` | ブロック | OGPリッチリンクカード | `@[link: タイトル](url: "https://example.com")` |
| `mono-image` | インライン/ブロック | 最適化画像パーサー | `@[image: 説明](src: "img.png")` |

### インタラクティブ・教育パッケージ（`-p interactive` または個別指定）

| コンポーネント | 種類 | 概要 | 記述例 |
|---|---|---|---|
| `mono-poll` | ブロック | リアルタイム・ローカル投票コンポーネント | `@[poll: 質問](options: "選択肢A, 選択肢B")` |
| `mono-reaction` | ブロック | 絵文字リアクションバー | `@[reaction](emojis: "👍,🎉,❤️")` |
| `mono-ab-test` | ブロック | 2つの画像やコンテンツを並べて比較・投票 | `@[ab-test](src-a: "a.png", src-b: "b.png")` |
| `mono-notebook` | ブロック | 永続化メモ・ノートブック領域 | `@[notebook: メモ](id: "note-1")` |
| `mono-textfield-input` | インライン | 入力データ収集テキストフィールド | `@[textfield-input: 氏名](id: "user-name")` |
| `mono-group-assignment` | ブロック | 参加者のランダムグループ分け | `@[group-assignment](groups: "4")` |
| `mono-session-join` | ブロック | 講義・セッション参加ボタン | `@[session-join](room: "101")` |
| `mono-account` | インライン | ログイン・セッション管理UI | `@[account]()` |

## 拡張 Markdown 記法

- **改行禁止 (Nowrap)**: `{{絶対に改行させないテキスト}}`
- **3×3 デザイントークン (流体タイポグラフィ & 余白)**:
  - `[特大スライド見出し]{.text-display}` （看板スケール）
  - `[標準本文]{.text-body}` （24px基準）
  - `[カラム内・注釈]{.text-compact}` （18〜20px基準）
  - レイアウト余白: `@[hbox]{.gap-flow}` / `{.gap-group}` / `{.gap-item}`
- **Colabリンク自動変換**: `.ipynb` ファイルへのリンクを記述すると、自動的に Google Colab 起動バッジ付きリンクへ変換されます。

## プレゼンテーション・読書キーボードショートカット

Monoで出力されたHTML（特に `-p presentation` や `@[zoom]()` 有効時）では、以下のキーボード操作により極上の読書・プレゼン体験が得られます。

| キー | 機能 | 説明 |
|---|---|---|
| `D` | **フラット表示切替** | デフォルトのアンビエント没頭フォーカス（カレント明度100%、上下減光0.22）と、全体均一100%表示（フラットモード）をワンキーで切り替えます。 |
| `J` / `↓` | **次の章・節へ移動** | 次の見出し（`h1`/`h2`）または水平線（`---`）へ滑らかに自動スクロールします。 |
| `K` / `↑` | **前の章・節へ移動** | 前の見出し（`h1`/`h2`）または水平線（`---`）へ滑らかに自動スクロールします。 |
| `Z` | **ピンポイント拡大** | マウスオーバー中の画像、コードブロック、ダイアグラムなどを全画面モーダルズームします（`Esc` キーまたはオーバーレイ外クリックで閉じます）。 |

