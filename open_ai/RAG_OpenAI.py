"""
This module is a wrapper around the OpenAI Chat API to implement a RAG (Retrieval Augmented Generation) model.
"""

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from indexing.indexing_pdf import IndexingPdfData
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage, AIMessage
import operator
from typing import Literal, TypedDict, Annotated
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
import random
from typing import List
from langchain_core.documents.base import Document


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class FindContextToAnswerQuestion(BaseModel):
    """Call this with a question to get some context that you will use to answer the user question"""

    question: str = Field(description="The question you want to answer")


class Agent:
    def __init__(self, model, tools, checkpointer, system_prompt="") -> None:
        self.tool_node = ToolNode(tools)
        self.model = model.bind_tools(tools)
        self.checkpointer = checkpointer
        self.system_prompt = system_prompt
        # Define a new graph
        self.workflow = StateGraph(MessagesState)
        # Define the two nodes we will cycle between
        self.workflow.add_node("llm", self.call_model)
        self.workflow.add_node("tools", self.tool_node)
        self.workflow.set_entry_point("llm")
        self.workflow.add_conditional_edges("llm", self.should_continue)
        self.workflow.add_edge("tools", "llm")
        self.app = self.workflow.compile(checkpointer=self.checkpointer)

    def should_continue(self, state: AgentState) -> Literal["tools", END]:  # type: ignore
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, then we route to the "tools" node
        if last_message.tool_calls:  # type: ignore
            print("\033[1;31mRouting to tools\033[0m")
            return "tools"
        # Otherwise, we stop (reply to the user)
        print("\033[1;32mEnd of the LangGraph workflow\033[0m")
        return END

    def call_model(self, state: AgentState):
        messages = state["messages"]
        if self.system_prompt:
            messages = [SystemMessage(content=self.system_prompt)] + messages
        print("\033[1;36mCalling model\033[0m")
        response = self.model.invoke(messages)
        print("\033[1;33mGot : ", response, "\033[0m")
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}


class RAG_OpenAI:
    """
    Class that manage the communication with the OpenAI Model in implement a RAG
    """

    def __init__(self, path_vdb="") -> None:
        _ = load_dotenv(find_dotenv())
        self.index = IndexingPdfData()
        if path_vdb:
            self.index.load_vdb_from_file(path_vdb)
        self.find_context_function = StructuredTool.from_function(
            func=self.find_context_to_answer_a_question,
            name="FindContextToAnswerQuestion",
            description="Call this with a question to get some context that you will use to answer the user question",
            args_schema=FindContextToAnswerQuestion,
        )
        self.thread_id = random.randint(0, 50)
        self.system_prompt = """
        Role:
            - You are a multilangual smart research assistant
            - You need to use the same language as the user.
            - You need to provide accurate and sourced information by leveraging the available tools.

        Important Rules:
            - No Personal Knowledge: Never answer a user's question using your own knowledge.
            - Provide Sources: Always cite the specific documents or sources used to answer a question.
            - Response Language: Respond in the same language as the user's question.
        If you need to look up some information before asking a follow up question, you are allowed to do that!
        """
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.model = ChatOpenAI()
        self.bot = Agent(
            model=self.model,
            tools=[self.find_context_function],
            checkpointer=self.memory,
            system_prompt=self.system_prompt,
        )

    def find_context_to_answer_a_question(self, question: str) -> List[Document]:
        """Find context to answer a question"""
        return self.index.similarity_search(question, k=5)

    # def ask_question(self, question: str) -> List[AnyMessage]:
    #     """Ask a question to the bot"""
    #     response = self.bot.app.invoke(
    #         {"messages": [HumanMessage(content=question)]},
    #         config={"configurable": {"thread_id": self.thread_id}},
    #     )
    #     return response["messages"]

    def ask_question(self, question: str):
        """Ask a question to the bot and stream the response"""
        for response in self.bot.app.stream(
            {"messages": [HumanMessage(content=question)]},
            config={"configurable": {"thread_id": 1}},
        ):
            if "llm" in response:
                for message in response["llm"].get("messages"):
                    if isinstance(message, AIMessage):
                        for token in message.content:
                            yield token
