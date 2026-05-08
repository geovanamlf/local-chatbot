import json
import requests


OLLAMA_API_URL = "http://localhost:11434/api/generate"


def build_context(messages, system_prompt):
    context = ""

    if system_prompt.strip():
        context += f"System: {system_prompt}\n\n"

    for message in messages:
        role = "User" if message["role"] == "user" else "Assistant"
        content = message["content"]

        context += f"{role}: {content}\n"

    context += "Assistant:"

    return context


def get_available_models():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return [
            model["name"]
            for model in data.get("models", [])
        ]

    except Exception:
        return []


def stream_ollama(messages, model, system_prompt):
    context = build_context(messages, system_prompt)

    payload = {
        "model": model,
        "prompt": context,
        "stream": True
    }

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")

                data = json.loads(decoded_line)

                chunk = data.get("response", "")

                if chunk:
                    yield chunk

    except requests.exceptions.ConnectionError:
        yield "Could not connect to Ollama. Make sure Ollama is running."

    except requests.exceptions.Timeout:
        yield "The request timed out."

    except Exception as e:
        yield f"Unexpected error:\n\n{str(e)}"