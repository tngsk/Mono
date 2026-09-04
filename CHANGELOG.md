# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 蛍光マーカー記法（`==テキスト=={color}`）および蛍光アンダーライン記法（`++テキスト++{color}`）の軽量インライン構文（5色対応: yellow, pink, green, cyan, orange）
- 複数行改行に対応したグラデーション強調描画スタイル（`box-decoration-break: clone`）
- プレゼンテーションモード（`-p presentation`）における手書き蛍光ブラシ機能（`mono-brush`）の標準統合

### Changed
- 手書きブラシのトグル操作を `B` キー（および `Esc` で解除）へと刷新し、マーカー調の蛍光赤ピンク（`rgba(244, 63, 94, 0.75)`）による一定ストローク描画へ変更
- プレゼンター機能（`mono-presenter`）のステータスを開発中（wip / experimental）へ変更

## [2.0.0] - 2026-09-03

### Added
- 3×3 ミニマリスト・デザイントークン体系（Typography Trinity: .text-display, .text-body, .text-compact / Spacing Trinity: --space-flow, --space-group, --space-item）
- @interactive オプトイン・パッケージングアーキテクチャ
- Playwright E2E による完全均一余白・流体スケール自動検証
- CLI `--version`（`-V`）フラグ

### Changed
- 全コアWebコンポーネント（mono-layout, mono-section, mono-zoom, mono-theme, mono-link等）のトークン直結リファクタリング
- mono-image の非WebComponentパーサー最適化（アセット探索スキップ）
- フルスクリーン流体CSS Grid（最大1800px、画面占有率92%）

### Deprecated
- mono-brush（将来的な手書き描画機能の非推奨化）

### Removed
- mono-spacer（空ディレクトリ）
- mono-sync（SSE同期用コンポーネント）

### Fixed
- 流体タイポグラフィにおけるvw係数過大によるスケール停止不具合の解消
- 要素間垂直マージンの完全均一化（112px）
