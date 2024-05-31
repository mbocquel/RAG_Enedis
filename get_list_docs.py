from scrapping.list_docs_enedis import ScrapListDocsEnedis

def main():
    """
    This program collect data from the Enedis documentation website,
    and create a csv file with the list of available documents and their URL
    """
    scrap = ScrapListDocsEnedis()
    scrap.scrap_all()
    scrap.create_dataframe()
    scrap.save_dataframe_to_csv()

if __name__ == "__main__":
    main()