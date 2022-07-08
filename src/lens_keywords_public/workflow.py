from .utils import count_strings_in_texts
from .count import count_keywords, count_strings
from .utils import count_separated_strings
from .context import add_context
from .keyword_column import get_keyword_column
from .constants import *

import logging
log = logging.getLogger(__name__)

def find_similar_keywords_scholarly(lens_export,
            context_keyword_counts=DEFAULT_CONTEXT_KEYWORD_COUNTS_SCHOLARLY,
            queried_keywords=[], 
            real_amount=None, 
            per_column=False,
            **count_arguments):

    return _find_similar_generic(lens_export,
        context_keyword_counts,
        queried=queried_keywords,
        real_amount=real_amount,
        queried_keyword_columns=[FIELDS_OF_STUDY_COL, KEYWORDS_COL, MESH_TERMS_COL, CHEMICALS_COL],
        queried_text_columns=[TITLE_COL, ABSTRACT_COL],
        per_column=per_column,
        **count_arguments)

def find_similar_keywords_patents(lens_export,
            lens_export_scholarly_for_keywords=None,
            context_keyword_counts=DEFAULT_CONTEXT_KEYWORD_COUNTS_PATENTS,
            queried_keywords=[], 
            real_amount=None, 
            per_column=False,
            **count_arguments):
    

    if isinstance(lens_export_scholarly_for_keywords, type(None)):
        log.info("No Lens Scholarly export provided for keywords, will use keywords from context.")
        keyword_list = list(context_keyword_counts.index)
    else:
        log.info("Lens Scholarly export provided for keywords, extracting keywords.")
        keyword_list = list(count_keywords(lens_export_scholarly_for_keywords, 
            per_column=False, 
            **count_arguments).index)

    keywords_with_context, keywords_without_context = _find_similar_generic(lens_export,
        context_keyword_counts,
        queried=queried_keywords,
        real_amount=real_amount,
        queried_keyword_columns=[],
        queried_text_columns=[TITLE_COL],
        per_column=per_column,
        keyword_list=keyword_list,
        **count_arguments)

    # using keywords from other sources does not guarantee all keywords are found
    # remove keywords that are not found:
    keywords_with_context = keywords_with_context[keywords_with_context[ALL_COUNT_COL] > 0]
    keywords_without_context = keywords_without_context[keywords_without_context[ALL_COUNT_COL] > 0]

    return keywords_with_context, keywords_without_context

def find_similar_source_titles(lens_export,
        context_source_title_counts=DEFAULT_CONTEXT_SOURCE_TITLE_COUNTS_SCHOLARLY,
        queried_source_titles=[],
        real_amount=None, 
        per_column=False,
        **count_arguments):
    
    return _find_similar_generic(lens_export,
        context_source_title_counts,
        queried=queried_source_titles,
        real_amount=real_amount, 
        queried_keyword_columns=[SOURCE_TITLE_COL],
        queried_text_columns=[],
        per_column=per_column,
        **count_arguments)

def find_similar_ipcr_classifications(lens_export,
        context_ipcr_classification_counts=DEFAULT_CONTEXT_IPCR_CLASSIFICATION_COUNTS_PATENTS,
        queried_ipcr_classification=[],
        real_amount=None, 
        per_column=False,
        **count_arguments):

    log.info("Extracting classifications.")
    ipcr_classifications_list = list(count_separated_strings(lens_export[IPCR_CLASSIFICATIONS_COL], separator=LENS_SEPARATOR).index.str.lower())
    
    return _find_similar_generic(lens_export,
        context_ipcr_classification_counts,
        queried=queried_ipcr_classification,
        real_amount=real_amount, 
        queried_keyword_columns=[IPCR_CLASSIFICATIONS_COL],
        queried_text_columns=[],
        keyword_list=ipcr_classifications_list,
        per_column=per_column,
        **count_arguments)

def _find_similar_generic(lens_export,
    context_amounts,
    queried=[],
    real_amount=None,
    queried_keyword_columns=[FIELDS_OF_STUDY_COL, KEYWORDS_COL, MESH_TERMS_COL, CHEMICALS_COL],
    queried_text_columns=[TITLE_COL, ABSTRACT_COL],
    per_column=False,
    keyword_list=None,
    **count_arguments):

    if len(lens_export) in MAXIMUM_EXPORT_SIZES and isinstance(real_amount, type(None)):
        log.warning(f"Lens export contains {len(lens_export)} records, which is a download limit of the Lens."+\
                "However, no real amount of records was specified via the 'real_amount' keyword.")

    if isinstance(keyword_list, type(None)):
        cutoff = count_arguments.get("cutoff", CUTOFF_FOR_MAXIMUM_EXPORT_SIZE*len(lens_export)/MAXIMUM_EXPORT_SIZE)

        log.info("Commencing keyword counting without pre-determined keywords.")
        keyword_counts = count_keywords(lens_export, 
            cutoff=cutoff,
            keyword_columns=queried_keyword_columns,
            text_columns=queried_text_columns,
            per_column=per_column,
            **count_arguments)
    else:
        log.info("Commencing keyword counting with pre-determined keywords.")
        keyword_counts = count_strings(lens_export, 
            keyword_list,
            keyword_columns=queried_keyword_columns,
            text_columns=queried_text_columns,
            per_column=per_column,
            **count_arguments)

    log.info("Commencing keyword context retrieval.")

    if isinstance(real_amount, type(None)): coverage = 1
    else: coverage = len(lens_export)/real_amount

    keywords_with_context, keywords_without_context = add_context(keyword_counts, 
            queried=queried, 
            coverage=coverage,
            context_amounts=context_amounts)
    return keywords_with_context, keywords_without_context


"""------------------------------------------------------------------------------------------
        Adding keyword columns
------------------------------------------------------------------------------------------"""

def find_keywords_patent_families(families, scholarly_export, cutoff=STANDARD_KEYWORD_CUTOFF):
    keywords = count_keywords(scholarly_export, per_column=False, cutoff=cutoff)
    keywords_list = list(keywords.index)
    keywords_list.remove(ALL_VALUE)

    if len(keywords_list) == 0:
        log.error(f"No keywords above cutoff of {cutoff}")

    keywords_column = get_keyword_column(families, keywords_list, 
        id_column=PATENT_ID_COL, 
        text_columns=[PATENT_ABSTRACT_COL, PATENT_TITLES_COL], 
        keyword_columns=[])

    families[PATENT_KEYWORDS_COL] = keywords_column
    return families
    
def find_keywords_scholarly_export(scholarly_export, cutoff=STANDARD_KEYWORD_CUTOFF):
    keywords = count_keywords(scholarly_export, per_column=False, cutoff=cutoff)
    keywords_list = list(keywords.index)
    keywords_list.remove(ALL_VALUE)

    if len(keywords_list) == 0:
        log.error(f"No keywords above cutoff of {cutoff}")

    keywords_column = get_keyword_column(scholarly_export, keywords_list)

    scholarly_export[SCHOLARLY_CUSTOM_KEYWORDS_COL] = keywords_column
    return scholarly_export




    