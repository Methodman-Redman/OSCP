# dshell
- `git clone https://github.com/USArmyResearchLab/Dshell.git`
- `sudo apt install pyenv`
```
sudo apt update && sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git libpcap-dev
```

```
# zshの設定ファイルにpyenvのパスを追加
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 設定を現在のターミナルに即時反映
source ~/.zshrc
```

- `pyenv install 3.11.9`
- `pyenv local 3.11.9`
- `python -V`

```
# 新しい仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate

# 仮想環境内の pip と setuptools を最新にしておく
pip install --upgrade pip setuptools wheel
```

```
cd /home/kali/Lesson/test1/Dshell
pip install .
pip install netifaces
```
- `dshell -h`

# passive
1. 依存インストール
- `sudo apt update`
```
sudo apt install -y \
  git \
  build-essential \
  autoconf \
  automake \
  libtool \
  pkg-config \
  libpcap-dev \
  libldns-dev \
  libjansson-dev \
  zlib1g-dev
```
2. clone
- `cd ~/Lesson`
- `git clone https://github.com/gamelinux/passivedns.git`
- `cd passivedns`
2. autotools生成
- `autoreconf --install`
2. modern GCC対応パッチ
- `cd src`
- signal handler 宣言修正:
```
sed -i 's/^void game_over ();/void game_over(int sig);/' passivedns.c
sed -i 's/^void print_pdns_stats();/void print_pdns_stats(int sig);/' passivedns.c
# signal handler 定義修正:
sed -i 's/^void sig_alarm_handler()/void sig_alarm_handler(int sig)/' passivedns.c
sed -i 's/^void sig_hup_handler()/void sig_hup_handler(int sig)/' passivedns.c
sed -i 's/^void game_over()/void game_over(int sig)/' passivedns.c
sed -i 's/^void print_pdns_stats()/void print_pdns_stats(int sig)/' passivedns.c
# dns側修正:
sed -i 's/^void expire_all_dns_records()/void expire_all_dns_records(int sig)/' dns.h
sed -i 's/^void expire_all_dns_records()/void expire_all_dns_records(int sig)/' dns.c
# 古い関数呼び出し修正:
sed -i 's/expire_all_dns_records();/expire_all_dns_records(0);/' passivedns.c
sed -i 's/print_pdns_stats();/print_pdns_stats(0);/' passivedns.c
sed -i 's/game_over();/game_over(0);/g' passivedns.c
```
5. build
- `cd ..`
- `make clean`
- `make -j$(nproc)`
5. install
- `sudo make install`
5. 確認
- `passivedns -h`
