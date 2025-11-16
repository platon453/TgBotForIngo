import json
from config import LANDING_URL
from bot.data.faq_data import load_faq_data

def _build_vk_keyboard(buttons, one_time=False, inline=False):
    """Helper to build VK keyboard JSON."""
    keyboard = {
        "one_time": one_time,
        "buttons": buttons,
        "inline": inline
    }
    return json.dumps(keyboard, ensure_ascii=False)

def build_main_menu_keyboard():
    """Builds the main menu keyboard for VK."""
    data = load_faq_data()
    buttons = []
    for i, category in enumerate(data['categories']):
        buttons.append([{
            "action": {
                "type": "callback",
                "payload": json.dumps({"type": "category_select", "data": i}),
                "label": category['name']
            },
            "color": "primary"
        }])
    
    buttons.append([{
        "action": {
            "type": "open_link",
            "link": LANDING_URL,
            "label": "🌐 Перейти на лендинг",
            "payload": json.dumps({"type": "landing_click"}) # Payload for tracking
        }
    }])
    
    return _build_vk_keyboard(buttons, inline=True)

def build_question_menu_keyboard(category_index):
    """Builds the question menu for a given category for VK."""
    data = load_faq_data()
    question_ids = data['categories'][category_index]['questions']
    buttons = []
    for i, q_id in enumerate(question_ids):
        buttons.append([{
            "action": {
                "type": "callback",
                "payload": json.dumps({"type": "question_select", "data": {"category_index": category_index, "question_index": i}}),
                "label": data['questions'][str(q_id)]['short_title']
            },
            "color": "default"
        }])
    
    buttons.append([{
        "action": {
            "type": "callback",
            "payload": json.dumps({"type": "back_to_main_menu"}),
            "label": "<< Назад"
        },
        "color": "negative"
    }])
    
    return _build_vk_keyboard(buttons, inline=True)

def build_question_answer_keyboard(category_index):
    """Builds a keyboard with a back button and a landing page button for VK."""
    buttons = [
        [{
            "action": {
                "type": "callback",
                "payload": json.dumps({"type": "back_to_category", "data": category_index}),
                "label": "<< Назад"
            },
            "color": "negative"
        }],
        [{
            "action": {
                "type": "open_link",
                "link": LANDING_URL,
                "label": "🌐 Перейти на лендинг",
                "payload": json.dumps({"type": "landing_click"}) # Payload for tracking
            }
        }]
    ]
    return _build_vk_keyboard(buttons, inline=True)
