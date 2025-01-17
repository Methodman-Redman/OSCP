## Normal
`sudo nmap -o -Pn -p- -sC -sV --min-rate=1000 -T4 10.10.10.204`  
## vuln
`sudo nmap --script vuln 10.0.2.8`
## mysql
`nmap --script=mysql-enum 10.10.10.1`
## smb
`nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.10.1`
## NFS
`nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.10.1`
## help
`nmap --script-help <script-name>`
