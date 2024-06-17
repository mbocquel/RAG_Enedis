from langchain.tools import tool
from indexing.indexing_csv import IndexingCSV
from indexing.indexing_pdf import IndexingPdfData
from typing import List
from langchain_core.documents import Document


index = IndexingCSV(load_existing=True)
if index.db is None:
    index.parse_csv()
    index.create_vector_database()

index_pdf = IndexingPdfData()
index_pdf.load_vdb_from_file("vdb_enedis")


@tool
def list_interesting_documents(query: str, number_of_documents: int = 3) -> List[dict]:
    """
    Function that returns a list of documents in the library related to a topic.
    """
    results = index.similarity_search(query=query, k=number_of_documents)
    to_return = []
    for result in results:
        row = result.metadata["row"]
        to_return.append(index.dataframe.iloc[row, :].to_dict())
    return to_return


@tool
def find_context_to_answer_a_question(question: str) -> List[Document]:
    """
    Function that find context to answer a specific question.
    """
    return index_pdf.similarity_search(question)
