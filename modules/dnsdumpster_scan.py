#!/usr/bin/env python3
"""
dnsdumpster_scan – module OSINT-Kit
──────────────────────────────────
Deux usages équivalents :

    # Avec option nommée
    python3 src/main.py --module dnsdumpster_scan --target example.com

    # Ou avec argument positionnel
    python3 src/main.py --module dnsdumpster_scan example.com
"""
from argparse import ArgumentParser
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI


def run(domain: str) -> None:
    """Exécute la recherche DNSDumpster pour un domaine donné et affiche les hôtes trouvés."""
    print(f"[+] Domaine analysé : {domain}")
    results = DNSDumpsterAPI().search(domain)

    hosts = results.get("dns_records", {}).get("host", [])
    if not hosts:
        print("[!] Aucun hôte trouvé.")
        return

    for host in hosts:
        print(f"  • {host['domain']}  ({host['ip']})")


def main(args_list=None) -> None:
    """
    Point d’entrée appelé par OSINT-Kit.
    `args_list` est la liste transmise par src/main.py ; si le module est lancé
    directement, on récupère sys.argv[1:].
    """
    import sys

    if args_list is None:
        args_list = sys.argv[1:]

    parser = ArgumentParser(description="Scan DNSDumpster pour un domaine")
    parser.add_argument(
        "domain",
        nargs="?",
        help="Domaine cible (ex.: example.com)",
    )
    parser.add_argument(
        "--target", "-t",
        help="Alias de --domain, permet d’écrire --target example.com",
    )
    args = parser.parse_args(args_list)

    # Priorité à --target, sinon à l’argument positionnel
    domain = args.target or args.domain
    if not domain:
        parser.error("Spécifie un domaine via argument positionnel ou --target.")

    run(domain)


# Lancement direct éventuel (debug)
if __name__ == "__main__":
    main()
