import pandas as pd
import os

from .constants import *
from .utils import count_strings_in_texts, count_separated_strings
from .search import *

import logging
log = logging.getLogger(__name__)

def split_csv(lens_export, keywords,
        index_directory=".whoosh_index/",
        id_column=LENS_ID_COL,
        text_columns=[ABSTRACT_COL, TITLE_COL],
        keyword_columns=[FIELDS_OF_STUDY_COL, KEYWORDS_COL, MESH_TERMS_COL, CHEMICALS_COL],
        delete_args={"sleep":5, "retry":1, "aftersleep":1}):
    
    if len(keywords) == 1:
        log.info(f"Single keyword export encountered, returning lens export directly.")
        yield lens_export
        return

    log.info(f"Creating index for lens_export of {keywords}.")
    whoosh_index = create_index(lens_export, index_directory=index_directory,
            id_column=id_column,
            text_columns=text_columns,
            keyword_columns=keyword_columns)

    lens_export = lens_export.set_index(LENS_ID_COL)
    for keyword in keywords:
        ids = search_index(whoosh_index, text_columns+keyword_columns, keyword)
        yield lens_export.loc[ids]

    delete_index(index_directory=index_directory, **delete_args)
