#install streamlit dotenv langchain openai
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI #will be using huggingface instead afterwards
from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    load_dotenv()
    if os.getenv("OPEN_AI_KEY") is None or os.getenv("OPEN_AI_KEY") == "":
        print("OPEN_AI_KEY is not set")
        exit(1)
    else:
        print("OPEN_AI_KEY is set")


    st.set_page_config(
        page_title="Your AI",
        page_icon=":shark:"
    )

def main():
    init()

    chat = ChatOpenAI(temperature=0.7)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="Thank")
    ]

    st.header("Your AI :shark:")

    with st.sidebar:
        user_input = st.text_input("Your message:", key="user_input")

        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

    messages=st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if i & 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')



if __name__ == '__main__':
    main()
