from langchain.tools import tool
from indexing.indexing_csv import IndexingCSV
from indexing.indexing_pdf import IndexingPdfData
from typing import List
from q_and_a.q_and_a import QAndA

index = IndexingCSV(load_existing=True)
if index.db is None:
    index.parse_csv()
    index.create_vector_database()

index_pdf = IndexingPdfData()


@tool
def trouver_des_documents_interessant(
    question: str, nombre_de_documents: int = 3
) -> List[dict]:
    """
    Recherche dans une base de donnee vectorielle pour trouver les meilleurs documents qui repondent a la demande utilisateur.
    Renvoie un dictionnaire comportant l'URL des documents qui permettra a l'utilisateur de les telecharger,
    ainsi que des informations complementaires sur les documents
    """
    results = index.similarity_search(query=question, k=nombre_de_documents)
    to_return = []
    for result in results:
        row = result.metadata["row"]
        to_return.append(index.dataframe.iloc[row, :].to_dict())
    return to_return


@tool
def rechercher_une_information_dans_un_pdf(
    question: str, url_du_pdf: str, nom_du_pdf: str
) -> str:
    """
    Telecharge un fichier pdf, puis recherche des informations qui peuvent repondre a la questions dans ce pdf.
    """
    if (url_du_pdf, nom_du_pdf) not in index_pdf.set_url_added:
        index_pdf.parse_one_pdf(url_du_pdf, nom_du_pdf)
        index_pdf.create_vector_database()
    q_and_a = QAndA(index_pdf)
    reponse = q_and_a.ask_question(query=question)
    return reponse["output_text"]
