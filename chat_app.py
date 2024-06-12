from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.tools import tool
import requests
from pydantic import BaseModel, Field
import datetime


@tool()
def get_current_temperature(latitude: float, longitude: float) -> str:
    """Fetch current temperature for given coordinates."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # Parameters for the request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1,
    }

    # Make the request
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.utcnow()
    time_list = [
        datetime.datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        for time_str in results["hourly"]["time"]
    ]
    temperature_list = results["hourly"]["temperature_2m"]

    closest_time_index = min(
        range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time)
    )
    current_temperature = temperature_list[closest_time_index]

    return f"The current temperature is {current_temperature}°C"


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
