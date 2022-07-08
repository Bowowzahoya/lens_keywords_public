from datetime import datetime
import pandas as pd
from .constants import *
from .utils import count_separated_strings
from .search import *

import logging
log = logging.getLogger(__name__)

def count_keywords(lens_export, 
            keyword_columns=[FIELDS_OF_STUDY_COL, KEYWORDS_COL, MESH_TERMS_COL, CHEMICALS_COL],
            cutoff=2,
            **count_arguments):
    log.info("Adding keyword columns.")
    keyword_column = _get_keyword_columns(lens_export[keyword_columns])
    log.info("Retrieving keywords.")
    keyword_amounts = count_separated_strings(keyword_column)
    log.info(f"{len(keyword_amounts)} keywords identified.")

    keywords_to_count = keyword_amounts[keyword_amounts >= cutoff].index
    keywords_to_count = list(set([kw.lower() for kw in keywords_to_count]))
    log.info(f"Cut to {len(keywords_to_count)} relevant keywords and removed casing.")

    log.info("Retrieving keywords.")
    counts = count_strings(lens_export, 
        keywords_to_count, 
        keyword_columns=keyword_columns, 
        **count_arguments)
    counts = counts.append(pd.Series({col:len(lens_export) for col in counts.columns}, name=ALL_VALUE))
    log.info("Sorting keywords.")
    counts = counts.sort_values(by=ALL_COUNT_COL, ascending=False)
    return counts


def count_strings(lens_export, strings,
        index_directory=DEFAULT_INDEX_DIRECTORY,
        per_column=True,
        id_column=LENS_ID_COL,
        text_columns=[ABSTRACT_COL, TITLE_COL],
        keyword_columns=[FIELDS_OF_STUDY_COL, KEYWORDS_COL, MESH_TERMS_COL, CHEMICALS_COL],
        delete_args=DEFAULT_DELETE_ARGS):

    log.info("Removing quotes from columns.")
    for column in keyword_columns+text_columns:
        lens_export.loc[:,column] = lens_export[column].str.replace('"','')
    strings = [str(s).replace('"',"") for s in strings]


    log.info("Creating index.")
    whoosh_index = create_index(lens_export, index_directory=index_directory,
            id_column=id_column,
            text_columns=text_columns,
            keyword_columns=keyword_columns)

    log.info("Counting column all.")
    counts = _count(whoosh_index, strings, text_columns+keyword_columns)
    counts.name = ALL_COUNT_COL
    counts = pd.DataFrame(counts)
    if per_column:
        for column in text_columns+keyword_columns:
            log.info(f"Counting column {column}")
            column_counts = _count(whoosh_index, strings, [column])
            counts[COUNT_IN_PREFIX+column] = column_counts

    delete_index(index_directory=index_directory, **delete_args)
    
    return counts

def _count(whoosh_index, keywords, search_columns):
    counts = {}
    for index, keyword in enumerate(keywords):
        if index%500 == 0:
            log.info(f"Searching for keyword {keyword} ({index+1}/{len(keywords)})")

        ids = search_index(whoosh_index, search_columns, keyword)
        counts[keyword] = len(ids)
    return pd.Series(counts)
    
def _get_keyword_columns(dataframe, separator=SEPARATOR):
    dataframe = dataframe.fillna("").astype(str)
    out_column = dataframe[dataframe.columns[0]]
    for column_left, column_right in zip(dataframe.columns[:-1], dataframe.columns[1:]):
        mask = (dataframe[column_left].str.len() != 0) & (dataframe[column_right].str.len() != 0)
        out_column[mask] += separator
        out_column += dataframe[column_right]

    return out_column
