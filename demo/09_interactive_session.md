# セッションおよび学習支援コンポーネント群仕様検証

演習・講義環境における状態管理およびセッション連携コンポーネントの検証ドキュメント。

---

## アカウント管理（mono-account）

@[account]()

- 動作仕様: ログイン状態を `localStorage`（キー: `mono_auth`）で管理し、状態変更時に `window` オブジェクトへ `mono-auth-changed` イベントを送出。

---

## セッション参加（mono-session-join）およびグループ分け（mono-group-assignment）

@[hbox]{.gap-group}
:::
@[session-join](room: "CS-201")
:::
:::
@[group-assignment](groups: "4")
:::
@[/hbox]

- `mono-session-join`: ルーム番号を指定したセッション接続UI。
- `mono-group-assignment`: 参加者を指定グループ数（1〜N）にランダム配分。

---

## 永続化メモ領域（mono-notebook）

@[notebook: 演習メモ](id: "exercise-notes-1")

- 構文: `@[notebook: タイトル](id: "識別子")`
- 動作仕様: 入力されたMarkdownまたはテキストを自動保存し、リロード後も状態を維持。
