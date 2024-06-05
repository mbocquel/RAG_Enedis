import requests
import pandas as pd
import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler(f"logs/{__name__}.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class IndexingPdfData:
    """
    This class manages the indexing part of the RAG. It recieve a dataframe with
    the URL of some PDF files as well as some information on these files.
    The class download these files, parses the pdf to text, cut the text into small
    chunks of data, embed the text into a vector using HuggingFaceEmbeddings
    """

    def __init__(self, dataframe: pd.core.frame.DataFrame) -> None:
        assert dataframe.shape[1] == 7, "IndexingPdfData -> Wrong dataframe shape"
        assert list(dataframe.columns) == [
            "url",
            "type",
            "date",
            "content",
            "file_name",
            "file_type",
            "file_size",
        ]
        self.docs = []
        self.db = None
        self.dataframe = dataframe
        self.pdf_folder_path = "pdf_files"
        if not os.path.isdir(self.pdf_folder_path):
            os.mkdir(self.pdf_folder_path)
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.embeddings = HuggingFaceEmbeddings()
        logger.info("IndexingPdfData initialised")

    def parse_one_pdf(self, index, row):
        """Download the pdf and add it to the list of parced element"""
        file = row["url"]
        file_name = row["file_name"]
        logger.info(f"{index} - File {file_name} loaded")
        pdf = requests.get(file, timeout=10)
        file_path = os.path.join(self.pdf_folder_path, row["file_name"])
        with open(file_path, "wb") as f:
            f.write(pdf.content)
        loader = UnstructuredPDFLoader(file_path)
        doc = loader.load()
        self.docs.append(self.text_splitter.split_documents(doc))
        os.remove(file_path)

    def parse_all_pdf(self):
        """
        Download all the pdf and parse them
        """
        for index, row in self.dataframe.iterrows():
            self.parse_one_pdf(index, row)

    def create_vector_database(self):
        """
        Create the vector database using FAISS from the extracted documents
        """
        if len(self.docs) == 0:
            return
        docs = [item for sublist in self.docs for item in sublist]
        _ = load_dotenv(find_dotenv())
        logger.info("HuggingFace token loaded from .env file")
        self.db = FAISS.from_documents(docs, self.embeddings)

    def save_vdb_to_file(self, path: str):
        """
        Save the vector database to a file for future use
        """
        if self.db is None:
            return
        logger.info(f"Vector database saved localy in {path}")
        self.db.save_local(path)

    def load_vdb_from_file(self, path: str):
        """
        Load a vector database from a file
        """
        if not os.path.isdir(path):
            return
        logger.info(f"Vector database loaded from {path}")
        self.db = FAISS.load_local(
            path, self.embeddings, allow_dangerous_deserialization=True
        )

    def similarity_search(self, query: str):
        """
        Find documents in the database that are similar to the querry and return them
        """
        logger.info(f"Similarity search done with {query}")
        return self.db.similarity_search(query)
