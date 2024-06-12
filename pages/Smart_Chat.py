import sys
import os
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ChatMessage,
    FunctionMessage,
    ToolMessage,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from typing import List, Union

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from tools.find_interesting_docs import (
    trouver_des_documents_interessant,
    rechercher_une_information_dans_un_pdf,
)


_ = load_dotenv(find_dotenv())  # Get the API key for Mistral


def get_response(user_question, chat_history):
    """
    Function that call the LLM and get an answer
    """
    # prompt = hub.pull("hwchase17/openai-tools-agent")
    my_system_prompt_message = """
    Tu es un super assistant qui travail pour un gestionnaire de reseaux d'electricite.
    Ton objectif est d'aider l'utilisateur en lui fournissant de l'information et en repondant a ses questions.
    Repond aux questions de l'utilisateur en utilisant l'historique de conversation.
    Tu peux t'aider de tes outils.
    """.strip()
    prompt = ChatPromptTemplate(
        input_variables=["agent_scratchpad", "input", "chat_history"],
        input_types={
            "chat_history": List[
                Union[
                    AIMessage,
                    HumanMessage,
                    ChatMessage,
                    SystemMessage,
                    FunctionMessage,
                    ToolMessage,
                ]
            ],
            "agent_scratchpad": List[
                Union[
                    AIMessage,
                    HumanMessage,
                    ChatMessage,
                    SystemMessage,
                    FunctionMessage,
                    ToolMessage,
                ]
            ],
        },
        messages=[
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=[], template=my_system_prompt_message
                )
            ),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(input_variables=["input"], template="{input}")
            ),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ],
    )
    llm = ChatMistralAI(model_name="mistral-large-latest")
    tools = [trouver_des_documents_interessant, rechercher_une_information_dans_un_pdf]
    agent = create_tool_calling_agent(llm, tools, prompt)  # type: ignore
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # type: ignore

    return agent_executor.stream({"chat_history": chat_history, "input": user_question})


def stream_ai(user_question, chat_history):
    ai = get_response(user_question, chat_history)
    for word in ai:
        if "output" not in word:
            continue
        for token in word["output"]:
            yield token


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
            stream_ai(user_query, st.session_state.chat_history)
        )
    st.session_state.chat_history.append(AIMessage(content=ai_response))
