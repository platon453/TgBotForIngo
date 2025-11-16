import json
import vk_api
from bot.vk_keyboards import build_main_menu_keyboard, build_question_menu_keyboard, build_question_answer_keyboard, _build_vk_keyboard
from bot.data.faq_data import load_faq_data
from bot.services.tracking import increment_counter
from bot.states import STATE_AWAIT_MAIN_MENU, STATE_CATEGORY_SELECTED, STATE_QUESTION_SELECTED

def send_message(vk, user_id, message, keyboard=None):
    """Helper function to send a message with an optional keyboard."""
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard
    )

def handle_start(vk, user_id, user_states):
    """Handles the /start command."""
    start_keyboard = _build_vk_keyboard([[{"action": {"type": "text", "label": "Главное меню"}, "color": "primary"}]])
    send_message(
        vk,
        user_id,
        "Привет! Я Инга, чат-бот. Нажми 'Главное меню' чтобы начать.",
        keyboard=start_keyboard
    )
    user_states[user_id] = STATE_AWAIT_MAIN_MENU

def handle_main_menu(vk, user_id, user_states):
    """Displays the main menu."""
    send_message(
        vk,
        user_id,
        "Выбери категорию вопросов:",
        keyboard=build_main_menu_keyboard()
    )
    user_states[user_id] = STATE_CATEGORY_SELECTED

def handle_category_selection(vk, user_id, category_index, user_states):
    """Displays questions for the selected category."""
    data = load_faq_data()
    category_name = data['categories'][category_index]['name']
    send_message(
        vk,
        user_id,
        f"Вы выбрали категорию: {category_name}",
        keyboard=build_question_menu_keyboard(category_index)
    )
    user_states[user_id] = STATE_QUESTION_SELECTED

def handle_question_selection(vk, user_id, data_payload, user_states):
    """Displays the answer to the selected question."""
    category_index = data_payload['category_index']
    question_index = data_payload['question_index']
    
    data = load_faq_data()
    question_id = data['categories'][category_index]['questions'][question_index]
    question_text = data['questions'][str(question_id)]['question']
    answer_text = data['questions'][str(question_id)]['answer']

    send_message(
        vk,
        user_id,
        f"{question_text}\n\n{answer_text}",
        keyboard=build_question_answer_keyboard(category_index)
    )
    user_states[user_id] = STATE_QUESTION_SELECTED

def handle_landing_click(vk, user_id, user_states):
    """Handles the landing page click."""
    increment_counter()
    # VK open_link buttons handle the URL directly, so no message is needed here.
    # We might want to send a confirmation message if the user clicks a callback button
    # that triggers the landing page, but for open_link, it's handled by VK client.
    # For now, just increment the counter.
    pass
