
import json
import os

def load_faq_data() -> dict:
    """Loads the FAQ data from the JSON file."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'faq_data.json'), 'r', encoding='utf-8') as f:
        return json.load(f)
