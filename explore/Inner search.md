## check shell
`whoami` or `echo %USERPROFILE%`
## encrpt txt by xml
`powershell ‑c "$credential = import‑clixml ‑path C:\Data\Users\app\iot‑admin.xml;$credential.GetNetworkCredential().password"`
