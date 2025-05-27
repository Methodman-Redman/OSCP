import subprocess
import urllib.parse
import argparse
import sys
import os
import time

def build_search_url(target_url):
    query = f"site:{target_url} ext:login"
    encoded_query = urllib.parse.quote_plus(query)
    return f"https://www.google.com/search?q={encoded_query}"

def open_in_firefox(url, first=False):
    try:
        if first:
            # Open firefox
            subprocess.Popen(["firefox", "--new-window", url])
        else:
            # Back ground
            subprocess.Popen(["firefox", "--new-tab", url])
        # Timing
        time.sleep(0.5)
    except Exception as e:
        print(f"[!] Misstake Firefox open: {e}")

def main():
    parser = argparse.ArgumentParser(description="Google Dork By Firefox")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="URL")
    group.add_argument("-f", "--file", help="File")

    args = parser.parse_args()

    if args.url:
        search_url = build_search_url(args.url)
        print(f"[+] Opening: {search_url}")
        open_in_firefox(search_url, first=True)

    elif args.file:
        if not os.path.isfile(args.file):
            print(f"[!] Not File: {args.file}")
            sys.exit(1)

        with open(args.file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        for i, url in enumerate(urls):
            search_url = build_search_url(url)
            print(f"[+] Opening: {search_url}")
            open_in_firefox(search_url, first=(i == 0))

if __name__ == "__main__":
    main()
