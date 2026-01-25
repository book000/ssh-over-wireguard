# GEMINI.md

## 目的
Gemini CLI 向けのコンテキストと作業方針を定義する。

## 出力スタイル
- 言語: 日本語
- トーン: 専門的かつ簡潔
- 形式: Markdown

## 共通ルール
- 会話言語: 日本語
- コミット規約: Conventional Commits ([description] は日本語)
- 日本語と英数字の間には半角スペースを入れる

## プロジェクト概要
- 目的: WireGuard VPN 経由で SSH/SCP を実行する GitHub Action
- 主な機能: VPN 接続、SSH コマンド実行、SCP 転送

## コーディング規約
- フォーマット: `action.yml` の既存スタイルに従う
- 命名規則: ケバブケース (inputs 等)
- コメント言語: 日本語
- エラーメッセージ言語: 英語

## 開発コマンド
特定のパッケージマネージャーは使用していません。
GitHub Actions のワークフロー定義ファイルが開発・テストの主戦場となります。

## 注意事項
- 認証情報のコミット禁止
- ログへの機密情報出力禁止
- 既存の `action.yml` の構造を維持する
- WireGuard のセットアップには `sudo` 権限が必要であることを考慮する

## リポジトリ固有
- `runs.using: 'composite'` を使用しているため、各ステップで `shell: bash` を明示する必要があります。
- WireGuard 関連パッケージ (`wireguard-tools`/`wireguard`) のインストール手順が含まれています。
