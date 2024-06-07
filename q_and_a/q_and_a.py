from indexing.indexing_data import IndexingPdfData
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain_community.llms import HuggingFaceEndpoint
from configs.CFG import CFG
from configs.config import Config


class QAndA:
    """
    Class that manage the retrival of information from the database
    and send a question with context to a Large Language Model
    """
    def __init__(self, index: IndexingPdfData) -> None:
        self.index = index
        assert self.index.db is not None, "No vector db found"
        self.config = Config.from_json(CFG)
        self.llm = HuggingFaceEndpoint(
            repo_id=self.config.llm.repo_id,
            temperature=self.config.llm.temperature,
            max_new_tokens = self.config.llm.max_new_tokens
            )
        self.chain = load_qa_chain(
            self.llm,
            chain_type=self.config.chain.chain_type,
            verbose=self.config.chain.verbose
            )
        self.history = []
    
    def ask_question(self, query:str, save_history:bool=True) -> str:
        """
        Method that recieve a question, send it to the LLM and retrive the answer. 
        If save_historyy = True, the question and answer are saved. 
        """
        pass

    
    def get_history(self, index_start=0, index_end=None):
        """
        Retrieve the history of question and answer asked
        """
        pass


    def clear_history(self):
        """
        Clear the Q and A history
        """
        pass
