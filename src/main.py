#!/usr/bin/env python3
import requests, sys, datetime, os

def banner():
    print(f"[OSINT-Kit] {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")

def run():
    banner()
    url = sys.argv[1] if len(sys.argv) > 1 else "https://httpbin.org/ip"
    r = requests.get(url, timeout=10)
    print(f"[*] GET {url} → {r.status_code}")
    print(r.text)

if __name__ == "__main__":
    run()
