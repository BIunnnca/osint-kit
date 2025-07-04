import sys
from dnsdumpster import DNSDumpsterAPI

def run(target="example.com"):
    results = DNSDumpsterAPI().search(target)
    print("[+] Domaine analysé :", target)
    for host in results['dns_records']['host']:
        print(f"  - {host['domain']} ({host['ip']})")

def main(args_list=None):
    """
    Point d’entrée appelé par OSINT-Kit.
    Utilisation : --module dnsdumpster_scan --target example.com
    """
    if args_list is None:
        args_list = []
    target = args_list[args_list.index("--target")+1] if "--target" in args_list else "example.com"
    run(target)
