from langchain.tools import tool
from indexing.indexing_csv import IndexingCSV
from typing import List
from langchain_core.documents import Document

index = IndexingCSV(load_existing=True)
if index.db is None:
    index.parse_csv()
    index.create_vector_database()


@tool
def find_interesting_documents(query: str) -> List[Document]:
    """Look into a vector database to find documents that are related to the user query.
    Return a list of Documents"""
    return index.similarity_search(query=query)
