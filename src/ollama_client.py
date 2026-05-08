import subprocess


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
        result = subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return []

        lines = result.stdout.splitlines()[1:]
        models = []

        for line in lines:
            if line.strip():
                model_name = line.split()[0]
                models.append(model_name)

        return models

    except Exception:
        return []


def stream_ollama(messages, model, system_prompt):
    context = build_context(messages, system_prompt)

    try:
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        process.stdin.write(context)
        process.stdin.close()

        for line in process.stdout:
            yield line

        process.wait()

        if process.returncode != 0:
            error_message = process.stderr.read()

            yield f"\n\nError running Ollama:\n\n{error_message}"

    except FileNotFoundError:
        yield "Ollama is not installed or could not be found on this system."

    except Exception as e:
        yield f"Unexpected error:\n\n{str(e)}"