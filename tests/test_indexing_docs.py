from indexing.indexing_pdf import IndexingPdfData
from indexing.indexing_csv import IndexingCSV
import pytest
import os
from langchain_core.documents.base import Document
from langchain_community.vectorstores.faiss import FAISS
import shutil


@pytest.fixture()
def generate_index_pdf():
    index = IndexingPdfData()
    yield index


@pytest.fixture()
def generate_index_csv():
    index = IndexingCSV(load_existing=False)
    yield index


def test_parse_one_pdf(generate_index_pdf):
    """
    Test the parse one pdf function
    """
    size_db = 0
    if generate_index_pdf.db is not None:
        size_db = len(generate_index_pdf.db.docstore._dict)
    generate_index_pdf.parse_one_pdf(
        "https://www.enedis.fr/media/2164/download", "Enedis-NMO-CF_007E.pdf"
    )
    assert generate_index_pdf.db is not None
    assert len(generate_index_pdf.db.docstore._dict) > size_db


def test_save_vdb_to_file(generate_index_pdf):
    """
    Test the save vdb to file function
    """
    generate_index_pdf.parse_one_pdf(
        "https://www.enedis.fr/media/2164/download", "Enedis-NMO-CF_007E.pdf"
    )
    # generate_index_pdf.create_vector_database()
    test_dir = "__test1_faiss_index"
    generate_index_pdf.save_vdb_to_file(test_dir)
    assert os.path.isdir(test_dir)
    shutil.rmtree(test_dir)


def test_load_vdb_from_file(generate_index_pdf):
    """
    Test the load vdb from file function
    """
    generate_index_pdf.parse_one_pdf(
        "https://www.enedis.fr/media/2164/download", "Enedis-NMO-CF_007E.pdf"
    )
    # generate_index_pdf.create_vector_database()
    test_dir = "__test2_faiss_index"
    generate_index_pdf.save_vdb_to_file(test_dir)
    generate_index_pdf.db = None
    assert generate_index_pdf.db is None
    generate_index_pdf.load_vdb_from_file(test_dir)
    assert generate_index_pdf.db is not None
    assert isinstance(generate_index_pdf.db, FAISS)
    shutil.rmtree(test_dir)


def test_similarity_search(generate_index_pdf):
    """
    Test the similarity search function
    """
    generate_index_pdf.parse_one_pdf(
        "https://www.enedis.fr/media/2164/download", "Enedis-NMO-CF_007E.pdf"
    )
    # generate_index_pdf.create_vector_database()
    docs = generate_index_pdf.similarity_search("electricite")
    assert isinstance(docs, list)
    if len(docs) > 0:
        assert isinstance(docs[0], Document)


def test_parse_csv(generate_index_csv):
    """
    Test the parse function for csv
    """
    generate_index_csv.parse_csv()
    test_key = {"page_content": [], "metadata": [], "type": []}
    assert len(generate_index_csv.docs) > 0
    assert isinstance(generate_index_csv.docs[0], Document)
    assert generate_index_csv.docs[0].__dict__.keys() == test_key.keys()


def test_csv_create_vector_database(generate_index_csv):
    """
    Test the create vector database function for csv
    """
    generate_index_csv.parse_csv()
    generate_index_csv.docs = generate_index_csv.docs[:5]
    generate_index_csv.create_vector_database()
    assert generate_index_csv.db is not None


def test_csv_save_vdb_to_file(generate_index_csv):
    """
    Test the save vdb to file function for csv
    """
    generate_index_csv.parse_csv()
    generate_index_csv.docs = generate_index_csv.docs[:5]
    generate_index_csv.create_vector_database()
    test_dir = "__test1_faiss_index_csv"
    generate_index_csv.save_vdb_to_file(test_dir)
    assert os.path.isdir(test_dir)
    shutil.rmtree(test_dir)


def test_csv_load_vdb_from_file(generate_index_csv):
    """
    Test the load vdb from file function for csv
    """
    generate_index_csv.parse_csv()
    generate_index_csv.docs = generate_index_csv.docs[:5]
    generate_index_csv.create_vector_database()
    test_dir = "__test2_faiss_index_csv"
    generate_index_csv.save_vdb_to_file(test_dir)
    generate_index_csv.db = None
    assert generate_index_csv.db is None
    generate_index_csv.load_vdb_from_file(test_dir)
    assert generate_index_csv.db is not None
    assert isinstance(generate_index_csv.db, FAISS)
    shutil.rmtree(test_dir)


def test_csv_similarity_search(generate_index_csv):
    """
    Test the similarity search function for csv
    """
    generate_index_csv.parse_csv()
    generate_index_csv.docs = generate_index_csv.docs[:5]
    generate_index_csv.create_vector_database()
    docs = generate_index_csv.similarity_search("electricite")
    assert isinstance(docs, list)
    if len(docs) > 0:
        assert isinstance(docs[0], Document)
