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
        self.url_base = "https://www.enedis.fr/documents"
        self.curent_page = None
        self.dataframe = None
        self.num_page = 0

    def load_page(self):
        """Load a page and parse it, then store it in self.curent_page"""
        if self.num_page < 0:
            return
        url = self.url_base + "?page=" + str(self.num_page)
        response = requests.get(url, timeout=10)
        self.url_visited.append(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.curent_page = soup.select(".press-page__field")
        next_ = soup.select(".pager__next")
        if next_:
            self.num_page += 1
        else:
            self.num_page = -1

    def get_page_data(self) -> None:
        """
        Collect the data from a page, return value :
        [['title', 'url', 'type', "date", "content", "file_info"], [...]]
        """
        if not self.curent_page:
            raise Exception("The page does not exist")
        scrapping = []
        scrap_elem = []
        sep_list = [elem == self.curent_page[0] for elem in self.curent_page]
        for i in range(1, len(sep_list)):
            if sep_list[i]:
                scrapping.append(scrap_elem)
                scrap_elem = []
            else:
                scrap_elem.append(
                    [elem for elem in self.curent_page[i].contents if elem != "\n"]
                )
        scrapping.append(scrap_elem)

        for pdf in scrapping:
            new_data = [[""]] * 8
            for elem in pdf:
                if isinstance(elem, list) and len(elem):
                    if (
                        "attrs" in elem[0].__dict__
                        and "href" in elem[0].__dict__.get("attrs")
                        and "aria-label" not in elem[0].__dict__.get("attrs")
                    ):
                        new_data[0] = elem[0].__dict__.get("contents")[0].strip().replace(",", ";")
                        new_data[1] = "https://www.enedis.fr" + elem[0].__dict__.get(
                            "attrs"
                        ).get("href")
                    elif "attrs" in elem[0].__dict__ and "datetime" in elem[
                        0
                    ].__dict__.get("attrs"):
                        new_data[3] = elem[0].__dict__.get("attrs").get("datetime")
                    elif "attrs" in elem[0].__dict__ and "aria-label" in elem[
                        0
                    ].__dict__.get("attrs"):
                        file_info = elem[0].__dict__.get("attrs").get("aria-label")
                        infos = str(file_info).split(",")
                        if len(infos) == 3:
                            new_data[5] = [infos[0].strip()]
                            new_data[6] = [infos[1].strip()]
                            new_data[7] = [infos[2].strip()]
                        else:
                            new_data[5] = file_info
                    elif new_data[2] == [""]:
                        new_data[2] = [str(elem[0]).strip().replace(",", ";")]
                    else:
                        new_data[4] = [str(elem[0]).strip().replace(",", ";")]
            self.data.append(new_data)

    def scrap_all(self):
        """
        Scrap all pages of the enedis document page
        """
        while self.num_page >= 0:
            if self.num_page % 5 == 0:
                print(self.num_page)
            self.load_page()
            self.get_page_data()

    def create_dataframe(self):
        """
        Create the dataframe from all data collected
        """
        if len(self.data) == 0:
            return
        self.dataframe = pd.DataFrame(
            self.data,
            columns=[
                "title",
                "url",
                "type",
                "date",
                "content",
                "file_name",
                "file_type",
                "file_size",
            ],
        )

    def save_dataframe_to_csv(self, path="documents_enedis.csv"):
        """
        Save the documents in a csv
        """
        if self.dataframe is None:
            return
        self.dataframe.to_csv(path)
