from open_ai.RAG_OpenAI import RAG_OpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
import pytest


@pytest.fixture()
def rag():
    rag = RAG_OpenAI("vdb_enedis")
    yield rag


def test_no_function_call(rag):
    """
    Test the RAG_OpenAI class without calling any function
    """
    reponse = rag.ask_question("Bonjour !")
    assert len(reponse) > 1
    assert isinstance(reponse[-1].content, str)
    for message in reponse:
        assert not isinstance(message, ToolMessage)


def test_function_call(rag):
    """
    Test the RAG_OpenAI class with calling a function
    """
    reponse = rag.ask_question(
        "Quel est le role d'Enedis dans le comptage de l'électricité en France ?"
    )
    assert len(reponse) > 1
    assert isinstance(reponse[-1].content, str)
    assert sum([1 for message in reponse if isinstance(message, ToolMessage)]) > 0
