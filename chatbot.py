import streamlit as st
from pathlib import Path

from src.ollama_client import (
    stream_ollama,
    get_available_models
)

from src.chat_storage import (
    load_messages,
    save_messages,
    clear_messages,
    export_chat_markdown
)


MAX_CONTEXT_MESSAGES = 20


@st.cache_data
def cached_models():
    return get_available_models()


def load_css():
    css_file = Path("styles/main.css")

    if css_file.exists():
        with open(css_file) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


st.set_page_config(
    page_title="Geo Local Chatbot",
    page_icon="◐",
    layout="centered"
)

load_css()

st.title("Geo Local Chatbot")
st.caption("Private, fast and fully local AI chat powered by Ollama.")


if "messages" not in st.session_state:
    st.session_state.messages = load_messages()

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""


models = cached_models()
has_models = bool(models)


with st.sidebar:
    st.title("Settings")

    if has_models:
        selected_model = st.selectbox(
            "Model",
            models
        )

        st.caption(f"Active model: {selected_model}")

    else:
        selected_model = None

        st.error("No Ollama models found.")
        st.caption(
            "Make sure Ollama is running and at least one model is installed."
        )

        if st.button("Retry connection", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

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

    export_content = export_chat_markdown(
        st.session_state.messages
    )

    st.download_button(
        label="Export Chat",
        data=export_content,
        file_name="geo_local_chat.md",
        mime="text/markdown",
        use_container_width=True
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
        "Start a conversation with your local assistant."
    )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            message["content"],
            unsafe_allow_html=False
        )


if prompt := st.chat_input(
    "Type your message...",
    disabled=not has_models
):
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

        with st.spinner("Generating response..."):
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