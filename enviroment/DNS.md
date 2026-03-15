## 概要
- PowerDNS（Docker版）を使用してDNSローテーション環境を構築するための全ファイルを整理します。

#### ディレクトリ構造
- VM上の作業ディレクトリを作成し、以下の構造でファイルを配置

```
Plaintext
lab-dns/
├── docker-compose.yml
├── pdns.conf
└── zones/
    ├── named.conf
    └── test.com.zone
```

## 1. docker-compose.yml
- PowerDNSの本体を動かす設定です。
```
services:
  pdns:
    image: powerdns/pdns-auth-48
    container_name: pdns-server
    restart: always
    ports:
      - "53:53/udp"
      - "53:53/tcp"
    volumes:
      - ./pdns.conf:/etc/powerdns/pdns.conf:ro
      - ./zones:/zones:ro
    environment:
      - TZ=Asia/Tokyo
```

## 2. pdns.conf
- PowerDNSの動作エンジン（BINDバックエンド）とLUAレコードを有効化する設定です。
```
# 基本設定
launch=bind
bind-config=/zones/named.conf
enable-lua-records=yes

# ネットワーク設定
local-address=0.0.0.0
local-port=53

# ログ設定 (デバッグ用に詳細出力)
loglevel=6
log-dns-queries=yes
log-dns-details=yes
3. zones/named.conf
どのドメイン（ゾーン）を管理するかを定義します。

Plaintext
zone "test.com" {
    type master;
    file "/zones/test.com.zone";
};
```
## 4. zones/test.com.zone
- ここが肝心のローテーション設定です。IPアドレスはご自身の環境（Redirector VMのIP）に合わせて適宜書き換えてください。
```
$ORIGIN test.com.
$TTL 60
@   IN  SOA ns1.test.com. admin.test.com. (
        2026031501 ; シリアル番号
        3600       ; Refresh
        1800       ; Retry
        604800     ; Expire
        60 )       ; Minimum TTL

@   IN  NS  ns1.test.com.

; DNSサーバー自身のAレコード
ns1 IN  A   192.168.56.10

; --- 攻撃インフラ模倣設定 ---
; クエリごとに1つのIPをランダム(実質ラウンドロビン風)に返す
www IN  LUA A "pickrandom({'192.168.56.21','192.168.56.22','192.168.56.23','192.168.56.24'})"
```
## 環境構築と確認の手順
#### ステップ1：53番ポートの解放（重要）
- Ubuntu等のVMでは標準DNSサービスがポートを占有しているため、必ず停止させてください。
- `sudo systemctl stop systemd-resolved`
- `sudo systemctl disable systemd-resolved`
- `sudo systemctl mask systemd-resolved`
#### ステップ2：コンテナ起動
- `docker-compose up -d`
#### ステップ3：動作確認
- 別の端末、あるいは同じVM内から dig コマンドを連続で叩いて確認します。
- `for i in {1..5}; do dig +short @localhost www.test.com; done`

## 復旧
- `sudo systemctl unmask systemd-resolved`
- `sudo systemctl start systemd-resolved`
- `sudo systemctl enable systemd-resolved`

## おまけ
#### 1. Docker環境のセットアップ
- まずはDocker本体と、新しい方のCompose V2（プラグイン版）をインストールします。
- パッケージリストの更新
  - `sudo apt update`
- 必要な依存パッケージのインストール
  - `sudo apt install -y ca-certificates curl gnupg`
- Docker公式のGPGキーを追加
```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
# リポジトリの設定
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# インストール（docker-compose-plugin が新しい方です）
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
#### 2. 権限の設定（sudoなしで実行できるようにする）
- 毎回 sudo を打つのは手間ですし、ラボ環境では不便なので、自分のユーザーを docker グループに追加します。
- `sudo usermod -aG docker $USER`
- 注意: この設定を反映させるには、一度 ログアウトして再ログイン するか、`newgrp docker` と打つ必要があります。
#### 3. 起動確認
- インストールができたら、ハイフンなしのコマンドでバージョンを確認してみてください。
- `docker compose version`
