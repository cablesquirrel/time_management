"""Functions related to the remote API endpoints"""

import json


def build_message_json(line_1_text: str, line_2_text: str) -> str:
    """Create a JSON version of the display text for sending to the remote display

    Args:
        line_1_text (str): Text to display on line 1 (Max 16 chars)
        line_2_text (str): Text to display on line 2 (Max 16 chars)

    Returns:
        str: JSON payload for remote unit
    """
    msg = {
        "line_1": line_1_text[:16],
        "line_2": line_2_text[:16],
    }
    return json.dumps(msg)


def format_time_string(time_left: tuple[int, int, int, int]) -> str:
    """Create a formatted time string to fit the display from the remaining time tuple given by the TimeManager

    Args:
        time_left (tuple): Output from TimeManager.get_remaining_time()

    Returns:
        str: Display text
    """
    return f"{str(time_left[1]).zfill(2)}:{str(time_left[2]).zfill(2)}:{str(time_left[3]).zfill(2)}"
