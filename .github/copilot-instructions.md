# GitHub Copilot Instructions

WireGuard VPN 経由でリモートサーバーに接続し、SSH コマンド実行や SCP 転送を行う GitHub Composite Action。実装の本体は `action.yml` の `runs.steps` に書かれた Bash スクリプトである。レビュー時は以下を重点的に確認する。

## セキュリティ (最重要)
- WireGuard/SSH の秘密鍵・プリシェアードキー・ホストキー等の認証情報がハードコードされていないか。値は必ず `inputs` 経由で受け取る。
- 秘密鍵やパスワードが `echo` やコマンド出力でログに露出していないか。`sudo tee` で機密を書き込む際に標準出力へ漏れていないか (`> /dev/null` の付与を確認)。
- `/tmp/id_rsa` や `~/.ssh/config`、`/etc/wireguard/wg0.conf` などの秘密情報を含むファイルに適切なパーミッション (`chmod 600`) が設定されているか。
- SSH ホストキー検証を無効化していないか (`StrictHostKeyChecking=no` の追加や `known_hosts` の省略は不可)。MITM 対策として `ssh-host-key` による検証を維持すること。
- `Cleanup` ステップで秘密鍵ファイルと VPN 接続が確実に破棄されるか (`if: always()` の維持)。

## Composite Action の規約
- 各 `run` ステップに `shell: bash` が明示されているか。
- `${{ inputs.* }}` を含む Bash はコマンドインジェクションに注意する。ユーザー入力を展開してコマンド実行する箇所 (`command`、`scp-source` 等) の扱いを確認する。
- 新規 `inputs` はケバブケース (例: `ssh-host-ip`)。`required` と `default` の指定が実際の利用と整合しているか。
- WireGuard セットアップは `sudo` 前提。権限や `wg-quick` の失敗時ハンドリングを確認する。

## 整合性
- `action.yml` の `inputs` を追加・変更・削除した PR では、`README.md` と `README-ja.md` の入力パラメータ表も更新されているか。
- 条件付きステップ (`if:` による `operation`/`scp-direction` の分岐) が新しい入力と矛盾しないか。

## フラグ不要な既知パターン
- WireGuard フルパッケージのインストール失敗を握りつぶして `wireguard-tools` のみで続行する処理は意図的な設計 (コンテナ環境向け)。バグとして指摘しない。
- ステータス表示の絵文字 (✅ / ⚠️ 等) はスタイルとして許容されている。

## コメント
- レビューコメント・指摘は日本語で行う。日本語と英数字の間には半角スペースを入れる。
