import requests
import pandas as pd
import os


class IndexingPdfData:
	"""
	This class manages the indexing part of the RAG. It recieve a dataframe with
	the URL of some PDF files as well as some information on these files. 
	The class download these files, parses the pdf to text, cut the text into small
	chunks of data, embed the text into a vector using HuggingFaceEmbeddings
	"""
	def __init__(self, df: pd.core.frame.DataFrame) -> None:
		pass

	def parse_one_pdf(self):
		"""Download the pdf and add it to the list of parced element"""
		pass

	def create_vector_database(self):
		"""
		Create the vector database using FAISS from the extracted documents
		"""
		pass

	def save_vdb_to_file(self, path:str):
		"""
		Save the vector database to a file for future use
		"""
		pass

	def load_vdb_from_file(self, path:str):
		"""
		Load a vector database from a file
		"""
		pass

	def similarity_search(self, query:str):
		"""
		Find documents in the database that are similar to the querry and return them
		"""
		pass

	
