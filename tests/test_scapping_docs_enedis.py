from scrapping.list_docs_enedis import ScrapListDocsEnedis
import pytest
import tempfile
import pandas as pd
import os


@pytest.fixture()
def scrap_with_page_loaded():
    scrap = ScrapListDocsEnedis()
    scrap.load_page()
    yield scrap


@pytest.fixture()
def scrap_all_done_no_df():
    scrap = ScrapListDocsEnedis()
    scrap.load_page()
    scrap.get_page_data()
    yield scrap


@pytest.fixture()
def scrap_all_done():
    scrap = ScrapListDocsEnedis()
    scrap.load_page()
    scrap.get_page_data()
    scrap.create_dataframe()
    yield scrap


def test_load_page():
    scrap = ScrapListDocsEnedis()
    scrap.load_page()
    assert scrap.curent_page is not None
    assert len(scrap.url_visited) > 0


def test_get_page_data(scrap_with_page_loaded):
    scrap_with_page_loaded.get_page_data()
    assert len(scrap_with_page_loaded.data) != 0
    assert len(scrap_with_page_loaded.data[0]) == 8


def test_create_dataframe(scrap_all_done_no_df):
    scrap_all_done_no_df.create_dataframe()
    assert scrap_all_done_no_df.dataframe is not None
    assert type(scrap_all_done_no_df.dataframe) == pd.core.frame.DataFrame


def test_save_dataframe_to_csv(scrap_all_done):
    test_dir = tempfile.TemporaryDirectory()
    tmp_file_name = os.path.join(test_dir.name, "documents_enedis.csv")
    scrap_all_done.save_dataframe_to_csv(tmp_file_name)
    assert os.path.isfile(tmp_file_name)
    os.remove(tmp_file_name)
