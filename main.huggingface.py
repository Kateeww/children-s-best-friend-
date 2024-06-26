#install streamlit dotenv transformer langchain huggingface_hub
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from transformers import pipeline

def init():
    load_dotenv()
    if os.getenv("AI_KEY") is None or os.getenv("AI_KEY") == "":
        print("AI_KEY is not set")
        exit(1)
    else:
        print("AI_KEY is set")


    st.set_page_config(
        page_title="Your AI",
        page_icon=":shark:"
    )

def main():
    init()

    chat_pipeline = pipeline(
        "conversational",
        model="microsoft/DialoGPT-medium",
        device=0 if st.sidebar.checkbox("Use GPU") else -1 
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Thank"}
        ]

    st.header("Your AI :shark:")

    with st.sidebar:
        user_input = st.text_input("Your message:", key="user_input")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = chat_pipeline([msg["content"] for msg in st.session_state.messages], return_prompt=False)
            st.session_state.messages.append({"role": "assistant", "content": response[0]['generated_text']})

    messages=st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if i & 2 == 0:
            message(msg['content'], is_user=True, key=str(i) + '_user')
        else:
            message(msg['content'], is_user=False, key=str(i) + '_ai')

if __name__ == '__main__':
    main()
