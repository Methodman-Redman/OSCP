import subprocess
import multiprocessing

def main():
    target_dict = {}
    with open('sample.txt', 'r') as f:
        #print(f.read())
        for target_org in f:
            key,value = target_org.split()
            target_dict[key] = value
            #print(i)
    return target_dict

# スキャン対象のドメインリスト
domains = ["sample.com", "www.sample.com"]

# 実行するスキャンコマンド（例：dirsearch を使う場合）
def scan_domain(domain):
    try:
        cmd = f"dirsearch -u http://{domain} -e php,html,js"
        print(f"[INFO] Scanning {domain} ...")
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {domain} scan completed")
        else:
            print(f"[ERROR] {domain} scan failed: {result.stderr}")

    except Exception as e:
        print(f"[EXCEPTION] Error scanning {domain}: {e}")

if __name__ == "__main__":
    with multiprocessing.Pool(processes=len(domains)) as pool:
        pool.map(scan_domain, domains)

    print("[INFO] All scans completed.")

```
multiprocessing.Pool を使用
各ドメインのスキャンを 独立したプロセス で実行するため、どれか1つがクラッシュしても他のプロセスには影響なし。
subprocess.run() で外部スキャンツールを実行
例えば dirsearch のようなツールを使用。
stderr をキャッチして、エラーハンドリングも可能。
全プロセス終了後にメッセージを出力
print("[INFO] All scans completed.") で、全てのスキャンが終了したことを確認。
```
