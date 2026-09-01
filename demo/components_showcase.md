# Mono 全コンポーネント ショーケース (Phase 3 カタログ)

このドキュメントは、Monoの全Webコンポーネントの表示・インタラクション・テーマ連動性を一括検証するためのカタログです。

---

## 1. 表示・静的系コンポーネント (Batch A)

### mono-badge
@[badge: 重要](type: "error")
@[badge: 新機能](type: "info")
@[badge: 完了](type: "success")

### mono-icon
@[icon: lucide:sparkles](size: "24", color: "primary")
@[icon: lucide:check-circle-2](size: "24", color: "success")

### mono-link
@[link: Google](url: "https://google.com", description: "検索エンジン", image: "https://www.google.com/favicon.ico")

### mono-section
@[section: セクションタイトル](padding: "md")
これは mono-section コンポーネントのテスト領域です。
@[/section]

---

## 2. UI・インタラクティブ系コンポーネント (Batch B)

### mono-flipcard
@[flipcard: 表のテキスト](back: "裏のテキスト", width: "300px", height: "180px")

### mono-dice
@[dice](sides: "6")

### mono-clock
@[clock](format: "24h")

### mono-countdown
@[countdown](minutes: "5")

---

## 3. フォーム・データ入力系コンポーネント (Batch C)

### mono-poll
@[poll: あなたの好むプレゼンテーション形式は？](options: "スクロール型, スライド型, ハイブリッド型")

### mono-textfield-input
@[textfield-input: アイデアを入力してください](placeholder: "ここに入力...")

### mono-reaction
@[reaction](emojis: "👍,🎉,❤️,🚀")
