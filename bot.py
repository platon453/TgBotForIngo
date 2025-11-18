import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    Defaults
)
from telegram.request import HTTPXRequest

from config import TELEGRAM_TOKEN
from tracking import increment_counter
from keyboards_and_data import (
    build_main_menu,
    build_question_menu,
    build_question_keyboard,
    load_faq_data
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# State constants
AWAIT_MAIN_MENU, CATEGORY, QUESTION = range(3)

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with a welcome text and a main menu button, entering the conversation."""
    reply_keyboard = [["Главное меню"]]
    await update.message.reply_text(
        "Привет! Я Инга, чат-бот.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return AWAIT_MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the main menu."""
    await update.message.reply_text(
        "Выбери категорию вопросов:",
        reply_markup=build_main_menu()
    )
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the questions for the selected category."""
    query = update.callback_query
    await query.answer()
    category_index = int(query.data.split('_')[1])
    data = load_faq_data()
    category_name = data['categories'][category_index]['name']
    
    await query.edit_message_text(
        text=f"Вы выбрали категорию: {category_name}",
        reply_markup=build_question_menu(category_index)
    )
    return QUESTION

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the answer to the selected question."""
    query = update.callback_query
    await query.answer()
    category_index, question_index = map(int, query.data.split('_')[1:])
    data = load_faq_data()
    question_id = str(data['categories'][category_index]['questions'][question_index])
    question_text = data['questions'][question_id]['question']
    answer_text = data['questions'][question_id]['answer']

    await query.edit_message_text(
        text=f"*{question_text}*\n\n{answer_text}",
        parse_mode='Markdown',
        reply_markup=build_question_keyboard(category_index)
    )
    return QUESTION

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns to the main menu."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Выбери категорию вопросов:",
        reply_markup=build_main_menu()
    )
    return CATEGORY

async def landing_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the landing page click."""
    query = update.callback_query
    await query.answer()
    increment_counter()

# --- Main function ---

def main() -> None:
    """Start the bot."""
    defaults = Defaults(block=False)
    request = HTTPXRequest(proxy=None)
    application = Application.builder().token(TELEGRAM_TOKEN).defaults(defaults).request(request).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AWAIT_MAIN_MENU: [MessageHandler(filters.Regex('^Главное меню$'), main_menu)],
            CATEGORY: [
                CallbackQueryHandler(category, pattern='^category_'),
                CallbackQueryHandler(landing_click, pattern='^landing_click$')
            ],
            QUESTION: [
                CallbackQueryHandler(question, pattern='^question_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_to_main_menu$'),
                CallbackQueryHandler(landing_click, pattern='^landing_click$'),
                CallbackQueryHandler(category, pattern='^category_')
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
