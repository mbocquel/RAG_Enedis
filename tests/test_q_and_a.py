from q_and_a.q_and_a import QAndA
import pytest
from indexing.indexing_pdf import IndexingPdfData
import time


indexing = IndexingPdfData()
indexing.parse_one_pdf(
    "https://www.enedis.fr/media/2057/download", "Enedis-NOI-RES_46E.pdf"
)
# indexing.create_vector_database()


@pytest.fixture()
def generate_q_and_a():
    q_and_a = QAndA(indexing)
    yield q_and_a


def test_ask_question(generate_q_and_a):
    """
    Test the ask question method
    """
    time.sleep(5)
    query = "D'apres le code de l'energie, qui est responsable du comptage de l'electricite sur le reseau de distribution ?"
    answer = generate_q_and_a.ask_question(query, save_history=False)
    expected_answer_struct = {
        "input_documents": [],
        "question": "the question of type str",
        "output_text": "the output texte of type str",
    }
    assert isinstance(answer, dict)
    assert answer.keys() == expected_answer_struct.keys()
    assert answer["question"] == query
    assert isinstance(answer["output_text"], str)
    assert generate_q_and_a.history == []


def test_get_history(generate_q_and_a):
    """
    Test the get_history method
    """
    time.sleep(5)
    query_1 = "D'apres le code de l'energie, qui est responsable du comptage de l'electricite sur le reseau de distribution ?"
    answer_1 = generate_q_and_a.ask_question(query_1, save_history=True)
    time.sleep(5)
    query_2 = (
        "Quelle est la démarche d’instruction du schéma de Raccordement et de Comptage?"
    )
    answer_2 = generate_q_and_a.ask_question(query_2, save_history=True)
    time.sleep(5)
    query_3 = "Quelles sont les differentes fonctions de comptage qui existent ?"
    answer_3 = generate_q_and_a.ask_question(query_3, save_history=True)

    history_1 = generate_q_and_a.get_history()
    assert history_1 == [answer_1, answer_2, answer_3]

    history_2 = generate_q_and_a.get_history(index_start=1)
    assert history_2 == [answer_2, answer_3]

    history_3 = generate_q_and_a.get_history(index_end=1)
    assert history_3 == [answer_1, answer_2]

    history_4 = generate_q_and_a.get_history(index_start=1, index_end=1)
    assert history_4 == [answer_2]

    history_5 = generate_q_and_a.get_history(index_start=0, index_end=10)
    assert history_5 == [answer_1, answer_2, answer_3]

    history_6 = generate_q_and_a.get_history(index_start=3, index_end=10)
    assert history_6 == []

    history_7 = generate_q_and_a.get_history(index_start=2, index_end=1)
    assert history_7 == []


def test_clear_history(generate_q_and_a):
    """
    Test the clear_history method
    """
    time.sleep(5)
    query_1 = "D'apres le code de l'energie, qui est responsable du comptage de l'electricite sur le reseau de distribution ?"
    generate_q_and_a.ask_question(query_1, save_history=True)

    assert len(generate_q_and_a.history) > 0
    generate_q_and_a.clear_history()
    assert len(generate_q_and_a.history) == 0


def test_question_off_topic(generate_q_and_a):
    """
    Test the q and a with an off topic question
    """
    time.sleep(5)
    query = (
        "Quel est le meilleur candidat pour les elections europeennes de juin 2024 ?"
    )
    answer = generate_q_and_a.ask_question(query)
    assert answer["output_text"].strip() == "HORS SUJET"
