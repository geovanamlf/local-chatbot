# 🧠 Local Chatbot with Ollama + Streamlit

Hey, i'm Geovana, and this is a simple local chatbot i built using [Ollama](https://ollama.com) and [Streamlit](https://streamlit.io).  

The goal was to create a lightweight, fast chatbot that runs 100% locally — no APIs, no cloud, just Python.

## 🔧 Technologies Used

- 🐍 Python
- 🖥️ Ollama (running `gemma:2b`)
- 🎈 Streamlit (for the UI)
- 💥 Subprocess (to run commands in the shell)

## ⚙️ How to Run

1. **Clone the repository:**
    ```bash
    git clone git@github.com:geovanamlf/local-chatbot.git
    cd local-chatbot
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the chatbot:**
    ```bash
    streamlit run chatbot.py
    ```

⚠️ Make sure you have [Ollama](https://ollama.com/download) installed and running with the `gemma:2b` model pulled.

## 🤖 About the Project

This was a personal experiment to understand how local LLMs work and to practice combining backend tools with a frontend framework like Streamlit.
