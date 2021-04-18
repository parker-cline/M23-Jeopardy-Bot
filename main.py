#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging, random, sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from sqlalchemy import create_engine, MetaData, Table, text, select, func
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# env variables
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "clues.db")
API_KEY = os.getenv('API_KEY')

# load telegram classes
updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

# load sqlalchemy classes
engine = create_engine('sqlite:///{}'.format(db_path), future=True)
metadata = MetaData()
# reflect tables
clues = Table("clues", metadata, autoload_with=engine)
airdates = Table("airdates", metadata, autoload_with=engine)
documents = Table("documents", metadata, autoload_with=engine)
categories = Table("categories", metadata, autoload_with=engine)
classifications = Table("classifications", metadata, autoload_with=engine)


def random_clue(engine):
    with engine.connect() as conn:

        stmt_num_rows = select(func.count('*')).select_from(clues)
        num_rows = conn.execute(stmt_num_rows).first()[0]
        random_id = random.randint(1, num_rows)

        stmt_clue = select(documents).where(documents.c.id == random_id)
        clue = conn.execute(stmt_clue).first()

        stmt_category = select(categories.c.category).select_from(
            categories.join(
                classifications,
                categories.c.id == classifications.c.category_id).join(
                    documents,
                    classifications.c.clue_id == documents.c.id)).where(
                        documents.c.id == random_id)
        category = conn.execute(stmt_category).first()
        return category[0], clue[1], clue[2]


def start(update, context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user


def getclue(update, context) -> None:
    category, clue, answer = random_clue(engine)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=(category + ": " + clue))
    context.bot_data["answer"] = answer
    print(answer)


def check_answer(update, context):
    if context.bot_data["answer"] and update.message.text.lower() == context.bot_data["answer"].lower():
        context.bot.send_message(chat_id=update.effective_chat.id,
                             text="You got it.")
    context.bot_data["answer"] = None


def help(update, context) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)

getclue_handler = CommandHandler("getclue", getclue)
dispatcher.add_handler(getclue_handler)

check_answer_handler = MessageHandler(Filters.text & (~Filters.command), check_answer)
dispatcher.add_handler(check_answer_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()