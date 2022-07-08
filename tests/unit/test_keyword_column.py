import pandas as pd
import numpy as np

from context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, assert_dataframes_equal, assert_series_equal
from lens_keywords_public import keyword_column as kc
from lens_keywords_public import search as sc

TEST_EXPORT_SHORT = pd.read_csv(RESOURCES_FOLDER+"short.csv")

def test_get_keywords():
    whoosh_index = sc.create_index(TEST_EXPORT_SHORT)
    keywords_column = kc._get_keywords(whoosh_index, 
        ["catalyst", "oxide", "artificial neural networks"], 
        [sc.ABSTRACT_COL,sc.TITLE_COL,sc.KEYWORDS_COL], TEST_EXPORT_SHORT[sc.LENS_ID_COL])
    assert keywords_column["000-141-187-087-774"] == "catalyst; oxide"
    assert keywords_column["000-329-230-459-620"] == ""