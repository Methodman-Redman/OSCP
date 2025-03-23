import subprocess
import multiprocessing
import logging
from datetime import datetime

# ログの設定
log_filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# スキャン対象のドメインリスト
domains = ["sample.com", "www.sample.com"]

# スキャンを実行する関数
def scan_domain(domain):
    try:
        cmd = f"dirsearch -u http://{domain} -e php,html,js"
        logging.info(f"Starting scan for {domain}")
        print(f"[INFO] Scanning {domain} ...")

        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            logging.info(f"Scan completed successfully for {domain}")
            print(f"[SUCCESS] {domain} scan completed")
        else:
            logging.error(f"Scan failed for {domain}: {result.stderr.strip()}")
            print(f"[ERROR] {domain} scan failed: {result.stderr.strip()}")

    except Exception as e:
        logging.exception(f"Exception while scanning {domain}")
        print(f"[EXCEPTION] Error scanning {domain}: {e}")

if __name__ == "__main__":
    logging.info("Starting all scans")
    with multiprocessing.Pool(processes=len(domains)) as pool:
        pool.map(scan_domain, domains)

    logging.info("All scans completed")
    print("[INFO] All scans completed.")

'''
ログファイルを保存
scan_results_YYYYMMDD_HHMMSS.log という形式でログをファイルに記録。
logging.basicConfig() でログの設定を行い、INFO レベル以上のメッセージを記録。
スキャンの開始・成功・失敗をログに記録
logging.info() でスキャンの開始・成功を記録。
logging.error() でスキャン失敗時のエラーを記録（stderr を保存）。
logging.exception() で予期しない例外も記録。
ターミナルとログの両方に出力
print() でリアルタイムに確認可能。
logging でファイルに保存し、後から分析可能。

2025-03-23 15:30:45 [INFO] Starting all scans
2025-03-23 15:30:45 [INFO] Starting scan for sample.com
2025-03-23 15:30:50 [INFO] Scan completed successfully for sample.com
2025-03-23 15:30:50 [INFO] Starting scan for www.sample.com
2025-03-23 15:31:00 [ERROR] Scan failed for www.sample.com: Connection timed out
2025-03-23 15:31:00 [INFO] All scans completed
'''
