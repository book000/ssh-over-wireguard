# GitHub Copilot Instructions

## プロジェクト概要
- 目的: WireGuard VPN を介してリモートサーバーに安全に接続し、SSH コマンドの実行や SCP ファイル転送を行う GitHub Action。
- 主な機能: WireGuard 接続の確立、SSH コマンド実行、SCP ファイル転送（アップロード/ダウンロード）、接続テスト。
- 対象ユーザー: GitHub Actions を利用する開発者。

## 共通ルール
- 会話は日本語で行う。
- PR とコミットは Conventional Commits に従う。
- 日本語と英数字の間には半角スペースを入れる。
- コード内のコメントは日本語で記載する。

## 技術スタック
- 言語: Bash (GitHub Actions Composite Action)
- ツール: WireGuard (wireguard-tools), OpenSSH

## 開発コマンド
このリポジトリは GitHub Composite Action であり、標準的なパッケージマネージャーによるインストールやビルドコマンドはありません。
動作確認は GitHub Actions のワークフロー上で行います。

## テスト方針
- 手動または自動の GitHub Actions ワークフローによる結合テスト。
- 接続テスト機能 (`ping-check`) による疎通確認。

## セキュリティ / 機密情報
- WireGuard の秘密鍵や SSH の秘密鍵などの認証情報をコードに含めない。
- GitHub Secrets を使用して管理する。
- ログに秘密鍵やパスワードを出力しない。

## ドキュメント更新
- `README.md`
- `README-ja.md`
- `action.yml` (入力パラメータの変更時)

## リポジトリ固有
- `action.yml` がエントリポイントです。
- composite action として実装されており、`steps` 内で `shell: bash` を使用してコマンドを実行しています。
