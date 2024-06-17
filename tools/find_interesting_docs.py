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
    dataframe_rows = [
        result.metadata["row"]
        for result in index.similarity_search(query=question, k=3)
    ]
    list_documents = [
        (
            index.dataframe.iloc[row, :].to_dict().get("url", ""),
            index.dataframe.iloc[row, :].to_dict().get("file_name", ""),
        )
        for row in dataframe_rows
    ]

    for doc in list_documents:
        if (doc[0], doc[1]) not in index_pdf.set_url_added:
            index_pdf.parse_one_pdf(doc[0], doc[1])
    # index_pdf.create_vector_database()
    return index_pdf.similarity_search(question)
