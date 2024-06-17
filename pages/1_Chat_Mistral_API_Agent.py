from mistral_ai.RAG_Mistal import MistralRAGLangChain
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage


st.set_page_config(page_title="RAG with Mistral API and LangChain", page_icon="🤖")

rag = MistralRAGLangChain()

# Initialise chat history
if "chat_history_mistral" not in st.session_state:
    st.session_state.chat_history_mistral = []

st.title("RAG with Mistral API and LangChain")

st.markdown(
    """
### Issues with the bot: 
- *The bot is good at calling the first tool, to get a list of documents, but it is not able to call the second tool to get the answer from the document.*
- *Instead it says that it's calling the second tool and print the tool calling instructions but never actually calls it. And then it makes up an answer.*
- *There are some hallucination with wrong URL"""
)

# Conversation
for message in st.session_state.chat_history_mistral:
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
    st.session_state.chat_history_mistral.append(HumanMessage(content=user_query))
    with st.chat_message("AI"):
        ai_response = st.write_stream(
            rag.stream_ai(user_query, st.session_state.chat_history_mistral)
        )
    st.session_state.chat_history_mistral.append(AIMessage(content=ai_response))
