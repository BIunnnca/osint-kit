"""
Module dnsdumpster_scan – Recherche de sous-domaines / IP
Utilisation :
    python3 src/main.py --module dnsdumpster_scan --target example.com
"""

from argparse import ArgumentParser
from dnsdumpster import DNSDumpsterAPI


def run(target: str):
    print(f"[+] Domaine analysé : {target}")
    results = DNSDumpsterAPI().search(target)
    hosts = results["dns_records"]["host"]
    if not hosts:
        print("[!] Aucun enregistrement trouvé.")
        return
    for h in hosts:
        print(f"  • {h['domain']}  ({h['ip']})")


# ----- point d’entrée appelé par OSINT-Kit ---------------------------
def main(args_list=None):
    """
    args_list est fourni par OSINT-Kit ; si lancé isolément on récupère sys.argv.
    """
    import sys
    if args_list is None:
        args_list = sys.argv[1:]

    parser = ArgumentParser(description="Scan DNSDumpster")
    parser.add_argument("--target", "-t", required=True,
                        help="Domaine à analyser, ex : example.com")
    args = parser.parse_args(args_list)

    run(args.target)
