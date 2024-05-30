import requests
from bs4 import BeautifulSoup
import pandas as pd


class ScrapListDocsEnedis:
    """
    This class aims at scrapping the enedis "Documentation de Reference" website.
    """
    def __init__(self) -> None:
        self.data = []
        self.url_visited = []
        self.url_base = 'https://www.enedis.fr/documents'
        self.curent_page = None
    
    
    def load_page(self):
        """Load a page and parse it, then store it in self.curent_page"""
        pass


    def get_page_data(self) -> list:
        """
        Collect the data from a page, return value : 
        [['url', 'type', "date", "content", "file_info"], [...]]
        """
        pass

    def scrap_all(self):
        """
        Scrap all pages of the enedis document page
        """
        pass


    def create_dataframe(self):
        """
        Create the dataframe from all data collected
        """
        pass


    def save_dataframe_to_csv(self, path = "documents_enedis.csv"):
        """
        Save the documents in a csv
        """
        pass


