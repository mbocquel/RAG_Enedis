import os
from langchain_community.document_loaders import OnlinePDFLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from typing import List
from configs.CFG import CFG
from configs.config import Config
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

    def __init__(self) -> None:
        self.config = Config.from_json(CFG).indexing_pdf
        self.docs = []
        self.set_url_added = set()
        self.db = None
        self.pdf_folder_path = self.config.pdf_folder_path
        if not os.path.isdir(self.pdf_folder_path):
            os.mkdir(self.pdf_folder_path)
        self.text_splitter = CharacterTextSplitter(
            chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap
        )
        _ = load_dotenv(find_dotenv())
        self.embeddings = HuggingFaceEmbeddings()
        logger.info("IndexingPdfData initialised")

    def parse_one_pdf(self, url: str, file_name: str) -> None:
        """Download the pdf and add it to the vector database"""
        logger.info(f"File {file_name} loaded")
        if (url, file_name) in self.set_url_added:
            logger.info(f"File {file_name} already loaded")
            return
        try:
            loader = OnlinePDFLoader(url)
            doc = loader.load()
            for d in doc:
                d.metadata["url"] = url
                d.metadata["source"] = file_name
            docs = self.text_splitter.split_documents(doc)
            db = FAISS.from_documents(docs, self.embeddings)
            if self.db is None:
                self.db = db
            else:
                self.db.merge_from(db)
            self.set_url_added.add((url, file_name))
        except Exception:
            logger.error(f"Error while loading {url}")
            return

    def save_vdb_to_file(self, path: str) -> None:
        """
        Save the vector database to a file for future use
        """
        if self.db is None:
            return
        logger.info(f"Vector database saved localy in {path}")
        self.db.save_local(path)

    def load_vdb_from_file(self, path: str) -> None:
        """
        Load a vector database from a file
        """
        if not os.path.isdir(path):
            return
        logger.info(f"Vector database loaded from {path}")
        self.db = FAISS.load_local(
            path, self.embeddings, allow_dangerous_deserialization=True
        )

    def similarity_search(self, query: str, k=4) -> List[Document]:
        """
        Find documents in the database that are similar to the querry and return them
        """
        if self.db is None:
            logger.error("Similarity search requiered but ne vector database is found")
            return []
        logger.info(f"Similarity search done with {query}")
        return self.db.similarity_search(query=query, k=k)
