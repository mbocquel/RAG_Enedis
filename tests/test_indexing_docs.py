from indexing.indexing_data import IndexingPdfData
import pytest
import tempfile
import pandas as pd
import os
import langchain_core
import langchain_community
import random


@pytest.fixture()
def generate_pd():
    data = [
        "https://www.enedis.fr/media/4107/download",
        "Référentiel clientèle",
        "2024-05-21T09:03:25+02:00",
        "Suite à la délibération de la CRE n° 2024-42 du 15 février 2024; relative à la mise en œuvre de la généralisation des options tarifaires à 4 plages temporelles du TURPE HTA-BT; cette procédure a pour objectif de préciser les modalités de mise en œuvre de la généralisation de l'option tarifaire à 4 plages temporelles.",
        "Enedis-NMO-CF_007E.pdf",
        "fichier PDF",
        "1.45 Mo"
    ]
    df = pd.DataFrame(data, columns=['url', 'type', "date", "content", "file_name", "file_type", "file_size"])
    print("toto ", random.random())
    indexing = IndexingPdfData(df)
    yield indexing


def test_parse_one_pdf(generate_pd):
    """
    Test the parse one pdf function
    """
    generate_pd.parse_one_pdf()
    test_key = {
        'page_content': [], 
        'metadata': [],
        'type':[]
    }
    assert len(generate_pd.docs) > 0
    assert type(generate_pd.docs[0]) == langchain_core.documents.base.Document
    assert generate_pd.docs[0].__dict__.keys() == test_key.keys()



def test_create_vector_database(generate_pd):
    """
    Test the create vector database function
    """
    generate_pd.parse_one_pdf()
    generate_pd.create_vector_database()
    assert generate_pd.db is not None


def test_save_vdb_to_file(generate_pd):
    """
    Test the save vdb to file function
    """
    generate_pd.parse_one_pdf()
    generate_pd.create_vector_database()
    test_dir = tempfile.TemporaryDirectory()
    tmp_file_name = os.path.join(test_dir.name, f'db')
    generate_pd.save_vdb_to_file(tmp_file_name)
    assert os.path.isfile(tmp_file_name)
    os.remove(tmp_file_name)


def test_load_vdb_from_file(generate_pd):
    """
    Test the load vdb from file function
    """
    generate_pd.parse_one_pdf()
    generate_pd.create_vector_database()
    test_dir = tempfile.TemporaryDirectory()
    tmp_file_name = os.path.join(test_dir.name, f'db')
    generate_pd.save_vdb_to_file(tmp_file_name)
    generate_pd.db = None
    assert generate_pd.db is None
    generate_pd.load_vdb_from_file(tmp_file_name)
    assert generate_pd.db is not None
    assert type(generate_pd) == langchain_community.vectorstores.faiss.FAISS
    os.remove(tmp_file_name)


def test_similarity_search(generate_pd):
    """
    Test the similarity search function 
    """
    generate_pd.parse_one_pdf()
    generate_pd.create_vector_database()
    docs = generate_pd.similarity_search("electricite")
    assert type(docs) == list
    if len(docs) > 0:
        assert type(docs[0]) == langchain_core.documents.base.Document
    

