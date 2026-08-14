---
name: jules-workflow
description: Google Jules (asynchronous coding agent) CLI (jules) の操作方法、非対話モードによるタスク発注、リモート監視、成果物パッチの取り込み、ローカルテスト検証、およびGitリベース同期プロトコル。
---

# Google Jules 連携・受発注および同期プロトコルガイド

本ガイドは、Googleの非同期コーディングエージェント Jules とローカルエージェント（Antigravity等）が協調して開発を行うための標準受発注・検証・同期プロトコルを定めたものです。

---

## 1. 役割分担と協調モデル

- **Jules (リモート・非同期実行)**:
  GitHubリモートリポジトリに接続し、独立した仮想環境上で非同期にタスク処理、リファクタリング、CI構築、機能実装を行います。
- **ローカルエージェント (Antigravity / 開発者)**:
  タスクの切り出し、Julesへの非対話発注、リモート監視、成果物パッチの取り込み、ローカル環境でのテスト検証、およびGit履歴の同期・統合を担当します。

---

## 2. タスク発注プロトコル (非対話モード必須)

### 実行規則
Jules CLI (`jules new`) はデフォルトで対話型TUIとして起動し、ターミナル標準入力を待ち受けます。エージェント環境下で実行する際は、必ず標準入力リダイレクト (`< /dev/null`) および対象リポジトリ (`--repo`) を明示指定して非対話実行する必要があります。

### 発注コマンド構文
```bash
jules new --repo <owner/repo> "詳細なタスク指示文" < /dev/null
```

### 発注時の注意点
1. 発注前にローカルの最新コミットがリモートにプッシュされていることを確認する (`git push origin main`)。
2. コマンド実行後に出力されるセッションIDおよびURLを記録する。

---

## 3. リモート監視プロトコル

### セッション一覧とステータス確認
```bash
# 全リモートセッションの一覧表示
jules remote list --session

# 対象リポジトリのセッション抽出
jules remote list --session | grep "<owner/repo>"
```

### ステータス遷移
- **Planning**: タスク計画策定中
- **In Progress**: コード生成および検証中
- **Completed**: タスク完了（パッチ取得可能）

---

## 4. 成果物取り込みとローカル検証プロトコル

### パッチの取得と適用
```bash
# 差分の事前プレビュー
jules remote pull --session <SESSION_ID>

# ローカルリポジトリへの差分適用
jules remote pull --session <SESSION_ID> --apply
```

### ローカルでの動作検証
パッチ適用後、必ずプロジェクトのテストスイートを実行して整合性を検証します。
```bash
uv run --project . pytest
```

---

## 5. Git同期およびリベース統合プロトコル

複数のエージェントやPRが並行してマージされる開発環境では、リモート履歴が先行して分岐する場合があります。以下の手順で直線的な履歴を維持して統合します。

### 同期手順
1. パッチ内容をステージングしてコミット:
   ```bash
   git add <modified-files>
   git commit -m "commit message"
   ```
2. リモートの最新履歴を取得:
   ```bash
   git fetch origin
   ```
3. リモートの最新コミット上にリベース:
   ```bash
   git rebase origin/main
   ```
4. リベース後のテスト再実行:
   ```bash
   uv run --project . pytest
   ```
5. Fast-Forwardプッシュの実行:
   ```bash
   git push origin main
   ```

---

## 6. トラブルシューティング

| 事象 | 原因 | 対処法 |
|---|---|---|
| セッションがリモートに登録されない / 404エラー | 対話型TUI待受による入力ブロック | コマンド末尾に `< /dev/null` を付与して非対話実行する |
| プッシュ時に non-fast-forward 拒否 | リモート側で先行コミットがマージ済み | `git fetch origin` 後に `git rebase origin/main` を実行して再プッシュする |
| パッチ適用時に No diff found | 変更なし（調査・レビュー等）または失敗 | プロンプト内容を見直し、具体的な成果物作成を指示する |
