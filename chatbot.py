import streamlit as st
from pathlib import Path

from src.ollama_client import (
    stream_ollama,
    get_available_models
)

from src.chat_storage import (
    load_messages,
    save_messages,
    clear_messages
)


MAX_CONTEXT_MESSAGES = 20


@st.cache_data
def cached_models():
    return get_available_models()


def load_css():
    css_file = Path("styles/main.css")

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


st.set_page_config(
    page_title="Geo Local Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("Geo Local Chatbot 🤖")
st.caption("Local LLM chat powered by Ollama")


if "messages" not in st.session_state:
    st.session_state.messages = load_messages()

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""


models = cached_models()


with st.sidebar:
    st.title("Settings")

    if not models:
        st.error("No Ollama models found.")

    selected_model = st.selectbox(
        "Model",
        models if models else ["No models available"]
    )

    st.success(f"Using: {selected_model}")

    st.divider()

    with st.expander("System Prompt"):
        system_prompt = st.text_area(
            "Assistant behavior",
            value=st.session_state.system_prompt,
            height=150,
            placeholder="You are a helpful assistant..."
        )

        st.session_state.system_prompt = system_prompt

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Messages",
            len(st.session_state.messages)
        )

    with col2:
        st.metric(
            "Context",
            MAX_CONTEXT_MESSAGES
        )

    st.divider()

    if st.button(
        "New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []

        clear_messages()

        st.rerun()


if not st.session_state.messages:
    st.info(
        "Start a conversation with your local AI assistant."
    )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            message["content"],
            unsafe_allow_html=False
        )


if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_messages(st.session_state.messages)

    with st.chat_message("user"):
        st.markdown(prompt)

    assistant_reply = ""

    recent_messages = st.session_state.messages[-MAX_CONTEXT_MESSAGES:]

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        for chunk in stream_ollama(
            recent_messages,
            selected_model,
            st.session_state.system_prompt
        ):
            assistant_reply += chunk

            response_placeholder.markdown(
                assistant_reply + "▌",
                unsafe_allow_html=False
            )

        assistant_reply = assistant_reply.strip()

        response_placeholder.markdown(
            assistant_reply,
            unsafe_allow_html=False
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    save_messages(st.session_state.messages)