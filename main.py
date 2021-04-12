#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging, random, sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect, text
from dotenv import load_dotenv
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "clues.db")
API_KEY = os.getenv('API_KEY')

updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

engine = create_engine('sqlite:///{}'.format(db_path), echo=True, future=True)

def test_select(engine):
    with engine.connect() as conn:
        result = conn.execute(text("select * from clues where id = 10000"))
        return result.all()

print(test_select(engine))


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to Jeopardy!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()