from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # Get the API key for Mistral


def get_response(user_question, chat_history):
    """Function that call the LLM and get an answer"""

    template = """
        Tu es un super assistant. Repond aux questions de l'utilisateur en utilisant l'historique de conversation qui t'est donne. 

        Historique de converation : {chat_history}

        Question de l'utilisateur: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatMistralAI(model_name="open-mistral-7b")
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"chat_history": chat_history, "user_question": user_question})


# Initialise chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Enedis ChatBot", page_icon="🤖")
st.title("Enedis ChatBot")


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

user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(
            get_response(user_query, st.session_state.chat_history)
        )
    st.session_state.chat_history.append(AIMessage(content=ai_response))
