"""
Module to determines how exclusive keywords are, based on known amounts of all occurences of that keyword in the Lens
This can possibly be within a time-period or other limitation
"""
import pandas as pd

from .constants import *
from .utils import get_tfidf

def add_context(keywords:pd.DataFrame, 
        queried=[],
        coverage=1,
        context_amounts=pd.Series()):

    keywords[COMPENSATED_SPECIFIC_AMOUNTS_COL] = keywords[ALL_COUNT_COL]/coverage

    keywords = _add_known_context_amounts(keywords, context_amounts)
    keywords = _add_queried_context_amounts(keywords, queried) 

    keywords_with_context = keywords[~keywords[CONTEXT_AMOUNTS_COL].isna()]
    keywords_without_context = keywords[keywords[CONTEXT_AMOUNTS_COL].isna()]

    keywords_with_context[RATIO_SPECIFIC_CONTEXT_COL] = keywords_with_context[COMPENSATED_SPECIFIC_AMOUNTS_COL] / keywords_with_context[CONTEXT_AMOUNTS_COL]
    keywords_with_context = keywords_with_context.sort_values(by=[RATIO_SPECIFIC_CONTEXT_COL, ALL_COUNT_COL], ascending=False)

    keywords_without_context = keywords_without_context.drop(CONTEXT_AMOUNTS_COL, axis=1)
    keywords_without_context[MAXIMUM_CONTEXT_AMOUNTS_COL] = context_amounts.min()
    keywords_without_context[MINIMUM_RATIO_SPECIFIC_CONTEXT_COL] = keywords_without_context[COMPENSATED_SPECIFIC_AMOUNTS_COL] / keywords_without_context[MAXIMUM_CONTEXT_AMOUNTS_COL]
    keywords_without_context = keywords_without_context.sort_values(by=[MINIMUM_RATIO_SPECIFIC_CONTEXT_COL, ALL_COUNT_COL], ascending=False)

    return keywords_with_context, keywords_without_context

def _add_known_context_amounts(keywords, known_amounts):
    overlap_index = [ix for ix in known_amounts.index if ix in keywords.index]
    keywords.loc[overlap_index, CONTEXT_AMOUNTS_COL] = known_amounts[overlap_index]
    return keywords
    
def _add_queried_context_amounts(keywords, queried_keywords):
    keywords.loc[queried_keywords, CONTEXT_AMOUNTS_COL] = keywords.loc[queried_keywords, COMPENSATED_SPECIFIC_AMOUNTS_COL]
    return keywords

def _get_tfidf(keywords, known_amounts):
    specific_amounts_all = keywords[COMPENSATED_SPECIFIC_AMOUNTS_COL].get(ALL_VALUE, max(keywords[COMPENSATED_SPECIFIC_AMOUNTS_COL]))
    context_amounts_all = known_amounts.get(ALL_VALUE, max(known_amounts))

    return get_tfidf(keywords[COMPENSATED_SPECIFIC_AMOUNTS_COL], specific_amounts_all,
            keywords[CONTEXT_AMOUNTS_COL], context_amounts_all)

