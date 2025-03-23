import nmap
import logging
from datetime import datetime
import multiprocessing

# ログの設定
log_filename = f"nmap_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# スキャン対象のドメインリスト
domains = ["sample.com", "www.sample.com"]

# nmapスキャンを実行する関数
def scan_domain(domain):
    nm = nmap.PortScanner()
    try:
        logging.info(f"Starting Nmap scan for {domain}")
        print(f"[INFO] Scanning {domain} with Nmap...")

        # Nmapスキャン実行（80, 443ポートのみスキャン）
        nm.scan(hosts=domain, arguments="-p 80,443 -T4")

        # スキャン結果の取得
        if domain in nm.all_hosts():
            open_ports = []
            for proto in nm[domain].all_protocols():
                ports = nm[domain][proto].keys()
                for port in ports:
                    state = nm[domain][proto][port]['state']
                    open_ports.append(f"{port}/{proto} ({state})")

            result_str = f"[SUCCESS] {domain} scan completed. Open ports: {', '.join(open_ports)}"
            logging.info(result_str)
            print(result_str)
        else:
            logging.warning(f"[WARNING] {domain} did not respond or is unreachable")
            print(f"[WARNING] {domain} did not respond or is unreachable")

    except Exception as e:
        logging.exception(f"Exception while scanning {domain}")
        print(f"[EXCEPTION] Error scanning {domain}: {e}")

if __name__ == "__main__":
    logging.info("Starting all Nmap scans")
    with multiprocessing.Pool(processes=len(domains)) as pool:
        pool.map(scan_domain, domains)

    logging.info("All Nmap scans completed")
    print("[INFO] All Nmap scans completed.")
