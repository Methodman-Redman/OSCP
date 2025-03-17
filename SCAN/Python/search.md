```py
import requests
from term_printer import Color, cprint

target = 'localhost'
def main():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    headers = {'user-agent': user_agent}
    Vuln_Search_Func(headers)

def Vuln_Search_Func(headers):
    cnt = 0
    # First test
    url = f'http://{target}'
    cnt = Search_Vuln_Point(headers,url,cnt)
    url = f'http://{target}/test.html'
    cnt = Search_Vuln_Point(headers,url,cnt)
    url = f'http://{target}/test2.html'
    cnt = Search_Vuln_Point(headers,url,cnt)

    if cnt == 3:
        cprint(f"{target} has CVE-2024-1234 {cnt}/3", attrs=[Color.BG_BRIGHT_BLUE])
    else:
        print(f"{target} has CVE-2024-1234 {cnt}/3")
        

def Search_Vuln_Point(headers,url,cnt):
    response = requests.get(url, headers=headers)
    
    http_code = response.status_code
    print(http_code)
    if http_code == 200:
        cnt += 1
        print(f'Find {url} Vuln count {cnt}')
    return cnt
    
    
if __name__ == "__main__":
    main()
```
