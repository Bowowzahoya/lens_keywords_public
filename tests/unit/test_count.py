import pandas as pd
import numpy as np

from context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, assert_dataframes_equal, assert_series_equal
from lens_keywords_public import count as cnt
from lens_keywords_public import utils as ut
from lens_keywords_public.constants import FIELDS_OF_STUDY_COL

TEST_EXPORT_SHORT = pd.read_csv(RESOURCES_FOLDER+"short.csv")

def test_count_strings():
    keywords = ut.count_separated_strings(TEST_EXPORT_SHORT[FIELDS_OF_STUDY_COL])
    counts = cnt.count_strings(TEST_EXPORT_SHORT, list(keywords.index))
    print(counts)
    
def test_get_keyword_columns():
    df = pd.DataFrame({1:{"a":"kw; kw2", "b":None}, 2:{"a":"kw3", "b":"kw4; kw5"}})
    column = cnt._get_keyword_columns(df)
    assert column["a"] == "kw; kw2; kw3"
    assert column["b"] == "kw4; kw5"

    df = pd.DataFrame({1:{"a":"kw; kw2", "b":None}, 2:{"a":"", "b":"kw4; kw5"}})
    column = cnt._get_keyword_columns(df)
    assert column["a"] == "kw; kw2"
    assert column["b"] == "kw4; kw5"

    df = pd.DataFrame({1:{"a":None, "b":None}, 2:{"a":"", "b":"kw4; kw5"}})
    column = cnt._get_keyword_columns(df)
    assert column["a"] == ""
    assert column["b"] == "kw4; kw5"

    df = pd.DataFrame({1:{"a":None, "b":"kw"}, 2:{"a":"", "b":"kw4; kw5"}, 3:{"a":"kw6", "b":"kw7"}})
    column = cnt._get_keyword_columns(df)
    assert column["a"] == "kw6"
    assert column["b"] == "kw; kw4; kw5; kw7"
