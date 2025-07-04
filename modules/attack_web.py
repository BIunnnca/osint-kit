#!/usr/bin/env python3
"""
attack_web – Interface Flask pour attaques adversariales
Usage :
    python3 src/main.py --module attack_web --host 0.0.0.0 --port 5000
"""

from pathlib import Path
import argparse, json, random
from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent.parent / "web"
app = Flask(__name__,
            template_folder=str(BASE_DIR / "templates"),
            static_folder=str(BASE_DIR / "static"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run_attack", methods=["POST"])
def run_attack():
    data = request.get_json(force=True)

    # TODO : remplace ce bloc par ta vraie attaque
    dummy_score = round(random.uniform(0, 1), 4)
    results = {
        "status": "ok",
        "params_received": data,
        "success_rate": dummy_score,
        "details": "Replace this with real attack results."
    }
    return jsonify(results)


def main(args_list=None):
    parser = argparse.ArgumentParser(description="Serveur web d'attaque")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args(args_list)

    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
