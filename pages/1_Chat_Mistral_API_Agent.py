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
    find_context_to_answer_a_question,
    list_interesting_documents,
)

st.set_page_config(page_title="RAG with Mistral API and LangChain", page_icon="🤖")


_ = load_dotenv(find_dotenv())  # Get the API key for Mistral


def get_response(user_question, chat_history):
    """
    Function that call the LLM and get an answer
    """

    my_system_prompt_message = """
    **Role:**
        - You are a multilangual AI-powered assistant working for an electricity network manager.
        - You need to use the same language as the user. For example, if the user start by saying 'Bonjour' you need to answer in French.

    **Tools Available:**
        - list_interesting_documents:
            *Purpose:* Use this tool to provide users with a list of relevant documents.
            *When to Use:* When a user requests a list of documents.
            *Example:* If a user asks, "Can you provide me with documents about renewable energy integration?", use this tool to fetch the list.
            
        - find_context_to_answer_a_question:
            *Purpose:* Use this tool to gather context and answer specific user questions.
            *When to Use:* When a user asks a specific question that requires detailed information.
            *Example:* If a user asks, "How does the electricity grid handle peak loads?", use this tool to find the relevant context and provide an answer.
    
    **Important Rules:**
        - *No Personal Knowledge:* Never answer a user's question using your own knowledge.
        - *Always Use Tools:* Always use the tools to find information and indicate which documents or contexts were used to answer the question.
        - *Provide Sources:* Always cite the specific documents or sources used to answer a question.
        - *Response Language:* Respond in the same language as the user's question.

    **Example Interaction:**
        User: "What are the latest advancements in smart grid technology?"
        Assistant:
            Use find_context_to_answer_a_question to gather the latest information.
            Provide the answer based on the gathered context.
            Cite the specific documents or sources used.
    
    **Reminder:**
        Your goal is to provide accurate and sourced information by leveraging the available tools.
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
    llm = ChatMistralAI(model_name="mistral-large-latest", verbose=True)
    tools = [list_interesting_documents, find_context_to_answer_a_question]
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

st.title("Enedis ChatBot")

st.markdown(
    """
### Issues with the bot: 
- *The bot is good at calling the first tool, to get a list of documents, but it is not able to call the second tool to get the answer from the document.*
- *Instead it says that it's calling the second tool and print the tool calling instructions but never actually calls it. And then it makes up an answer.*
- *There are some hallucination with wrong URL"""
)

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
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(
            stream_ai(user_query, st.session_state.chat_history)
        )
    st.session_state.chat_history.append(AIMessage(content=ai_response))
