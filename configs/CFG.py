"""
CONFIG FILE FOR THE PROJECT
"""

CFG = {
    "llm": {
        "repo_id": "mistralai/Mixtral-8x7B-Instruct-v0.1", 
        "temperature": 0.1, 
        "max_new_tokens": 2000
    }, 
    "chain": {
        "chain_type": "stuff", 
        "verbose": True, 
        "result_french": True
    }, 
    "indexing":{
        "pdf_folder_path": "pdf_files",
        "chunk_size": 1000,
        "chunk_overlap": 250
    }
}


my_prompt_template = """You are a multilingual assistant for question-answering tasks. Your answer must always be written in the same language than the question. 
You first need to check that the context provided is related to the question. If they are not related, imediately respond : 'HORS SUJET' and nothing more.
Otherwise, use the following pieces of retrieved context to answer the question. If you can't find the answer in the context provided, just say that you don't know.
You should never use knowledge that is not in the context to answer a question.
You have to be absolutly sure to use the correct language, for example if the question is written in French, you need to reply in French.


CONTEXT:
{context}


QUESTION:
{question}


REPONSE:"""