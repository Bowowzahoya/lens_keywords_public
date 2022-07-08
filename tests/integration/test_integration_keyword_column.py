import pandas as pd
import numpy as np
import os
import shutil

from integration_context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, COMPARE_FOLDER
from integration_context import dataframes_equal, series_equal
from lens_keywords_public import keyword_column as kc

TEST_PATENT_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"2D-materials_families_in_eu.xlsx")
COMPARE_FAMILIES = pd.read_excel(COMPARE_FOLDER+"families_out.xlsx", index_col=0)

def test_get_keywords_column():
    recognized_keywords = ["graphene", "borophene", "2d materials", "mesoporous", "nanomaterial", "bulk nanostructured"]
    keywords_column = kc.get_keyword_column(TEST_PATENT_FAMILIES, recognized_keywords, 
        id_column="Sorted Priority Numbers", 
        text_columns=["First Abstract", "Titles"], 
        keyword_columns=[])

    out_families = TEST_PATENT_FAMILIES.copy()
    out_families["Keywords"] = keywords_column
    out_families.to_excel(OUTPUT_FOLDER+"families_out.xlsx")

    assert dataframes_equal(out_families, COMPARE_FAMILIES)


