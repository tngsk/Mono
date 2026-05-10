# 探索型 UI エクステンション アップデート計画書 (Exploration UI Update Plan)

本ドキュメントは、Mono の「探索型 UI エクステンション」の実装計画を定義します。Mono を単なる読み物ではなく、「Executable Instrument（実行可能な計器）」として機能させるためのアーキテクチャアップデートを含みます。

## 1. 概要

「Disorientation（迷子症状）」リスクに対応しつつ、「Mono らしさ（現象の探索を主眼とする）」を維持するため、以下の3つの UI コンポーネントの追加・改修を行います。

*   **`mono-scroll-range`**: スクロール位置を変数化し（Scrollytelling）、能動的な探査を可能にする機能。既存の `mono-sync` コンポーネントに統合します。
*   **`mono-hud`**: 常に画面の最前面に固定され、現在の実験状態・変数を表示するステータスバー。既存の `mono-drawer` を拡張（HUD モードの追加）することで実現します。
*   **`mono-section-map`**: 現在位置を視覚化する空間的ランドマーク。右端に表示されるシンプルなナビゲーション（マイクロインタラクション）として新規実装します。

---

## 2. 実装詳細

### A. `mono-sync` への `mono-scroll-range` 機能の統合 (Scrollytelling)

`mono-sync` は本来、空間的アンカリングを設定する役割も担う予定であったため、スクロール位置の監視と変数化機能をここに統合します。

*   **対象ファイル:** `src/components/mono-sync/script.js`
*   **実装方針:**
    *   `window.addEventListener('scroll', ...)` を用いてスクロールイベントを監視します。
    *   **パフォーマンス要件:** 大量のアニメーションによる BYOD 環境（特に低スペックなスマートフォン）での熱スロットリングを防ぐため、イベントの発火には必ず `requestAnimationFrame` または throttle（間引き）処理を施します。
    *   **変数の計算と出力:** 現在のスクロール位置をドキュメント全体の高さに対する割合 (`0.0` 〜 `1.0`) として計算します。
    *   **同期:** 計算されたスクロール位置を、CSS 変数（例: `--mono-scroll-position`）として `:root` または `document.body` に設定します。また、必要に応じてカスタムイベント（例: `mono-scroll-update`）を発火し、他のコンポーネント（Web Audioのパラメータや波形表示など）がこの値を利用できるようにします。

### B. `mono-drawer` の HUD (Heads-Up Display) モード拡張 (Sticky Interface)

既存の `mono-drawer` を拡張し、常に開いた状態で画面に固定される「HUD」として機能できるようにします。

*   **対象ファイル:**
    *   `src/components/mono-drawer/parser.py`
    *   `src/components/mono-drawer/script.js`
    *   `src/components/mono-drawer/style.css`
*   **実装方針:**
    *   **Markdown 引数の追加:** 新しいオプション `hud="true|false"` (または `mode="hud"`) を追加します。
    *   **スタイリングと重なり対策:** HUD モードが有効な場合、ドロワーのハンドル（開閉ボタン）を非表示にし、コンテナを常に画面上部（または指定位置）に `position: fixed` で固定します。ドキュメント内の見出しや `mono-section-map` との視覚的な重なり（オーバーラップ）を防ぐため、`script.js` 側で HUD の高さを計算し、`document.body` に対して適切な `padding-top` を自動付与します。さらに、`style.css` で HUD の背景に透過性を持たせる等のスタイルガイドを含めます。
    *   **状態の監視と表示:** `script.js` 内で、実験のグローバル変数（`localStorage` に保存される `mono_` プレフィックスのデータなど）やカスタムイベント（例: `mono-data`）を監視します。HUD 内の特定の要素（例: `<span data-bind="variable_name">`）のテキストコンテンツを、監視している変数の値で動的に更新します。これにより、認知的なアンカーとして機能させます。

### C. 新規コンポーネント: `mono-section-map` (Landmarks)

スクロール時のコンテクスト喪失を防ぐ「記憶の栞」となる、シンプルなナビゲーションドットを実装します。

*   **新規ディレクトリ:** `src/components/mono-section-map/`
*   **構成ファイル:** `parser.py`, `script.js`, `style.css`, `content.css`, `template.html`
*   **実装方針:**
    *   **疎結合と責任分離:** 新規コンポーネント実装時には「疎結合と責任分離の明確化」という原則を徹底します。`parser.py` はHTML出力のみを担当し、ロジックは `script.js`、スタイルはShadow/Light DOMで明確に分離します。
    *   **マイクロインタラクション:** 画面の右端に固定（`position: fixed`）された、小さなドットのリストとして描画します。
    *   **見出しの抽出:** `script.js` にて、ドキュメント内の主要なセクション（`<h1>`, `<h2>` など、あるいは `mono-section` 要素）を抽出します。
    *   **アクセシビリティと明瞭性の確保:** ドットのみの表示では意味が伝わりにくいため、各ドットにホバーした際にセクションのタイトルを表示するツールチップ（または CSS によるヒント表示）を実装します。同時に、`script.js` 側で抽出したセクション名を用いて、各ドットに `aria-label` を付与し、スクリーンリーダー等のアクセシビリティ（a11y）を確保します。
    *   **現在位置のハイライト:** `IntersectionObserver` を利用して、現在画面に表示されているセクションを判定し、対応するドットの色やサイズを変更してハイライトします。
    *   ドットをクリックすることで、該当セクションへスムーズスクロール（`scrollIntoView({ behavior: 'smooth' })`）する機能を付加します。
    *   極力シンプルで軽量な実装を心がけます。

---
## 3. 依存関係と制約事項

*   実装はすべて Vanilla JS で行い、外部ライブラリ（jQuery, React など）は使用しません。
*   既存の Mono アーキテクチャの制約（30MB制限、オフライン動作可能）を遵守します。
*   各コンポーネントのテスト (`uv run pytest`) が通過することを確認した上でコミットします。E2Eテストについては、`test_browser_mono_<component_name>.py` というプレフィックスを付けて作成し、`import file mismatch` エラーを防ぎます。
