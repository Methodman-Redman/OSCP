```py
import os
import sys
import subprocess
import webbrowser
import nmap
import time
import re

hosts_file = "/etc/hosts"

def Normal_nmap(target_ip):
    options = "-sV -sC -F -Pn -T5"
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments=options)
    port_arry = []
    common_name = ""
    for host in nm.all_hosts():
        print("Host: ", host)
        for proto in nm[host].all_protocols():
            print("Protocol: ", proto)
            ports = nm[host][proto].keys()
            for port in ports:
                #print("Port: ", port, "State: ", nm[host][proto][port]['state'])
                print("service:", nm[host][proto][port]['product'] , "Version",nm[host][proto][port]['version'])
                common_name = str(nm[host][proto][port]['script'])
                pattern = r'\b([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)?\.htb)\b'
                matches = re.findall(pattern, common_name)
                if matches:
                    print(matches)
                    print(matches[0])
                    with open(hosts_file, "r") as f:
                        existing_hosts = f.read()

                    new_entries = []
                    for domain in matches:
                        entry = f"{target_ip} {domain}"
                        if entry not in existing_hosts:
                            new_entries.append(entry)

                    if new_entries:
                        with open(hosts_file, "a") as f:
                            f.write("\n" + "\n".join(new_entries) + "\n")
                        print("Updated /etc/hosts with new domains.")
                    else:
                        print("No new domains to add.")
                    target_ip = matches[0]
                brower_tmp = str(port)
                http_tmp = str(nm[host][proto][port]['name'])
                if brower_tmp == "80" or brower_tmp == "443" or http_tmp == "http":
                    Browser_Search(target_ip,brower_tmp)
                
                service_name = str(nm[host][proto][port]['product'])
                service_name = service_name.split()[0]
                tmp_version = nm[host][proto][port]['version']
                tmp_version = tmp_version[:4]
                vuln_word = service_name + " " + tmp_version
                command = f'searchsploit {service_name}'
                Run_Command(command)
                command = f'searchsploit {vuln_word}'
                Run_Command(command)
                # --script=vuln port
                port_arry.append(port)
    print("Debug")
    port_arry = str(port_arry)
    port_arry = port_arry[1:-1]
    port_arry = port_arry.replace(" ","")
    time.sleep(1)
    command = f'nmap --script=vuln -Pn -T5 -p {port_arry} {target_ip}'
    Run_Command(command)

    '''
    query = nm[host].keys()
    print(query)
    # dict_keys(['hostnames', 'addresses', 'vendor', 'status', 'tcp'])
    query = nm[host].values()
    print(query)
    query = nm[host].values()
    print(query)
    '''

def Open_Qterminal():
    # Start First qterminal
    subprocess.Popen(['qterminal'])
    time.sleep(2)  

def Run_Command(command):
    # New Terminal execute command
    subprocess.run(['xdotool', 'key', 'ctrl+shift+t'])
    time.sleep(0.5)
    print(command)
    subprocess.run(['xdotool', 'type', f'{command}'])
    subprocess.run(['xdotool', 'key', 'Return'])

def Browser_Search(target_ip,port):
    if port == "80":
        search_url = f"http://{target_ip}"
    elif port == "443":
        search_url = f"https://{target_ip}"
    else:
        search_url = f"http://{target_ip}:{port}"
    
    time.sleep(0.5)
    Directory_SCAN(search_url)
    #webbrowser.open(search_url)

def Directory_SCAN(search_url):
    command = f'whatweb --aggression 3 -v {search_url}'
    Run_Command(command)
    command = f'gobuster dir -u {search_url} -w /usr/share/wordlists/dirb/common.txt -k'
    Run_Command(command)

if __name__ == "__main__":
    Open_Qterminal()
    #target_ip = input("please ip : ")
    target_ip = "10.10.10.17"
    command = f'nmap -sV -Pn -F -T5 {target_ip}'
    Run_Command(command)
    command = f'nmap -sV -Pn -T5 {target_ip}'
    Run_Command(command)
    command = f'nmap -Pn -p- -T5  {target_ip}'
    Run_Command(command)
    Normal_nmap(target_ip)


'''
pip install python-nmap
sudo su
source venv/bin/activate
'''

```
