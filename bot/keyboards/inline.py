
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data.faq_data import load_faq_data
from config import LANDING_URL

def build_main_menu() -> InlineKeyboardMarkup:
    """Builds the main menu keyboard."""
    data = load_faq_data()
    buttons = [
        [InlineKeyboardButton(category['name'], callback_data=f"category_{i}")]
        for i, category in enumerate(data['categories'])
    ]
    buttons.append([InlineKeyboardButton("🌐 Перейти на лендинг", url=LANDING_URL, callback_data="landing_click")])
    return InlineKeyboardMarkup(buttons)

def build_question_menu(category_index: int) -> InlineKeyboardMarkup:
    """Builds the question menu for a given category."""
    data = load_faq_data()
    question_ids = data['categories'][category_index]['questions']
    buttons = [
        [InlineKeyboardButton(data['questions'][str(q_id)]['question'], callback_data=f"question_{category_index}_{i}")]
        for i, q_id in enumerate(question_ids)
    ]
    buttons.append([InlineKeyboardButton("<< Назад", callback_data="back_to_main_menu")])
    return InlineKeyboardMarkup(buttons)

def build_question_keyboard(category_index: int) -> InlineKeyboardMarkup:
    """Builds a keyboard with a back button and a landing page button."""
    buttons = [
        [InlineKeyboardButton("<< Назад", callback_data=f"category_{category_index}")],
        [InlineKeyboardButton("🌐 Перейти на лендинг", url=LANDING_URL, callback_data="landing_click")]
    ]
    return InlineKeyboardMarkup(buttons)
