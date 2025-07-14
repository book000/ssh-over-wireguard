# SSH over WireGuard

WireGuard VPN 経由でリモートサーバーに安全な暗号化接続を確立し、SSH コマンドの実行や SCP ファイル転送を行う GitHub Action です。

## 機能

- 🔒 **セキュアな VPN 接続**: 安全な通信のための WireGuard VPN トンネルを確立
- 🖥️ **SSH コマンド実行**: VPN 経由でリモートサーバー上でコマンドを実行
- 📁 **SCP ファイル転送**: SCP を使用してファイルを安全にアップロード・ダウンロード
- 🔍 **接続テスト**: VPN 接続を確認するためのオプションの ping テスト
- 🛡️ **セキュリティ機能**: ホストキー検証、適切な権限処理
- 🧹 **自動クリーンアップ**: 実行後に VPN を切断し、SSH キーをクリーンアップ

## 使用方法

### 基本的な SSH コマンド実行

```yaml
- name: WireGuard VPN 経由で SSH コマンドを実行
  uses: book000/ssh-over-wireguard@v1
  with:
    # WireGuard 設定
    wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
    wireguard-address: "10.0.0.2/24"
    wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
    wireguard-endpoint: "your-server.com:51820"
    wireguard-allowed-ips: "10.0.0.0/24"
    
    # SSH 設定
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
    ssh-user: "ubuntu"
    ssh-hostname: "myserver"
    ssh-host-ip: "10.0.0.1"
    ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
    
    # 操作設定
    operation: "ssh"
    command: "uptime && df -h"
```

### SCP ファイルアップロード

```yaml
- name: WireGuard VPN 経由でファイルをアップロード
  uses: book000/ssh-over-wireguard@v1
  with:
    # WireGuard 設定
    wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
    wireguard-address: "10.0.0.2/24"
    wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
    wireguard-endpoint: "your-server.com:51820"
    wireguard-allowed-ips: "10.0.0.0/24"
    
    # SSH 設定
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
    ssh-user: "ubuntu"
    ssh-hostname: "myserver"
    ssh-host-ip: "10.0.0.1"
    ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
    
    # SCP 操作
    operation: "scp"
    scp-source: "./build/app.tar.gz"
    scp-destination: "/home/ubuntu/releases/"
    scp-direction: "upload"
```

### SCP ファイルダウンロード

```yaml
- name: WireGuard VPN 経由でファイルをダウンロード
  uses: book000/ssh-over-wireguard@v1
  with:
    # ... 上記と同じ WireGuard と SSH 設定 ...
    
    # SCP 操作
    operation: "scp"
    scp-source: "/var/log/application.log"
    scp-destination: "./logs/"
    scp-direction: "download"
```

## 入力パラメータ

### 操作設定

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `operation` | 操作タイプ: `ssh` (コマンド実行) または `scp` (ファイル転送) | いいえ | `ssh` |
| `ping-check` | SSH/SCP 操作前の接続テスト（ping）を有効にする | いいえ | `true` |

### SSH 操作

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `command` | リモートサーバーで実行するコマンド（operation=ssh の場合のみ使用） | いいえ | `hostname && whoami && pwd` |

### SCP 操作

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `scp-source` | SCP 操作のソースパス（operation=scp の場合のみ使用） | はい* | - |
| `scp-destination` | SCP 操作の宛先パス（operation=scp の場合のみ使用） | はい* | - |
| `scp-direction` | SCP 方向: `upload` (ローカルからリモート) または `download` (リモートからローカル) | いいえ | `upload` |

*`operation=scp` の場合に必須

### WireGuard 設定

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `wireguard-private-key` | WireGuard クライアントプライベートキー | はい | - |
| `wireguard-address` | WireGuard クライアント VPN アドレス（例: 10.0.0.2/24） | はい | - |
| `wireguard-peer-public-key` | WireGuard サーバーパブリックキー | はい | - |
| `wireguard-endpoint` | WireGuard サーバーエンドポイント（例: server.com:51820） | はい | - |
| `wireguard-allowed-ips` | WireGuard の許可 IP（例: 10.0.0.0/24） | はい | - |
| `wireguard-preshared-key` | WireGuard 事前共有キー（オプションのセキュリティ強化） | いいえ | - |
| `wireguard-dns` | DNS サーバーアドレス | いいえ | `1.1.1.1` |

