## Search
`cat /etc/knockd.conf`
- exsample
  ```
  [options]
   logfile = /var/log/knockd.log
   interface = ens160

  [openSSH]
   sequence = 571, 290, 911 
   seq_timeout = 5
   start_command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
   tcpflags = syn

  [closeSSH]
   sequence = 911,290,571
   seq_timeout = 5
   start_command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
   tcpflags = syn
  ```
## execute (by kali)
```
for i in 571 290 911; do
nmap -Pn --host-timeout 100 --max-retries 0 -p $i 10.10.10.43 >/dev/null
 done; ssh -i ./next_key amrois@10.10.10.43
```
