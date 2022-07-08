import pandas as pd
import numpy as np

from integration_context import *
from lens_keywords_public import context as ctx
from lens_keywords_public.constants import *

TEST_KNOWN_AMOUNTS = pd.read_excel(RESOURCES_FOLDER+"keyword_known_amounts.xlsx", index_col=0, squeeze=True)
TEST_KEYWORDS = pd.read_excel(RESOURCES_FOLDER+"keyword_counts.xlsx", index_col=0)
COMPARE_KEYWORD_WITH_CONTEXT = pd.read_excel(COMPARE_FOLDER+"keyword_with_context.xlsx", index_col=0)
COMPARE_KEYWORD_WITHOUT_CONTEXT = pd.read_excel(COMPARE_FOLDER+"keyword_without_context.xlsx", index_col=0)

def test_add_keyword_context():
    coverage = TEST_KEYWORDS.loc[ALL_VALUE, ALL_COUNT_COL]/128_032.
    keywords_with_context, keywords_without_context = ctx.add_context(TEST_KEYWORDS, context_amounts=TEST_KNOWN_AMOUNTS,
        coverage=coverage, queried=["nanomaterials"])
    print(keywords_with_context)
    keywords_with_context.to_excel(OUTPUT_FOLDER+"keyword_with_context.xlsx")
    keywords_without_context.to_excel(OUTPUT_FOLDER+"keyword_without_context.xlsx")
    assert dataframes_equal(COMPARE_KEYWORD_WITH_CONTEXT, keywords_with_context)
    assert dataframes_equal(COMPARE_KEYWORD_WITHOUT_CONTEXT, keywords_without_context)
