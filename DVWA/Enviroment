## Ready to Docker
- 古いバージョンをアンイストール
  - `sudo apt remove docker docker-engine docker.io containerd runc`
- 必須ソフトウェアインストール
  - `sudo apt update && sudo apt install -y ca-certificates curl gnupg lsb-release`
- GPGキー取得
  - `sudo mkdir -m 0755 -p /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`
- リポジトリの設定
  - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
- Docker Engineインストール
  - `sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

## docker-compose.yml
```
version: '3.8'

services:
  # データベースサービス (例: MariaDB)
  db:
    image: mariadb:10.11
    # コンテナが再起動された時のポリシーを定義
    restart: always
    environment:
      # DVWAが使用するデータベース名
      MYSQL_DATABASE: 'dvwa'
      # DVWAが使用するユーザー名
      MYSQL_USER: 'dvwa'
      # DVWAが使用するパスワード
      MYSQL_PASSWORD: 'password'
      # MySQL/MariaDBのrootパスワード
      MYSQL_ROOT_PASSWORD: 'rootpassword'
    # データを永続化するためのボリューム
    volumes:
      - db-data:/var/lib/mysql

  # Webアプリケーションサービス (DVWA)
  web:
    # 適切なDVWAイメージを指定
    image: vulnerables/web-dvwa
    # データベースサービスが完全に起動するのを待機
    depends_on:
      - db
    # Webサーバーのポートをホストマシンに公開
    ports:
      - "3000:80"
    environment:
      # DVWAのデータベース接続設定 (dbサービスに接続)
      MYSQL_DB: 'dvwa'
      MYSQL_USER: 'dvwa'
      MYSQL_PASSWORD: 'password'
      MYSQL_HOST: 'db' # データベースサービスのホスト名はサービス名 'db' になります

# 永続化用のボリューム定義
volumes:
  db-data:
```
