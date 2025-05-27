import subprocess
import urllib.parse
import argparse
import sys
import os
import time

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q={}",
    "Yahoo":  "https://search.yahoo.co.jp/search?p={}",
    "Baidu":  "https://www.baidu.com/s?wd={}"
}

def build_search_urls(keyword):
    encoded_query = urllib.parse.quote_plus(keyword)
    return {name: url.format(encoded_query) for name, url in SEARCH_ENGINES.items()}

def open_in_firefox(url, first=False):
    try:
        cmd = ["firefox", "--new-window" if first else "--new-tab", url]
        subprocess.Popen(cmd)
        time.sleep(0.5) 
    except Exception as e:
        print(f"[!] Misstake Firefox Open: {e}")

def process_query(keyword, is_first_group=False):
    search_urls = build_search_urls(keyword)
    for i, (engine, url) in enumerate(search_urls.items()):
        print(f"[+] {engine} で検索: {url}")
        open_in_firefox(url, first=(is_first_group and i == 0))

def main():
    parser = argparse.ArgumentParser(description="Check Search Engine")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="URL")
    group.add_argument("-f", "--file", help="File")

    args = parser.parse_args()

    if args.url:
        process_query(args.url, is_first_group=True)

    elif args.file:
        if not os.path.isfile(args.file):
            print(f"[!] Not File exist: {args.file}")
            sys.exit(1)

        with open(args.file, "r") as f:
            queries = [line.strip() for line in f if line.strip()]

        for i, query in enumerate(queries):
            process_query(query, is_first_group=(i == 0))

if __name__ == "__main__":
    main()
