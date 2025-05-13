import streamlit as st
import subprocess

st.title("Geo Local ChatGPT - Chatbot com Ollama 🤖")

# initializing message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# displaying message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# fun to run ollama model with subprocess
def run_ollama(model_input):
    result = subprocess.run(
        ["ollama", "run", "gemma:2b"],
        input=model_input,  # Passando a entrada aqui
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

# rec user input
if prompt := st.chat_input("Escreva algo..."):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # dsp user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # getting response from model
    assistant_reply = run_ollama(prompt)
    
    # assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

