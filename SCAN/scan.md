## script
```
#!/bin/bash

TARGET="$1"
MAX_RETRIES=10
COUNT=0

# Function to check if DNS resolution succeeds
resolve_domain() {
    [[ -n "$(dig +short "$TARGET")" ]]
}

# Retry loop
while true; do
    if resolve_domain; then
        echo "[OK] DNS resolution successful: $TARGET"
        echo "[INFO] Running nmap with FQDN: nmap $TARGET"
        nmap "$TARGET"
        break
    else
        COUNT=$((COUNT + 1))
        echo "[WARN] DNS resolution failed (attempt $COUNT): $TARGET"

        if [[ "$COUNT" -ge "$MAX_RETRIES" ]]; then
            echo "[ERROR] DNS resolution failed $MAX_RETRIES times. Exiting."
            exit 1
        fi

        sleep 2
    fi
done

```

## oneliner
```
TARGET=example.com; COUNT=0; while true; do DIG_RESULT=$(dig +short "$TARGET"); if [[ -n "$DIG_RESULT" ]]; then echo "[OK] DNS resolution successful: $TARGET"; echo "[INFO] Running nmap with FQDN: nmap $TARGET"; nmap "$TARGET"; break; else COUNT=$((COUNT+1)); echo "[WARN] DNS resolution failed (attempt $COUNT): $TARGET"; [[ $COUNT -ge 10 ]] && echo "[ERROR] DNS resolution failed 10 times." && break; sleep 2; fi; done

```
