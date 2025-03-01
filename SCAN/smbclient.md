## Share Enumlation
`smbclient -L //10.10.11.35 -N`
## Access
- passwordとuser名を同時に指定する場合
`smbclient //cicada.htb/DEV -U 'david.orelious%aRt$Lp#7t*VQ!3'`
- user名のみの場合
`smbclient //cicada.htb/DEV -U 'david.orelious`
