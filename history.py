import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except:
        return []


def save_analysis(email, symptoms, result):

    history = load_history()

    # Make sure result is saved as simple text
    if isinstance(result, dict):
        result = result.get(
            "condition",
            "No clear result"
        )

    elif isinstance(result, list):

        if len(result) > 0 and isinstance(
            result[0], dict
        ):
            result = result[0].get(
                "condition",
                "No clear result"
            )
        else:
            result = str(result)

    record = {
        "email": email,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "symptoms": symptoms,
        "result": str(result)
    }

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(
            history,
            file,
            indent=4
        )


def get_user_history(email):

    history = load_history()

    return [
        record
        for record in history
        if record.get("email") == email
    ]