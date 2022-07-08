import pandas as pd
import numpy as np
import os

from context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, assert_dataframes_equal, assert_series_equal
from lens_keywords_public import split as sp
from lens_keywords_public.constants import *

TEST_EXPORT = pd.read_csv(RESOURCES_FOLDER+"3ab2e7bbd53b.csv") 
TEST_HASH_KEYWORD_DICT = pd.read_excel(RESOURCES_FOLDER+"hash_keywords_dict.xlsx", index_col=0, squeeze=True)


def test_split_csv():
    keywords = "Polymer science; Carbon Nanoparticles; Surface engineering".split("; ")
    dfs = {}
    for dataframe, keyword in zip(sp.split_csv(TEST_EXPORT, keywords), keywords):
        print(keyword)
        print(dataframe)
        dataframe.to_excel(OUTPUT_FOLDER+keyword+".xlsx")
        dfs[keyword] = dataframe
    assert len(dfs["Polymer science"]) == 25
