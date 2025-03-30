# vscode AREPL for python
import nmap
import random

def run_nmap_scan(target, ports, scan_type="regular"):
    """指定されたポートに対してnmapスキャンを実施し、一時ファイルに保存"""
    nm = nmap.PortScanner()
    temp_oN = "temp_scan.oN"
    temp_gnmap = "temp_scan.gnmap"

    if scan_type == "full":
        nm.scan(hosts=target, arguments=f"-Pn -p- -oN {temp_oN} -oG {temp_gnmap}")
    elif scan_type == "service":
        ports_str = ",".join(map(str, ports))
        nm.scan(hosts=target, arguments=f"-Pn -sV -p{ports_str} -oN {temp_oN} -oG {temp_gnmap}")
    else:
        ports_str = ",".join(map(str, ports))
        nm.scan(hosts=target, arguments=f"-Pn -p{ports_str} -oN {temp_oN} -oG {temp_gnmap}")

    # 結果を追記
    with open(temp_oN, "r") as temp_file, open("scan_result.oN", "a") as result_file:
        result_file.write(temp_file.read())

    with open(temp_gnmap, "r") as temp_file, open("scan_result.gnmap", "a") as result_file:
        result_file.write(temp_file.read())

    return nm

def extract_open_ports(nm, target):
    """nmapのスキャン結果から開いているポートを抽出する"""
    open_ports = []
    if target in nm.all_hosts():
        for proto in nm[target].all_protocols():
            open_ports.extend(nm[target][proto].keys())
    return open_ports

def perform_service_scan(target, unique_ports):
    """サービススキャン (-sV) を実施し、結果と unique_ports を比較"""
    print("[*] Running initial service version scan on open ports...")
    
    # 初回サービススキャン
    if len(unique_ports) <= 1000:
        nm = run_nmap_scan(target, unique_ports, scan_type="service")
    else:
        random.shuffle(unique_ports)
        nm = None
        for i in range(0, len(unique_ports), 1000):
            sample_ports = unique_ports[i:i+1000]
            nm = run_nmap_scan(target, sample_ports, scan_type="service")

    # 初回スキャン結果を取得
    service_ports = extract_open_ports(nm, target)

    # unique_ports に含まれているのに service_ports で確認できなかったポート
    missing_ports = list(set(unique_ports) - set(service_ports))
    
    if missing_ports:
        print(f"[*] Re-scanning {len(missing_ports)} missing ports...")

    # 追加のスキャン (1000個ずつ実施)
    while missing_ports:
        sample_ports = missing_ports[:1000]  # 最初の1000個
        missing_ports = missing_ports[1000:]  # 残りのポート
        nm = run_nmap_scan(target, sample_ports, scan_type="service")

        # 再スキャン後の開いているポートを取得
        new_service_ports = extract_open_ports(nm, target)

        # まだ未確認のポートをリストアップ
        missing_ports = list(set(missing_ports) - set(new_service_ports))

    print("[*] Service version scan completed.")

def perform_port_scan(target):
    """ステップごとにポートスキャンを実施し、最終的なユニークな開放ポートを特定する"""

    # 1. 全ポートのスキャンを実施
    print("[*] Running initial full port scan...")
    full_port_list = list(range(1, 65536))
    nm = run_nmap_scan(target, full_port_list, scan_type="full")
    open_port_list = extract_open_ports(nm, target)
    print(f"[*] Initial open ports: {open_port_list}")

    # 2. 未開放ポートのスキャン（ランダム1000個ずつ）
    diff_list = list(set(full_port_list) - set(open_port_list))
    diff_list2 = []

    print("[*] Running second scan on remaining ports...")
    while diff_list:
        sample_ports = random.sample(diff_list, min(1000, len(diff_list)))
        nm = run_nmap_scan(target, sample_ports)
        new_open_ports = extract_open_ports(nm, target)
        diff_list2.extend(new_open_ports)
        diff_list = list(set(diff_list) - set(sample_ports))  # スキャン済みポートを除外
        print(f"[*] New open ports found: {new_open_ports}")

    # 3. 追加スキャン（diff_list2が空なら2回目と同じスキャンを繰り返す）
    diff_list3 = list(set(full_port_list) - set(open_port_list) - set(diff_list2))
    diff_list4 = []

    print("[*] Running third scan on remaining ports...")

    if not diff_list3:
        print("[*] No remaining ports, re-scanning diff_list2...")
        diff_list3 = diff_list2[:]  # diff_list2のポートを使って再スキャン

    while diff_list3:
        print(f"[*] Ports remaining: {len(diff_list3)}")
        sample_ports = random.sample(diff_list3, min(1000, len(diff_list3)))
        nm = run_nmap_scan(target, sample_ports)
        new_open_ports = extract_open_ports(nm, target)
        diff_list4.extend(new_open_ports)
        diff_list3 = list(set(diff_list3) - set(sample_ports))  # スキャン済みポートを除外
        print(f"[*] New open ports found: {new_open_ports}")

    # 4. ユニークなポートリストの作成
    unique_ports = list(set(open_port_list + diff_list2 + diff_list4))
    unique_ports.sort()

    print(f"[*] Final unique open ports: {unique_ports}")

    # 5. サービススキャンを実施
    perform_service_scan(target, unique_ports)

    return unique_ports

if __name__ == "__main__":
    target_ip = "192.168.31.141"  # スキャン対象のIPを指定
    result_ports = perform_port_scan(target_ip)
    print(f"Final open ports: {result_ports}")
