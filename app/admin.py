from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.database.requests import get_links, get_contacts
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from unicodedata import category

