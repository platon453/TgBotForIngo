import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import json
import os

from config import VK_API_TOKEN, VK_GROUP_ID, LANDING_URL
from bot.vk_keyboards import build_main_menu_keyboard, build_question_menu_keyboard, build_question_answer_keyboard
from bot.vk_handlers import handle_start, handle_main_menu, handle_category_selection, handle_question_selection, handle_landing_click
from bot.data.faq_data import load_faq_data
from bot.states import user_states, STATE_AWAIT_MAIN_MENU, STATE_CATEGORY_SELECTED, STATE_QUESTION_SELECTED

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    if not VK_API_TOKEN or not VK_GROUP_ID:
        logger.error("VK_API_TOKEN or VK_GROUP_ID is not set in .env file.")
        return

    vk_session = vk_api.VkApi(token=VK_API_TOKEN)
    longpoll = VkBotLongPoll(vk_session, int(VK_GROUP_ID))
    vk = vk_session.get_api()

    logger.info("VK Bot started!")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text']:
            user_id = event.obj.message['from_id']
            text = event.obj.message['text']
            payload = event.obj.message.get('payload')

            current_state = user_states.get(user_id, STATE_AWAIT_MAIN_MENU)
            logger.info(f"Received message from user {user_id}. Text: '{text}'. Current state: '{current_state}'. Payload: {payload}")

            if text == '/start':
                handle_start(vk, user_id, user_states)
            elif text == 'Главное меню' and current_state == STATE_AWAIT_MAIN_MENU:
                handle_main_menu(vk, user_id, user_states)
            elif payload:
                payload_data = json.loads(payload)
                action = payload_data.get('type')
                data = payload_data.get('data')

                if action == 'category_select':
                    handle_category_selection(vk, user_id, data, user_states)
                elif action == 'question_select':
                    handle_question_selection(vk, user_id, data, user_states)
                elif action == 'back_to_main_menu':
                    handle_main_menu(vk, user_id, user_states)
                elif action == 'back_to_category':
                    handle_category_selection(vk, user_id, data, user_states) # data here is category_index
                elif action == 'landing_click':
                    handle_landing_click(vk, user_id, user_states)
            else:
                vk.messages.send(
                    user_id=user_id,
                    message="Извините, я не понял вашу команду. Пожалуйста, используйте кнопки.",
                    random_id=0
                )

if __name__ == '__main__':
    main()