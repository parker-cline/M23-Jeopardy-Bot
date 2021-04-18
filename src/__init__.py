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