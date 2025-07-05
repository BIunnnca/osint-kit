#!/usr/bin/env python3
"""
attack_web – Interface Flask « Adversarial Attack » pour OSINT-Kit

Lancement direct :
    python3 modules/attack_web.py --host 0.0.0.0 --port 8000

Lancement via OSINT-Kit :
    python3 src/main.py --module attack_web -- --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# ─────────────────────────────────────────────
#  Chemins (templates / static dans  « web/ »)
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
)


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────
@app.route("/")
def index():
    """Affiche la page HTML du formulaire."""
    return render_template("index.html")


@app.route("/run_attack", methods=["POST"])
def run_attack():
    """
    Point d’API où l’on branchera la vraie logique d’attaque.
    Pour l’instant : on renvoie simplement les paramètres reçus.
    """
    try:
        cfg = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # TODO : remplacer par votre pipeline d’attaque
    dummy_results = {
        "status": "ok",
        "details": "Attaque simulée – à implémenter",
        "received_cfg": cfg,
    }
    return jsonify(dummy_results), 200


# ─────────────────────────────────────────────
#  Point d’entrée module
# ─────────────────────────────────────────────
def main(argv: list[str] | None = None):
    """
    Fonction appelée par OSINT-Kit :
        module.main(remainder)
    `argv` reçoit exactement la liste `remainder`.
    """
    parser = argparse.ArgumentParser(
        prog="attack_web",
        description="Lance le serveur Flask Attack-Web",
        allow_abbrev=False,
    )
    parser.add_argument("--host", default="127.0.0.1", help="Adresse d’écoute Flask")
    parser.add_argument("--port", type=int, default=5000, help="Port d’écoute Flask")
    args = parser.parse_args(argv)

    print(f"[attack_web] Interface disponible sur http://{args.host}:{args.port}")
    # debug=False pour éviter le reloader qui double les processus
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
