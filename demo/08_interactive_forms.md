# インタラクティブ入力コンポーネント群仕様検証

`-p interactive` プロファイルまたは個別の `@interactive` コンポーネント群の動作検証ドキュメント。

---

## 投票コンポーネント（mono-poll）

@[poll: 実行環境の選択](options: "ローカル（uv）, サーバー（Docker）, クラウド")

- 構文: `@[poll: 設問](options: "選択肢1, 選択肢2, ...")`
- 動作仕様: 投票結果を `localStorage`（キー: `mono_poll_*`）へ記録し、集計バーを即時更新。

---

## 絵文字リアクション（mono-reaction）

@[reaction](emojis: "👍,🎉,🚀,👀")

- 構文: `@[reaction](emojis: "絵文字カンマ区切り")`
- 動作仕様: ボタン押下によるカウントインクリメントおよびローカル状態の保持。

---

## 比較テスト（mono-ab-test）

@[ab-test](src-a: "https://picsum.photos/400/200?random=1", src-b: "https://picsum.photos/400/200?random=2")

- 構文: `@[ab-test](src-a: "画像A", src-b: "画像B")`
- 効果: 2つの選択肢を並列表示し、クリック投票を記録。

---

## テキスト入力（mono-textfield-input）

@[textfield-input: 参加者ID](id: "participant-id")

- 構文: `@[textfield-input: ラベル](id: "識別子")`
- 動作仕様: 入力文字列を `localStorage` の `mono_textfield_*` にリアルタイム同期。
