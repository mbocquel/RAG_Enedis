from open_ai.RAG_OpenAI import RAG_OpenAI
import streamlit as st
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

if "rag_openai" not in st.session_state:
    st.session_state.rag_openai = RAG_OpenAI("vdb_enedis")


if "chat_history_openai" not in st.session_state:
    st.session_state.chat_history_openai = []

st.title("RAG with OpenAI API and LangGraph")

# Conversation
for message in st.session_state.chat_history_openai:
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
    st.session_state.chat_history_openai.append(HumanMessage(content=user_query))
    with st.chat_message("AI"):
        ai_response = st.write_stream(
            st.session_state.rag_openai.ask_question_stream(user_query)
        )
    st.session_state.chat_history_openai.append(AIMessage(content=ai_response))
