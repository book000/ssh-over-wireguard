# AGENTS.md

## 目的
エージェント共通の作業方針を定義する。

## 基本方針
- 会話言語: 日本語
- コメント言語: 日本語
- エラーメッセージ言語: 英語
- コミット規約: Conventional Commits ([description] は日本語)
- 日本語と英数字の間には半角スペースを入れる

## 判断記録のルール
- 判断内容、代替案、採用理由、前提条件、不確実性の明示

## 開発手順（概要）
1. プロジェクト理解 (`action.yml`, `README.md` の確認)
2. 変更実装 (Bash スクリプトの修正など)
3. 動作確認 (GitHub Actions ワークフロー等)

## セキュリティ / 機密情報
- 認証情報 (WireGuard / SSH 秘密鍵) をコミットしない
- ログに機密情報を出力しない

## リポジトリ固有
- GitHub Composite Action であるため、`action.yml` が主要な実装ファイルです。
- 実行環境は Linux (GitHub Hosted Runner 等) を想定しています。
