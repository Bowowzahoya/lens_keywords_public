import pandas as pd
import numpy as np

from integration_context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, COMPARE_FOLDER
from integration_context import dataframes_equal, series_equal
from lens_keywords_public import count as cnt

TEST_EXPORT_MEDIUM = pd.read_csv(RESOURCES_FOLDER+"medium.csv")

COMPARE_COUNTS_MEDIUM = pd.read_excel(COMPARE_FOLDER+"counts_medium.xlsx", index_col=0)
COMPARE_COUNTS_MEDIUM  = COMPARE_COUNTS_MEDIUM.sort_index()

def test_count_keywords():
    counts = cnt.count_keywords(TEST_EXPORT_MEDIUM)
    counts = counts.sort_index()
    counts.to_excel(OUTPUT_FOLDER+"counts_medium.xlsx")

    assert dataframes_equal(counts, COMPARE_COUNTS_MEDIUM)
