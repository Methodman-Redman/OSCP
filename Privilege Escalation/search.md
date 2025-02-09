`echo "\n----- Check SUID -----\n";find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null;echo "\n----- Check crontab -----\n" ;cat /etc/crontab;echo "\n----- Check sh faile -----\n" find / -iname ".sh" 2>/dev/null`
`sudo -l`
`pspy64`
