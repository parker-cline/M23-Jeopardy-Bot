#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging, random, sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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


# TODO: move to unit_test.py
def test_select(engine):
    with engine.connect() as conn:
        stmt = select(clues).where(clues.c.id == 10000)
        print(conn.execute(stmt).first())

def select_random(engine):
    with engine.connect() as conn:
        stmt_num_rows = select(func.count('*')).select_from(clues)
        num_rows = conn.execute(stmt_num_rows).first()[0]
        random_id = random.randint(1, num_rows)
        stmt = select(documents).where(documents.c.id == random_id)
        print(conn.execute(stmt).first())


select_random(engine)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to Jeopardy!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()