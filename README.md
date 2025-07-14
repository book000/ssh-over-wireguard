# SSH over WireGuard

A GitHub Action that establishes secure encrypted connection to remote servers via WireGuard VPN and executes SSH commands or SCP file transfers.

## Features

- 🔒 **Secure VPN Connection**: Establishes WireGuard VPN tunnel for secure communication
- 🖥️ **SSH Command Execution**: Execute commands on remote servers through the VPN
- 📁 **SCP File Transfer**: Upload and download files securely via SCP
- 🔍 **Connectivity Testing**: Optional ping test to verify VPN connectivity
- 🛡️ **Security Features**: Host key verification, proper permission handling
- 🧹 **Automatic Cleanup**: Tears down VPN and cleans up SSH keys after execution

## Usage

### Basic SSH Command Execution

```yaml
- name: Execute SSH command through WireGuard VPN
  uses: book000/ssh-over-wireguard@v1
  with:
    # WireGuard Configuration
    wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
    wireguard-address: "10.0.0.2/24"
    wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
    wireguard-endpoint: "your-server.com:51820"
    wireguard-allowed-ips: "10.0.0.0/24"
    
    # SSH Configuration
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
    ssh-user: "ubuntu"
    ssh-hostname: "myserver"
    ssh-host-ip: "10.0.0.1"
    ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
    
    # Operation
    operation: "ssh"
    command: "uptime && df -h"
```

### SCP File Upload

```yaml
- name: Upload file through WireGuard VPN
  uses: book000/ssh-over-wireguard@v1
  with:
    # WireGuard Configuration
    wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
    wireguard-address: "10.0.0.2/24"
    wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
    wireguard-endpoint: "your-server.com:51820"
    wireguard-allowed-ips: "10.0.0.0/24"
    
    # SSH Configuration
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
    ssh-user: "ubuntu"
    ssh-hostname: "myserver"
    ssh-host-ip: "10.0.0.1"
    ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
    
    # SCP Operation
    operation: "scp"
    scp-source: "./build/app.tar.gz"
    scp-destination: "/home/ubuntu/releases/"
    scp-direction: "upload"
```

### SCP File Download

```yaml
- name: Download file through WireGuard VPN
  uses: book000/ssh-over-wireguard@v1
  with:
    # ... WireGuard and SSH configuration same as above ...
    
    # SCP Operation
    operation: "scp"
    scp-source: "/var/log/application.log"
    scp-destination: "./logs/"
    scp-direction: "download"
```

## Input Parameters

### Operation Settings

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `operation` | Operation type: `ssh` (execute command) or `scp` (file transfer) | No | `ssh` |
| `ping-check` | Enable ping connectivity test before SSH/SCP operations | No | `true` |

### SSH Operation

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `command` | Command to execute on the remote server (only used when operation=ssh) | No | `hostname && whoami && pwd` |

### SCP Operation

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `scp-source` | Source path for SCP operation (only used when operation=scp) | Yes* | - |
| `scp-destination` | Destination path for SCP operation (only used when operation=scp) | Yes* | - |
| `scp-direction` | SCP direction: `upload` (local to remote) or `download` (remote to local) | No | `upload` |

*Required when `operation=scp`

### WireGuard Configuration

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `wireguard-private-key` | WireGuard client private key | Yes | - |
| `wireguard-address` | WireGuard client VPN address (e.g., 10.0.0.2/24) | Yes | - |
| `wireguard-peer-public-key` | WireGuard server public key | Yes | - |
| `wireguard-endpoint` | WireGuard server endpoint (e.g., server.com:51820) | Yes | - |
| `wireguard-allowed-ips` | Allowed IPs for WireGuard (e.g., 10.0.0.0/24) | Yes | - |
| `wireguard-preshared-key` | WireGuard preshared key (optional security enhancement) | No | - |
| `wireguard-dns` | DNS server address | No | `1.1.1.1` |

### SSH Configuration

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `ssh-private-key` | SSH private key for authentication | Yes | - |
| `ssh-user` | SSH username | Yes | - |
| `ssh-hostname` | SSH hostname alias for connection | Yes | - |
| `ssh-host-ip` | SSH server IP address within VPN | Yes | - |
| `ssh-host-key` | SSH server host key for verification | Yes | - |
| `ssh-port` | SSH port number | No | `22` |

## Security Considerations

### Secrets Management

Store all sensitive information as GitHub Secrets:

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

### Best Practices

1. **Use strong keys**: Generate SSH and WireGuard keys with appropriate lengths
2. **Enable preshared keys**: Use WireGuard preshared keys for additional security
3. **Verify host keys**: Always provide the SSH host key to prevent MITM attacks
4. **Limit allowed IPs**: Configure WireGuard allowed IPs to only necessary subnets
5. **Regular key rotation**: Rotate keys periodically for better security

## Prerequisites

- WireGuard server properly configured and running
- SSH server accessible within the VPN network
- Proper firewall rules allowing WireGuard and SSH traffic
- Valid SSH and WireGuard key pairs

## Example Workflow

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Build application
      run: |
        # Your build steps here
        npm install
        npm run build
        tar -czf app.tar.gz dist/
        
    - name: Deploy through WireGuard VPN
      uses: book000/ssh-over-wireguard@v1
      with:
        # WireGuard VPN configuration
        wireguard-private-key: ${{ secrets.WG_PRIVATE_KEY }}
        wireguard-address: "10.0.0.2/24"
        wireguard-peer-public-key: ${{ secrets.WG_SERVER_PUBLIC_KEY }}
        wireguard-preshared-key: ${{ secrets.WG_PRESHARED_KEY }}
        wireguard-endpoint: "prod-server.example.com:51820"
        wireguard-allowed-ips: "10.0.0.0/24"
        
        # SSH configuration
        ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
        ssh-user: "deploy"
        ssh-hostname: "production"
        ssh-host-ip: "10.0.0.1"
        ssh-host-key: ${{ secrets.SSH_HOST_KEY }}
        
        # Upload and deploy
        operation: "scp"
        scp-source: "./app.tar.gz"
        scp-destination: "/opt/app/releases/"
        scp-direction: "upload"
        
    - name: Extract and restart service
      uses: book000/ssh-over-wireguard@v1
      with:
        # ... same VPN and SSH config ...
        operation: "ssh"
        command: |
          cd /opt/app/releases
          tar -xzf app.tar.gz
          sudo systemctl restart myapp
          sudo systemctl status myapp
```

## Troubleshooting

### Common Issues

1. **WireGuard installation fails**: This is common in containerized environments. The action handles this gracefully by installing wireguard-tools only.
2. **VPN connection timeout**: Check that the WireGuard server is running and the endpoint is correct.
3. **SSH host key verification failed**: Ensure the SSH host key is correctly formatted and matches the server.
4. **Permission denied**: Verify that the SSH private key format is correct and the user has appropriate permissions.