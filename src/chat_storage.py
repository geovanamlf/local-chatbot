import json
from pathlib import Path


CHAT_FILE = Path("data/chat_history.json")

MAX_SAVED_MESSAGES = 40


def load_messages():
    try:
        if not CHAT_FILE.exists():
            return []

        with open(CHAT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception:
        return []


def save_messages(messages):
    try:
        limited_messages = messages[-MAX_SAVED_MESSAGES:]

        with open(CHAT_FILE, "w", encoding="utf-8") as file:
            json.dump(
                limited_messages,
                file,
                ensure_ascii=False,
                indent=2
            )

    except Exception:
        pass


def clear_messages():
    try:
        with open(CHAT_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

    except Exception:
        pass


def export_chat_markdown(messages):
    markdown = "# Geo Local Chatbot Export\n\n"

    for message in messages:
        role = (
            "User"
            if message["role"] == "user"
            else "Assistant"
        )

        content = message["content"]

        markdown += f"## {role}\n\n"
        markdown += f"{content}\n\n"

    return markdown