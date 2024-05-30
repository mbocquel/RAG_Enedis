from scrapping.list_docs_enedis import ScrapListDocsEnedis
import pytest

@pytest.fixture()
def resource():
    print("setup")
    yield "resource"
    print("teardown")

class TestScrapListDocsEnedis:
    def test_that_depends_on_resource(self, resource):
        print("testing {}".format(resource))

def test_load_page():
    assert True


def test_get_page_data():
    assert True


def test_scrap_all():
    assert True


def test_scrap_all():
    assert True

 
def test_create_dataframe():
    assert True


def test_save_dataframe_to_csv():
    assert True
