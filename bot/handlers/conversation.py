
from telegram import Update
from telegram.ext import ContextTypes

from bot.data.faq_data import load_faq_data
from bot.keyboards.inline import build_question_menu, build_question_keyboard

AWAIT_MAIN_MENU, CATEGORY, QUESTION = range(3)

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the questions for the selected category."""
    query = update.callback_query
    await query.answer()
    category_index = int(query.data.split('_')[1])
    data = load_faq_data()
    category = data['categories'][category_index]
    
    await query.edit_message_text(
        text=f"Вы выбрали категорию: {category['name']}",
        reply_markup=build_question_menu(category_index)
    )
    return QUESTION

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the answer to the selected question."""
    query = update.callback_query
    await query.answer()
    category_index, question_index = map(int, query.data.split('_')[1:])
    data = load_faq_data()
    question_id = data['categories'][category_index]['questions'][question_index]
    question_text = data['questions'][str(question_id)]['question']
    answer_text = data['questions'][str(question_id)]['answer']

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
    from bot.keyboards.inline import build_main_menu
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
