#!/usr/bin/env python3
"""
telegram_bot – module OSINT-Kit
Usage :
    python3 src/main.py --module telegram_bot --token YOUR_BOT_TOKEN
"""

import argparse, asyncio, logging, os, sys
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ───────────────────────────────────────────────
#  Handlers
# ───────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salut ! Envoie /help pour la liste des commandes.")

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Démarrage\n"
        "/help  - Cette aide\n"
        "/echo  - Je répète ton message"
    )

async def echo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# ───────────────────────────────────────────────
#  Setup & launch
# ───────────────────────────────────────────────
def main(argv=None):
    parser = argparse.ArgumentParser(description="Mini bot Telegram")
    parser.add_argument("--token", required=True, help="Token @BotFather")
    parser.add_argument("--loglevel", default="INFO")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=args.loglevel.upper(),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )
    log = logging.getLogger("telegram_bot")
    log.info("Boot…")

    app = (
        ApplicationBuilder()
        .token(args.token)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    log.info("Bot prêt !  Ctrl-C pour quitter.")
    try:
        app.run_polling()
    except KeyboardInterrupt:
        log.info("Arrêt demandé par l’utilisateur.")

if __name__ == "__main__":
    main()
