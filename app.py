import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config.config import GOOGLE_API_KEY
from models.llm import get_chatgemini_model
from utils.retrieval import retrieve_relevant_docs
from utils.search import web_search

def get_chat_response(chat_model, messages, system_prompt):
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        response = chat_model.invoke(formatted_messages)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

def instructions_page():
    st.title("The Chatbot Blueprint Instructions")
    st.markdown("Follow the setup to configure API keys and use the chatbot.")

def chat_page():
    st.title("🤖 AI ChatBot")
    chat_model = get_chatgemini_model()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mode" not in st.session_state:
        st.session_state.mode = "Concise"

    mode = st.sidebar.selectbox("Response Mode", ["Concise", "Detailed"], index=0)
    st.session_state.mode = mode

    system_prompt = f"You are a helpful assistant. Answer in a {mode.lower()} manner."

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Getting response..."):
                docs = []
                if "retrieve" in prompt.lower():
                    docs = retrieve_relevant_docs(prompt)
                    st.markdown("**References:**")
                    for d in docs:
                        st.markdown(d)

                search_results = []
                if "search" in prompt.lower():
                    search_results = web_search(prompt)
                    st.markdown("**Web Results:**")
                    for res in search_results:
                        st.markdown(res)

                response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(page_title="AI Chatbot", layout="wide")
    with st.sidebar:
        page = st.radio("Navigation", ["Chat", "Instructions"])
        if page == "Chat":
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()
    if page == "Chat":
        chat_page()
    else:
        instructions_page()

if __name__ == "__main__":
    main()
