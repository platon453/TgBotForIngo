

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, Defaults
from telegram.request import HTTPXRequest

from config import TELEGRAM_TOKEN
from bot.handlers.commands import start, main_menu
from bot.handlers.conversation import AWAIT_MAIN_MENU, CATEGORY, QUESTION, category, question, back_to_main_menu, landing_click

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    defaults = Defaults(block=False)
    request = HTTPXRequest(proxy=None)
    application = Application.builder().token(TELEGRAM_TOKEN).defaults(defaults).request(request).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AWAIT_MAIN_MENU: [MessageHandler(filters.Regex('^Главное меню$'), main_menu)],
            CATEGORY: [CallbackQueryHandler(category, pattern='^category_')],
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

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
