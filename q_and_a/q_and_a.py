from indexing.indexing_pdf import IndexingPdfData
from langchain.chains.question_answering import load_qa_chain
from langchain_huggingface import HuggingFaceEndpoint
from configs.CFG import CFG, my_prompt_template
from configs.config import Config
import logging
from typing import Dict, Any


logger = logging.getLogger(__name__)
handler = logging.FileHandler(f"logs/{__name__}.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


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
            max_new_tokens=self.config.llm.max_new_tokens,
        )  # type: ignore
        self.chain = load_qa_chain(
            self.llm,
            chain_type=self.config.chain.chain_type,
            verbose=self.config.chain.verbose,
        )
        self.chain.llm_chain.prompt.template = my_prompt_template  # type: ignore
        self.history = []

    def ask_question(self, query: str, save_history: bool = False) -> Dict[str, Any]:
        """
        Method that recieve a question, send it to the LLM and retrive the answer.
        If save_historyy = True, the question and answer are saved.
        """
        if self.index.db is None:
            raise Exception("Vector Database not defined")
        context_docs = self.index.db.similarity_search(query)
        response = self.chain.invoke(
            {"input_documents": context_docs, "question": query},
            return_only_outputs=False,
        )
        logger.info(f"QandA for{query}")
        if save_history:
            self.history.append(response)
        return response

    def get_history(self, index_start=None, index_end=None):
        """
        Retrieve the history of question and answer asked
        """
        if index_start is None and index_end is None:
            return self.history
        elif index_start is None and index_end is not None:
            return self.history[: index_end + 1]
        elif index_end is None:
            return self.history[index_start:]
        else:
            return self.history[index_start : index_end + 1]

    def clear_history(self):
        """
        Clear the Q and A history
        """
        self.history.clear()
