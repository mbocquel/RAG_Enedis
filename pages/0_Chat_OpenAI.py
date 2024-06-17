from open_ai.RAG_OpenAI import RAG_OpenAI
import streamlit as st
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)


rag = RAG_OpenAI("vdb_enedis")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("RAG with OpenAI API and LangGraph")

# Conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message(
            "Human",
        ):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

user_query = st.chat_input("Votre message")
if user_query is not None and user_query != "":
    with st.chat_message("Human"):
        st.markdown(user_query)
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("AI"):
        ai_response = st.write_stream(rag.ask_question(user_query))
    st.session_state.chat_history.append(AIMessage(content=ai_response))
