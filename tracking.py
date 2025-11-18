
import os

COUNTER_FILE = "landing_clicks.txt"

def increment_counter():
    """Increments the landing page click counter."""
    count = get_counter()
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count + 1))

def get_counter() -> int:
    """Gets the current value of the landing page click counter."""
    if not os.path.exists(COUNTER_FILE):
        return 0
    with open(COUNTER_FILE, "r") as f:
        try:
            return int(f.read())
        except (ValueError, TypeError):
            return 0
