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
from dotenv import load_dotenv, find_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from typing import List, Union
from mistral_ai.tool_find_interesting_docs import (
    find_context_to_answer_a_question,
    list_interesting_documents,
)


class MistralRAGLangChain:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.my_system_prompt_message = """
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
        self.prompt = ChatPromptTemplate(
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
                        input_variables=[], template=self.my_system_prompt_message
                    )
                ),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(input_variables=["input"], template="{input}")
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ],
        )
        self.tools = [list_interesting_documents, find_context_to_answer_a_question]
        self.llm = ChatMistralAI(
            model_name="mistral-large-latest", verbose=True
        ).bind_tools(self.tools)
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)  # type: ignore
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)  # type: ignore

    def get_response(self, user_question, chat_history):
        """Get response from the agent."""
        return self.agent_executor.stream(
            {"chat_history": chat_history, "input": user_question}
        )

    def stream_ai(self, user_question, chat_history):
        ai = self.get_response(user_question, chat_history)
        for word in ai:
            if "output" not in word:
                continue
            for token in word["output"]:
                yield token
