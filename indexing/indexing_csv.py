import os
from langchain_community.document_loaders import CSVLoader
from dotenv import load_dotenv, find_dotenv
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from typing import List
from configs.CFG import CFG
from configs.config import Config
import logging
import pandas as pd

logger = logging.getLogger(__name__)
handler = logging.FileHandler(f"logs/{__name__}.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class IndexingCSV:
    """
    This class is necessary to find documents related to a topic from a csv file that has a summary of the documents.
    It recieve a dataframe with the URL of some PDF files as well as some information on these files.
    The class download these files, parses the pdf to text, cut the text into small
    chunks of data, embed the text into a vector using HuggingFaceEmbeddings
    """

    def __init__(self, load_existing=True) -> None:
        self.config = Config.from_json(CFG).indexing_csv
        if not os.path.isfile(self.config.csv_doc_path):
            raise FileNotFoundError("Wrong vector database path")
        self.dataframe = pd.read_csv(self.config.csv_doc_path, index_col=0)
        self.docs = []
        self.db = None
        self.embeddings = HuggingFaceEmbeddings()
        if os.path.isdir(self.config.csv_vdb_path) and load_existing:
            self.load_vdb_from_file(self.config.csv_vdb_path)
        self.loader = CSVLoader(self.config.csv_doc_path)
        logger.info("IndexingCSV initialised")

    def parse_csv(self) -> List[Document]:
        """Parse the CSV into a list of Documents"""
        self.docs = self.loader.load()
        self.create_vector_database()
        return self.docs

    def create_vector_database(self) -> FAISS:
        """
        Create the vector database using FAISS from the extracted documents
        """
        if len(self.docs) == 0:
            raise Exception("Impossible to create a database. There is no documents")
        _ = load_dotenv(find_dotenv())
        logger.info("HuggingFace token loaded from .env file")
        self.db = FAISS.from_documents(self.docs, self.embeddings)
        return self.db

    def save_vdb_to_file(self, path: str) -> None:
        """
        Save the vector database to a file for future use
        """
        if self.db is None:
            return
        logger.info(f"Vector database saved localy in {path}")
        self.db.save_local(path)

    def load_vdb_from_file(self, path: str) -> FAISS:
        """
        Load a vector database from a file
        """
        if not os.path.isdir(path):
            raise FileNotFoundError("Wrong vector database path")
        logger.info(f"Vector database loaded from {path}")
        self.db = FAISS.load_local(
            path, self.embeddings, allow_dangerous_deserialization=True
        )
        return self.db

    def similarity_search(self, query: str, k=4) -> List[Document]:
        """
        Find documents in the database that are similar to the querry and return them
        """
        if self.db is None:
            logger.error("Similarity search requiered but ne vector database is found")
            return []
        logger.info(f"Similarity search done with {query}")
        return self.db.similarity_search(query=query, k=k)
