## smb by kali
`vi /etc/samba/smb.conf`
```
[Public]
   path = /tmp/Public
   writable = yes
   guest ok = yes
   guest only = yes
   create mode = 0777
   directory mode = 077
   force user = nobody
```
```
mkdir /tmp/Public
chmod 777 /tmp/Public
service smbd restart
```
