# SSH over WireGuard

WireGuard VPN経由でリモートサーバーに安全な暗号化接続を確立し、SSHコマンドの実行やSCPファイル転送を行うGitHub Actionです。

## 機能

- 🔒 **セキュアなVPN接続**: 安全な通信のためのWireGuard VPNトンネルを確立
- 🖥️ **SSHコマンド実行**: VPN経由でリモートサーバー上でコマンドを実行
- 📁 **SCPファイル転送**: SCPを使用してファイルを安全にアップロード・ダウンロード
- 🔍 **接続テスト**: VPN接続を確認するためのオプションのpingテスト
- 🛡️ **セキュリティ機能**: ホストキー検証、適切な権限処理
- 🧹 **自動クリーンアップ**: 実行後にVPNを切断し、SSHキーをクリーンアップ

## 使用方法

### 基本的なSSHコマンド実行

```yaml
- name: WireGuard VPN経由でSSHコマンドを実行
  uses: book000/ssh-over-wireguard@v1
  with:
    # WireGuard設定
    wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
    wireguard-address: "10.0.0.2/24"
    wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
    wireguard-endpoint: "your-server.com:51820"
    wireguard-allowed-ips: "10.0.0.0/24"
    
    # SSH設定
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
    ssh-user: "ubuntu"
    ssh-hostname: "myserver"
    ssh-host-ip: "10.0.0.1"
    ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
    
    # 操作設定
    operation: "ssh"
    command: "uptime && df -h"
```

### SCPファイルアップロード

```yaml
- name: WireGuard VPN経由でファイルをアップロード
  uses: book000/ssh-over-wireguard@v1
  with:
    # WireGuard設定
    wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
    wireguard-address: "10.0.0.2/24"
    wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
    wireguard-endpoint: "your-server.com:51820"
    wireguard-allowed-ips: "10.0.0.0/24"
    
    # SSH設定
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
    ssh-user: "ubuntu"
    ssh-hostname: "myserver"
    ssh-host-ip: "10.0.0.1"
    ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
    
    # SCP操作
    operation: "scp"
    scp-source: "./build/app.tar.gz"
    scp-destination: "/home/ubuntu/releases/"
    scp-direction: "upload"
```

### SCPファイルダウンロード

```yaml
- name: WireGuard VPN経由でファイルをダウンロード
  uses: book000/ssh-over-wireguard@v1
  with:
    # ... 上記と同じWireGuardとSSH設定 ...
    
    # SCP操作
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
| `ping-check` | SSH/SCP操作前の接続テスト（ping）を有効にする | いいえ | `true` |

### SSH操作

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `command` | リモートサーバーで実行するコマンド（operation=sshの場合のみ使用） | いいえ | `hostname && whoami && pwd` |

### SCP操作

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `scp-source` | SCP操作のソースパス（operation=scpの場合のみ使用） | はい* | - |
| `scp-destination` | SCP操作の宛先パス（operation=scpの場合のみ使用） | はい* | - |
| `scp-direction` | SCP方向: `upload` (ローカルからリモート) または `download` (リモートからローカル) | いいえ | `upload` |

*`operation=scp`の場合に必須

### WireGuard設定

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `wireguard-private-key` | WireGuardクライアントプライベートキー | はい | - |
| `wireguard-address` | WireGuardクライアントVPNアドレス（例: 10.0.0.2/24） | はい | - |
| `wireguard-peer-public-key` | WireGuardサーバーパブリックキー | はい | - |
| `wireguard-endpoint` | WireGuardサーバーエンドポイント（例: server.com:51820） | はい | - |
| `wireguard-allowed-ips` | WireGuardの許可IP（例: 10.0.0.0/24） | はい | - |
| `wireguard-preshared-key` | WireGuard事前共有キー（オプションのセキュリティ強化） | いいえ | - |
| `wireguard-dns` | DNSサーバーアドレス | いいえ | `1.1.1.1` |

### SSH設定

| パラメータ | 説明 | 必須 | デフォルト |
|-----------|-------------|----------|---------|
| `ssh-private-key` | 認証用SSHプライベートキー | はい | - |
| `ssh-user` | SSHユーザー名 | はい | - |
| `ssh-hostname` | SSH接続用ホスト名エイリアス | はい | - |
| `ssh-host-ip` | VPN内のSSHサーバーIPアドレス | はい | - |
| `ssh-host-key` | 検証用SSHサーバーホストキー | はい | - |
| `ssh-port` | SSHポート番号 | いいえ | `22` |

## セキュリティに関する考慮事項

### シークレット管理

すべての機密情報をGitHub Secretsとして保存してください：

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

1. **強力なキーを使用**: 適切な長さのSSHとWireGuardキーを生成する
2. **事前共有キーを有効にする**: 追加のセキュリティのためにWireGuard事前共有キーを使用する
3. **ホストキーを検証**: MITM攻撃を防ぐため、常にSSHホストキーを提供する
4. **許可IPを制限**: WireGuardの許可IPを必要なサブネットのみに設定する
5. **定期的なキーローテーション**: セキュリティ向上のため定期的にキーを更新する

## 前提条件

- 適切に設定され、稼働しているWireGuardサーバー
- VPNネットワーク内でアクセス可能なSSHサーバー
- WireGuardとSSHトラフィックを許可する適切なファイアウォールルール
- 有効なSSHとWireGuardキーペア

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
        
    - name: WireGuard VPN経由でデプロイ
      uses: book000/ssh-over-wireguard@v1
      with:
        # WireGuard VPN設定
        wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
        wireguard-address: "10.0.0.2/24"
        wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
        wireguard-preshared-key: ${{ secrets.WG_PRESHARED_KEY }}
        wireguard-endpoint: "prod-server.example.com:51820"
        wireguard-allowed-ips: "10.0.0.0/24"
        
        # SSH設定
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
        # ... 同じVPNとSSH設定 ...
        operation: "ssh"
        command: |
          cd /opt/app/releases
          tar -xzf app.tar.gz
          sudo systemctl restart myapp
          sudo systemctl status myapp
```

## トラブルシューティング

### よくある問題

1. **WireGuardのインストールに失敗**: これはコンテナ化環境でよく発生します。このアクションは、wireguard-toolsのみをインストールすることで優雅に処理します。

2. **VPN接続タイムアウト**: WireGuardサーバーが稼働していること、エンドポイントが正しいことを確認してください。

3. **SSHホストキー検証の失敗**: SSHホストキーが正しくフォーマットされ、サーバーと一致することを確認してください。

4. **権限が拒否される**: SSHプライベートキーのフォーマットが正しく、ユーザーが適切な権限を持っていることを確認してください。

## ライセンス

このプロジェクトはMITライセンスの下で利用可能です。詳細についてはLICENSEファイルをご覧ください。

## 貢献

貢献を歓迎します！お気軽にプルリクエストを送信してください。

## 作者

[Tomachi](https://github.com/book000)によって作成されました