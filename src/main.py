#!/usr/bin/env python3
"""
OSINT-Kit – point d’entrée CLI
──────────────────────────────
• Mode 1 : scan HTTP rapide
      python3 src/main.py https://example.com

• Mode 2 : appel d’un module interne
      python3 src/main.py --module dnsdumpster_scan --target example.com
"""
import argparse
import datetime
import importlib
import sys
from pathlib import Path


# ────────────────────────────────
#  Loader dynamique des modules
# ────────────────────────────────
def load_module(name: str):
    """Importe dynamiquement un module situé dans le dossier 'modules/'."""
    if "." in name or "/" in name:
        raise ValueError("Nom de module invalide : ne mets ni point ni slash.")
    modules_path = Path(__file__).resolve().parent.parent / "modules"
    sys.path.append(str(modules_path))
    return importlib.import_module(name)


# ────────────────────────────────
#  Utilitaires
# ────────────────────────────────
def banner():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[OSINT-Kit] {now}")


def run_http(url: str):
    import requests

    print(f"[*] Requête GET → {url}")
    try:
        r = requests.get(url, timeout=15)
        print(f"[+] Status : {r.status_code}")
        preview = r.text[:400] + (" [...]" if len(r.text) > 400 else "")
        print(preview)
    except Exception as e:
        print(f"[!] Erreur : {e}")


# ────────────────────────────────
#  Point d’entrée principal
# ────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="OSINT-Kit CLI")
    parser.add_argument(
        "target",
        nargs="?",
        help="URL (mode HTTP) ou premier argument passé au module.",
    )
    parser.add_argument(
        "--module",
        "-m",
        help="Nom du module à charger depuis le dossier 'modules/'.",
    )

    args, extra = parser.parse_known_args()
    banner()

    if args.module:
        # si la cible positionnelle est fournie, on la pousse dans la liste extra
        if args.target:
            extra = ["--target", args.target] + extra

        module = load_module(args.module)
        print(f"[+] Module « {args.module} » chargé.")

        if not hasattr(module, "main"):
            sys.exit(f"[!] Le module « {args.module} » n’expose pas de fonction main().")

        module.main(extra)  # on transmet les arguments restants
    else:
        if not args.target:
            parser.error("Une URL est requise si --module n’est pas précisé.")
        run_http(args.target)


# ────────────────────────────────
if __name__ == "__main__":
    main()
