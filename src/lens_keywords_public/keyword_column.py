from .constants import *
from .search import *

import logging
log = logging.getLogger(__name__)

def get_keyword_column(lens_export, recognized_keywords,
        index_directory=DEFAULT_INDEX_DIRECTORY,
        id_column=LENS_ID_COL,
        text_columns=[ABSTRACT_COL, TITLE_COL],
        keyword_columns=[FIELDS_OF_STUDY_COL, KEYWORDS_COL, MESH_TERMS_COL, CHEMICALS_COL],
        delete_args=DEFAULT_DELETE_ARGS):

    log.info("Creating index.")
    whoosh_index = create_index(lens_export, index_directory=index_directory,
            id_column=id_column,
            text_columns=text_columns,
            keyword_columns=keyword_columns)

    log.info("Getting keywords column.")
    keywords_column = _get_keywords(whoosh_index, 
        recognized_keywords, 
        text_columns+keyword_columns, 
        lens_export[id_column])

    keywords_column.index = lens_export.index
    
    delete_index(index_directory=index_directory, **delete_args)

    return keywords_column


def _get_keywords(whoosh_index, keywords, search_columns, id_values):
    keywords_column = pd.Series(index=id_values, data="")
    for index, keyword in enumerate(keywords):
        if index%500 == 0:
            log.info(f"Searching for keyword {keyword} ({index+1}/{len(keywords)})")

        ids = search_index(whoosh_index, search_columns, keyword)
        keywords_column.loc[ids] += keyword+SEPARATOR
    keywords_column = keywords_column.str[:-len(SEPARATOR)]
    return keywords_column