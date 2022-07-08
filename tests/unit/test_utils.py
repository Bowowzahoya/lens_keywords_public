import pandas as pd
import numpy as np

from context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, assert_dataframes_equal, assert_series_equal
from lens_keywords_public import utils as ut

TEST_EXPORT_SHORT = pd.read_csv(RESOURCES_FOLDER+"short.csv")

def test_count_separated_strings():
    counts = ut.count_separated_strings(TEST_EXPORT_SHORT["Fields of Study"])
    assert len(counts) == 19
    assert counts["Nanomaterials"] == 2
    assert counts ["Carbon nanomaterials"] == 1

def test_count_strings_in_texts():
    strings = pd.Series(["nanomaterials", "pulmonary"])
    texts = TEST_EXPORT_SHORT["Abstract"]
    counts = ut.count_strings_in_texts(strings, texts)
    assert counts[0] == 2
    assert counts[1] == 1
    assert len(counts) == 2

def test_count_strings_in_texts_na():
    strings = pd.Series(["nanomaterials", "pulmonary"])
    texts = pd.Series([None, "ok some text with nanomaterials"])
    counts = ut.count_strings_in_texts(strings, texts)
    assert counts[0] == 1
    assert counts[1] == 0

def test_get_tfidf():
    tfidf = ut.get_tfidf(pd.Series({"keyword1":20, "keyword2":30}), 50, 
                pd.Series({"keyword1":100, "keyword3":500}), 10000)
    print(tfidf)
    assert np.isnan(tfidf["keyword2"])
    assert round(tfidf["keyword1"], 2) == 1.84
