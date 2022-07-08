import pandas as pd
import numpy as np
import time

import whoosh
from context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, CURRENT_FOLDER
from context import assert_dataframes_equal, assert_series_equal
from lens_keywords_public import search as sr
from lens_keywords_public.constants import ABSTRACT_COL, FIELDS_OF_STUDY_COL, TITLE_COL

TEST_EXPORT_SHORT = pd.read_csv(RESOURCES_FOLDER+"short.csv")

def test_create_index():
    index_directory=CURRENT_FOLDER+"/.whoosh_index/"
    try:
        whoosh_index = sr.create_index(TEST_EXPORT_SHORT, index_directory=index_directory)
    finally:
        sr.delete_index(index_directory=index_directory, sleep=1, retry=1, aftersleep=1)
        time.sleep(1)
    assert type(whoosh_index) == whoosh.index.FileIndex

def test_search_index():
    index_directory = CURRENT_FOLDER+"/.whoosh_index/"
    whoosh_index = sr.create_index(TEST_EXPORT_SHORT, index_directory=index_directory)
    search_fields = [ABSTRACT_COL, TITLE_COL, FIELDS_OF_STUDY_COL]
    try:
        query = "oxides"
        results = sr.search_index(whoosh_index, search_fields, query)
        query2 = "cytotoxicity"
        results2 = sr.search_index(whoosh_index, search_fields, query2)
    finally:
        sr.delete_index(index_directory=index_directory, sleep=1, retry=1, aftersleep=1)
        time.sleep(1)

    assert len(results) == 1
    assert results[0] == '000-141-187-087-774'
    
    assert len(results2) == 1
    assert results2[0] == '000-329-230-459-620'

def test_search_index_keywords():
    index_directory = CURRENT_FOLDER+"/.whoosh_index/"
    whoosh_index = sr.create_index(TEST_EXPORT_SHORT, index_directory=index_directory)
    search_fields = [FIELDS_OF_STUDY_COL]
    try:
        query = "crystallite"
        results = sr.search_index(whoosh_index, search_fields, query)
        query2 = "toxicities"
        results2 = sr.search_index(whoosh_index, search_fields, query2)
    finally:
        sr.delete_index(index_directory=index_directory, sleep=1, retry=1, aftersleep=1)
        time.sleep(1)
        
    assert len(results) == 1
    assert results[0] == '000-141-187-087-774'
    
    assert len(results2) == 1
    assert results2[0] == '000-329-230-459-620'
