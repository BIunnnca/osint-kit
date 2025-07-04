#!/usr/bin/env python3
"""
crtsh_scan – récupère les sous-domaines via Certificate Transparency (crt.sh)
Usage :
    python3 src/main.py --module crtsh_scan example.com
"""
from argparse import ArgumentParser
from crtsh import crtshAPI

def run(domain: str):
    print(f"[+] crt.sh pour : {domain}")
    api = crtshAPI()
    entries = api.search(domain, table="certificate")["entries"]
    uniques = sorted({e["name_value"] for e in entries})
    for sub in uniques:
        print(f"  • {sub}")

def main(args_list=None):
    import sys
    args_list = args_list or sys.argv[1:]

    parser = ArgumentParser(description="Scan crt.sh – sous-domaines via CT logs")
    parser.add_argument("domain", nargs="?", help="Domaine cible (ex.: example.com)")
    parser.add_argument("--target", "-t", help="Alias de --domain (compatibilité)")
    args = parser.parse_args(args_list)

    domain = args.target or args.domain
    if not domain:
        parser.error("Spécifie un domaine positionnel ou avec --target/-t")

    run(domain)

if __name__ == "__main__":
    main()
