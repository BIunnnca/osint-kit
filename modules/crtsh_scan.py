#!/usr/bin/env python3
"""
crtsh_scan – Récupère les sous-domaines via Certificate Transparency (crt.sh)

Exemples :
    python3 src/main.py --module crtsh_scan example.com
    python3 src/main.py --module crtsh_scan --target example.com
"""
from argparse import ArgumentParser
import json, requests, sys, datetime, pathlib


def fetch_subs(domain: str) -> set[str]:
    """Interroge https://crt.sh/?q=%25.<domain>&output=json et renvoie un set de sous-domaines."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = json.loads(r.text)
    # `name_value` peut contenir plusieurs lignes séparées par \n
    subs = {d.strip() for entry in data for d in entry["name_value"].splitlines()}
    # enlève les wildcards *.example.com
    subs = {s.lstrip("*.") for s in subs}
    return subs


def run(domain: str) -> None:
    print(f"[+] crt.sh – domaine : {domain}")
    try:
        subs = fetch_subs(domain)
    except Exception as e:
        print(f"[!] Erreur crt.sh : {e}")
        return

    if not subs:
        print("[!] Aucun sous-domaine trouvé.")
        return

    for sub in sorted(subs):
        print(f"  • {sub}")

    # Sauvegarde brute dans reports/
    reports = pathlib.Path(__file__).resolve().parent.parent / "reports"
    reports.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = reports / f"crtsh_{domain}_{ts}.txt"
    outfile.write_text("\n".join(sorted(subs)))
    print(f"[✓] Rapport sauvegardé → {outfile}")


def main(args_list=None):
    args_list = args_list or sys.argv[1:]
    p = ArgumentParser(description="Scan Certificate Transparency (crt.sh)")
    p.add_argument("domain", nargs="?", help="Domaine cible (ex.: example.com)")
    p.add_argument("--target", "-t", help="Alias pour --domain (compatibilité)")
    ns = p.parse_args(args_list)

    domain = ns.target or ns.domain
    if not domain:
        p.error("Spécifie un domaine en positionnel OU avec --target/-t.")

    run(domain)


if __name__ == "__main__":
    main()
