## gobuster
#### ディレクトリの列挙
`gobuster dir -u http://test.com -w /usr/share/wordlists/dirb/common.txt -k`  
`gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt -x php,html -t 20 -k`  
`sudo gobuster dir -u http://10.10.10.56/ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -o scan/dir_scan.txt -k`
- dir: ディレクトリ列挙モード
- u: 対象のURL
- w: 使用するワードリスト
- x：ファイル拡張子を指定（例：.php、.html）。
- t：スレッド数を指定して高速化。(最大20)
- o：結果をファイルに出力。
- 
#### サブドメインの列挙
`gobuster dns -d example.com -w /usr/share/wordlists/subdomains.txt`
- dns: DNS列挙モード
- d: ドメイン名
#### VHOST探索
- 補足
  - 仮想ホストの列挙
    - これにより、複数のドメインが同じIPアドレスにホストされているかどうか
`gobuster vhost -u http://example.com -w /usr/share/wordlists/vhosts.txt`
#### Amazon S3バケットの探索
`gobuster s3 -w /usr/share/wordlists/s3-buckets.txt`