### SSH 設定

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `ssh-private-key` | 認証用 SSH プライベートキー | はい | - |
| `ssh-user` | SSH ユーザー名 | はい | - |
| `ssh-hostname` | SSH 接続用ホスト名エイリアス | はい | - |
| `ssh-host-ip` | VPN 内の SSH サーバー IP アドレス | はい | - |
| `ssh-host-key` | 検証用 SSH サーバーホストキー | はい | - |
| `ssh-port` | SSH ポート番号 | いいえ | `22` |

## セキュリティに関する考慮事項

### シークレット管理

すべての機密情報を GitHub Secrets として保存してください：

```yaml
secrets:
  WG_PRIVATE_KEY: "your-wireguard-private-key"
  WG_SERVER_PUBLIC_KEY: "your-wireguard-server-public-key"
  WG_PRESHARED_KEY: "optional-preshared-key"
  SSH_PRIVATE_KEY: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    your-ssh-private-key-content
    -----END OPENSSH PRIVATE KEY-----
  SSH_HOST_KEY: "ssh-rsa AAAAB3NzaC1yc2EAAAA... your-host-key"
```

### ベストプラクティス

1. **強力なキーを使用**: 適切な長さの SSH と WireGuard キーを生成する
2. **事前共有キーを有効にする**: 追加のセキュリティのために WireGuard 事前共有キーを使用する
3. **ホストキーを検証**: MITM 攻撃を防ぐため、常に SSH ホストキーを提供する
4. **許可 IP を制限**: WireGuard の許可 IP を必要なサブネットのみに設定する
5. **定期的なキーローテーション**: セキュリティ向上のため定期的にキーを更新する

## 前提条件

- 適切に設定され、稼働している WireGuard サーバー
- VPN ネットワーク内でアクセス可能な SSH サーバー
- WireGuard と SSH トラフィックを許可する適切なファイアウォールルール
- 有効な SSH と WireGuard キーペア

## ワークフローの例

```yaml
name: 本番環境へのデプロイ

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: コードをチェックアウト
      uses: actions/checkout@v3
      
    - name: アプリケーションをビルド
      run: |
        # ここにビルドステップを記述
        npm install
        npm run build
        tar -czf app.tar.gz dist/
        
    - name: WireGuard VPN 経由でデプロイ
      uses: book000/ssh-over-wireguard@v1
      with:
        # WireGuard VPN 設定
        wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
        wireguard-address: "10.0.0.2/24"
        wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
        wireguard-preshared-key: ${{ secrets.WG_PRESHARED_KEY }}
        wireguard-endpoint: "prod-server.example.com:51820"
        wireguard-allowed-ips: "10.0.0.0/24"
        
        # SSH 設定
        ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
        ssh-user: "deploy"
        ssh-hostname: "production"
        ssh-host-ip: "10.0.0.1"
        ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
        
        # アップロードとデプロイ
        operation: "scp"
        scp-source: "./app.tar.gz"
        scp-destination: "/opt/app/releases/"
        scp-direction: "upload"
        
    - name: 展開とサービス再起動
      uses: book000/ssh-over-wireguard@v1
      with:
        # ... 同じ VPN と SSH 設定 ...
        operation: "ssh"
        command: |
          cd /opt/app/releases
          tar -xzf app.tar.gz
          sudo systemctl restart myapp
          sudo systemctl status myapp
```

## トラブルシューティング

### よくある問題

1. **WireGuard のインストールに失敗**: これはコンテナ化環境でよく発生します。このアクションは、wireguard-tools のみをインストールすることで優雅に処理します。
2. **VPN 接続タイムアウト**: WireGuard サーバーが稼働していること、エンドポイントが正しいことを確認してください。
3. **SSH ホストキー検証の失敗**: SSH ホストキーが正しくフォーマットされ、サーバーと一致することを確認してください。
4. **権限が拒否される**: SSH プライベートキーのフォーマットが正しく、ユーザーが適切な権限を持っていることを確認してください。