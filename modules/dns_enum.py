#!/usr/bin/env python3
"""
dns_enum – Enumération de sous-domaines via subfinder et amass

Usage :
    python3 src/main.py --module dns_enum example.com
    python3 src/main.py --module dns_enum --target example.com -o reports/

Options pass-through :
    -o / --outdir    Chemin de sortie (dossier). Défaut : reports/
"""

import argparse, json, os, subprocess, sys, datetime
from pathlib import Path

def run_cmd(cmd: list[str]) -> list[str]:
    """Exécute une commande et renvoie les lignes uniques triées."""
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, timeout=300)
        return sorted(set(line.strip() for line in out.splitlines() if line.strip()))
    except subprocess.CalledProcessError as err:
        print(f"[!] Erreur commande {cmd[0]} : {err}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print(f"[!] {cmd[0]} n’est pas installé ou pas dans le PATH.", file=sys.stderr)
        return []

def enumerate_domain(domain: str) -> dict:
    print(f"[+] Enumération {domain}…")
    subfinder_res = run_cmd(["subfinder", "-silent", "-d", domain])
    amass_res     = run_cmd(["amass", "enum", "-passive", "-norecursive", "-d", domain])
    return {
        "domain": domain,
        "subfinder": subfinder_res,
        "amass": amass_res,
        "combined": sorted(set(subfinder_res + amass_res)),
    }

def main(args_list=None):
    parser = argparse.ArgumentParser(description="DNS enumeration")
    parser.add_argument("domain", nargs="?", help="Domaine cible")
    parser.add_argument("--target", "-t", help="Alias de domaine")
    parser.add_argument("--outdir", "-o", default="reports/", help="Dossier de sortie")
    args = parser.parse_args(args_list)

    domain = args.target or args.domain
    if not domain:
        parser.error("Spécifie un domaine (positionnel ou --target)")

    # Enumération
    results = enumerate_domain(domain)

    # Sauvegarde JSON
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / f"dns_enum_{domain}_{ts}.json"
    json_path.write_text(json.dumps(results, indent=2))
    print(f"[✓] Résultats sauvegardés → {json_path}")

    # Affichage terminal
    print("\n--- Sous-domaines uniques ---")
    for sub in results["combined"]:
        print(f"  • {sub}")
    print(f"Total : {len(results['combined'])}")

if __name__ == "__main__":
    main()
