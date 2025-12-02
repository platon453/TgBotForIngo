
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from bot.keyboards.inline import build_main_menu
from bot.handlers.conversation import CATEGORY


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a welcome text and a main menu button."""
    reply_keyboard = [["Главное меню"]]

    await update.message.reply_text(
        "Привет! Я Инга, чат-бот.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the main menu and enters the conversation."""
    await update.message.reply_text(
        "Выбери категорию вопросов:",
        reply_markup=build_main_menu()
    )
    return CATEGORY
