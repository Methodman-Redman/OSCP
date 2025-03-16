```py
import os
import sys
import subprocess
import webbrowser
import nmap
import time
import re
import argparse
import requests
import json
## For Color only
from term_printer import Color, cprint


parser = argparse.ArgumentParser(description='This Script is Original Auto Nmap Script')
parser.add_argument('-t','--Target',default='test.com')
parser.add_argument('-i','--Ip',default='192.168.31.141')
args = parser.parse_args()

target = args.Target
domain = args.Target
dns_server = '@' + domain
ip_add = args.Ip

hosts_file = "/etc/hosts"

def Normal_nmap(target):
    options = "-sV -sC -Pn -O -T5 -oN test_on -oG test_og"
    nm = nmap.PortScanner()
    nm.scan(target, arguments=options)
    port_arry = []
    common_name = ""
    #firefox_dict = {}
    firefox_arry = []
    for host in nm.all_hosts():
        print("Host: ", host)
        for proto in nm[host].all_protocols():
            print("Protocol: ", proto)
            ports = nm[host][proto].keys()
            for port in ports:
                firefox_dict = {}
                #print("Port: ", port, "State: ", nm[host][proto][port]['state'])
                print("service:", nm[host][proto][port]['product'] , "Version",nm[host][proto][port]['version'])
                try:
                    common_name = str(nm[host][proto][port]['script'])
                    pattern = r'\b([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)?\.htb)\b'
                    matches = re.findall(pattern, common_name)
                    if matches:
                        with open(hosts_file, "r") as f:
                            existing_hosts = f.read()
                        new_entries = []
                        dir_entries = []
                        for domain in matches:
                            if domain == target:
                                pass
                            else:
                                entry = f"{ip_add} {domain}"
                                new_entries.append(entry)
                                dir_entries.append(domain)
                        if new_entries:
                            with open(hosts_file, "a") as f:
                                f.write("\n" + "\n".join(new_entries) + "\n")
                            cprint("Updated /etc/hosts with new domains.",attrs=[Color.BG_BRIGHT_BLUE])
                            for search_domain in dir_entries:
                                tmp_port = str(port)
                                Change_URL(search_domain,tmp_port)
                                firefox_dict.update({search_domain:tmp_port})
                                firefox_arry.append(firefox_dict)
                        else:
                            print("No new domains to add.") 
                except KeyError:
                    pass
                brower_tmp = str(port)
                http_tmp = str(nm[host][proto][port]['name'])
                if brower_tmp == "80" or brower_tmp == "443" or http_tmp == "http":
                    Change_URL(target,brower_tmp)
                    firefox_dict.update({target:brower_tmp})
                    firefox_arry.append(firefox_dict)
                service_name = str(nm[host][proto][port]['product'])
                try:
                    service_name = IIS_Search(service_name)
                    #service_name = service_name.split()[0]
                except IndexError:
                    pass
                tmp_version = nm[host][proto][port]['version']
                port = str(port)
                if port == str(53):
                    Dns_Check()
                #tmp_version = tmp_version[:4]
                vuln_word = service_name + " " + tmp_version
                if "Windows" not in vuln_word and vuln_word != "Simple" and vuln_word.strip() != "":
                    print(f'Check :{vuln_word}')
                    command = f'searchsploit {vuln_word}'
                    Run_Command(command)
                else:
                    pass
                # --script=vuln port
                port_arry.append(port)
                if brower_tmp == "445":
                    SMB_Search(target)
                if brower_tmp == "389":
                    LDAP_Search(target)
        os_data = nm[host]['osmatch']
        for oss in os_data:
            name = oss['name']
            cpe_list = []
            for os in oss['osclass']:  
                if 'cpe' in os:  
                    for cpe in os['cpe']:
                        cpe_num = cpe.replace('/a','2.3:o')
                        cpe_list.append(cpe_num)  
            print(f"Name: {name}")
            print("CPEs:", ", ".join(cpe_list))
            # If doing CVE search , don't get nvd api 
            for cpe_string in cpe_list:
                cpe_search_word = convert_cpe_to_name(cpe_string)
                print(f"OS_CPE_TEST:{cpe_search_word}")
                command = f'searchsploit "{cpe_search_word}" | grep "Privilege Escalation"'
                #Run_Command(command)
            print("-" * 40)
        for port in ports:
            #print("{}:{}".format(port,nm[host].tcp(port))) #2
            print(nm[host]['tcp'][port]['cpe'])
            cpe_num = nm[host]['tcp'][port]['cpe']
            cpe_num = cpe_num.replace('/a','2.3:a')
            if cpe_num:
                # print(cpe_num)
                if cpe_num != 'cpe:/o:microsoft:windows':
                    CVE_search(cpe_num)
                else:
                    pass
            else:
                print("CPE None")
    port_arry = str(port_arry)
    port_arry = port_arry[1:-1]
    port_arry = port_arry.replace(" ","")
    time.sleep(1)
    command = f'nmap --script=vuln -Pn -T5 -p {port_arry} {target}'
    Run_Command(command)
    return firefox_arry

def Hosts_update(new_entries):
    with open(hosts_file, "a") as f:
        f.write("\n" + ip_add + "     " + new_entries)
    print("Updated /etc/hosts with new domains.")

def Dns_Check():
    # Make dig Command
    command = ['dig', 'axfr', target, dns_server]
    result = subprocess.run(command, capture_output=True, text=True)

    output = result.stdout

    # Get ARecord by re
    a_record_pattern = re.compile(r'(\S+)\s+\d+\s+IN\s+A\s+(\d+\.\d+\.\d+\.\d+)')

    # Search Arecord
    print("A Record:")
    for match in a_record_pattern.finditer(output):
        hostname, ip_address = match.groups()
        print(f"{hostname} -> {ip_address}")
        dns_test = hostname[:-1]
        check_dns = dns_test[0:2]
        if check_dns == 'ns':
            print("This is DNS Server")
        elif dns_test == target:
            pass
        else:
            print("Check This DNS")
            Hosts_update(dns_test)


def IIS_Search(service_name):
    match = re.search(r'Microsoft\s+(\S+)', service_name)
    if match:
        service_name = match.group(1)
        return service_name
    else:
        service_name = service_name.split()[0]
        return service_name

def CVE_search(cpe_num):
    NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    #CPE_NAME = "cpe:2.3:o:canonical:ubuntu_linux:20.04"
    #print(f"This is cpe_num: {cpe_num}")
    # API request query
    if cpe_num == "cpe:/o:microsoft:windows":
        return
    params = {
        "cpeName": cpe_num,
        "cvssV3Severity": "HIGH",  # SeverityがHighのものを取得
    } 
    time.sleep(1)
    response = requests.get(NVD_API_URL, params=params)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        data = response.json()

        # 必要な情報を抽出（CVE番号 & CVSSスコア）
        vulnerabilities = data.get("vulnerabilities", [])
        results = []
        for item in vulnerabilities:
            cve_id = item["cve"]["id"]
            # CVSS v3.1のベーススコアを取得（存在しない場合はNone）
            cvss_score = (
                item["cve"]
                .get("metrics", {})
                .get("cvssMetricV31", [{}])[0]
                .get("cvssData", {})
                .get("baseScore", None)
            )
            results.append({"CVE": cve_id, "CVSS": cvss_score})

        # 結果をJSONで出力
        #print(json.dumps(results, indent=2))
        #print(results)
        for cve in results:
            #print(cve)
            cve_get = cve.get("CVE")
            cprint(cve_get,attrs=[Color.BG_BRIGHT_BLUE])
            cve_num = cve.get("CVE")
            POC_search(cve_num)
    else:
        #print(f"Error: API request failed with status code {response.status_code}")
        cprint(f"Not found CVE : {cpe_num} ",attrs=[Color.RED])

def POC_search(cve_num):
    POC_IN_API_URL = "https://poc-in-github.motikan2010.net/api/v1"
    #CPE_NAME = "cpe:2.3:o:canonical:ubuntu_linux:20.04"
    print(f"This is cve_num: {cve_num}")
    # API request query
    params = {"cve_id": cve_num} 
    response = requests.get(POC_IN_API_URL, params=params)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        data = response.json()
        poc_url = data.get("pocs", [])
        results = []
        if poc_url:
            #print(poc_url)
            for poc_sum in poc_url:
                #get_name = poc_sum.get('name')
                #print(poc_test)
                poc_url = poc_sum.get('html_url')
                cprint(poc_url,attrs=[Color.BG_BRIGHT_BLUE])
                poc_date = poc_sum.get('updated_at')
                cprint(poc_date,attrs=[Color.BG_BRIGHT_BLUE])
        else:
            cprint(f"POC NO data : {cve_num}",attrs=[Color.RED])

def convert_cpe_to_name(cpe_string):
    # CPE split : * 2
    parts = cpe_string.rsplit(':', 2)
    if len(parts) < 3:
        raise ValueError("Invalid CPE format")
    name_part = parts[-2].replace('_', ' ').replace(':', ' ')
    version_part = parts[-1]
    # Change small Word to Large Word
    name_part = name_part.capitalize()
    # 変換後の文字列を返す
    return f"{name_part} {version_part}"

def SMB_Search(target):
    cprint("Start SMB Search",attrs=[Color.BG_BLUE])
    command = f'smbclient -N -L \\\\{target}'
    #dir_result = os.system(command)
    Run_Command(command)
    command = f'nxc smb {target} -u "guest" -p "" -M coerce_plus'
    #brute_result = os.system(command)
    Run_Command(command)
# For ldap 389 other must flag?
def LDAP_Search(target):
    cprint("Start LDAP Search",attrs=[Color.BG_BLUE])
    command = f'nxc ldap {target} -u "guest" -p "" --active-users'
    print(command)
    #print(os.system(command))
    Run_Command(command)

def Open_Qterminal():
    # Start First qterminal
    subprocess.Popen(['qterminal'], stderr=subprocess.DEVNULL)
    time.sleep(1)  

def Run_Command(command):
    # New Terminal execute command
    subprocess.run(['xdotool', 'key', 'ctrl+shift+t'])
    time.sleep(0.5)
    subprocess.run(['xdotool', 'type', f'{command}'])
    subprocess.run(['xdotool', 'key', 'Return'])

def Change_URL(target,port):
    if port == "80":
        search_url = f"http://{target}"
        Directory_SCAN(search_url)
    elif port == "443":
        search_url = f"https://{target}"
        Directory_SCAN(search_url)
    elif port == "5985" or "5986":
        pass
    else:
        search_url = f"http://{target}:{port}"
        Directory_SCAN(search_url)
    

def Directory_SCAN(search_url):
    command = f'whatweb --aggression 3 -v {search_url}'
    Run_Command(command)
    command = f'gobuster dir -u {search_url} -w /usr/share/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt -k'
    Run_Command(command)

def Brower_Search(browser_search_arry):
    print(browser_search_arry)
    for domain_dict in browser_search_arry:
        for domain,port in domain_dict.items():
            if port == "80":
                search_url = f"http://{domain}"
                webbrowser.open(search_url)
            elif port == "443":
                search_url = f"https://{domain}"
                webbrowser.open(search_url)
            elif port == "389" or "5985" or "5986":
                pass
            else:
                search_url = f"http://{domain}:{port}"
                webbrowser.open(search_url)
            #cprint(f"This is DEBUG {search_url}",attrs=[Color.BG_RED])
    sys.exit()

if __name__ == "__main__":
    Open_Qterminal()
    #target = input("please ip : ")
    command = f'nmap -sV -Pn -F -T5 {target}'
    Run_Command(command)
    command = f'nmap -sV -Pn -T5 {target}'
    Run_Command(command)
    command = f'nmap -Pn -p- -T5  {target}'
    Run_Command(command)
    browser_search_arry = Normal_nmap(target)
    cprint(f"Check this Domain {browser_search_arry}",attrs=[Color.BG_BLUE])
    Brower_Search(browser_search_arry)


'''
pip install python-nmap
pip install term-printer
sudo su
source venv/bin/activate
'''

```

## screenshot
```py
'''
sudo apt install python3-pip chromium chromium-driver
pip3 install selenium pyvirtualdisplay
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

def take_screenshot(url, output_path):
    """指定されたURLのスクリーンショットを保存する。

    Args:
        url (str): スクリーンショットを撮るURL.
        output_path (str): スクリーンショットの保存パス.
    """
    display = Display(visible=0, size=(1920, 1080))  # 仮想ディスプレイを開始
    display.start()

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモードを有効化
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)  # ウィンドウサイズを設定
    driver.get(url)  # URLを開く
    driver.save_screenshot(output_path)  # スクリーンショットを保存
    driver.quit()  # ブラウザを閉じる

    display.stop()  # 仮想ディスプレイを停止

# 使用例
url = "https://www.google.com"
output_path = "screenshot.png"
take_screenshot(url, output_path)
print(f"{url}のスクリーンショットを{output_path}に保存しました。")

```
