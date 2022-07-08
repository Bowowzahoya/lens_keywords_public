import os
import pandas as pd

CONSTANTS_RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/")
SEPARATOR = "; "
LENS_SEPARATOR = ";;"

# Lens original column names
TITLE_COL = "Title"
ABSTRACT_COL = "Abstract"
FIELDS_OF_STUDY_COL = "Fields of Study"
KEYWORDS_COL = "Keywords"
MESH_TERMS_COL = "MeSH Terms"
CHEMICALS_COL = "Chemicals"
LENS_ID_COL = "Lens ID"
SOURCE_TITLE_COL = "Source Title"
IPCR_CLASSIFICATIONS_COL = "IPCR Classifications"

# Keyword counts column names
ALL_COUNT_COL = "Count in All Columns"
COUNT_IN_PREFIX = "Count in "

# Keyword context columns names
COMPENSATED_SPECIFIC_AMOUNTS_COL = "Amounts Compensated for Coverage"
CONTEXT_AMOUNTS_COL = "Amounts in Context"
MAXIMUM_CONTEXT_AMOUNTS_COL = "Maximum Amounts in Context"
RATIO_SPECIFIC_CONTEXT_COL = "Ratio to Context"
MINIMUM_RATIO_SPECIFIC_CONTEXT_COL = "Minimum Ratio to Context"
ALL_VALUE = "_all_"

TFIDF_COL = "TF-IDF"

# Patent families column names
PATENT_ID_COL = "Sorted Priority Numbers"
PATENT_ABSTRACT_COL = "First English Abstract"
PATENT_TITLES_COL = "Titles"
PATENT_KEYWORDS_COL = "Keywords from Title and Abstract"

# Scholarly export custom column names
SCHOLARLY_CUSTOM_KEYWORDS_COL = "Custom Identified Keywords"

# Queries
TITLE_FIELD = "title"
ABSTRACT_FIELD = "abstract"
FIELDS_OF_STUDY_FIELD = "field_of_study"
SOURCE_TITLE_EXACT_FIELD = "source.title.exact"
OR_JOIN = " OR "

# Workflow
MAXIMUM_EXPORT_SIZES = [10, 100, 1_000, 10_000, 50_000]
CUTOFF_FOR_MAXIMUM_EXPORT_SIZE = 20
MAXIMUM_EXPORT_SIZE = 50_000
DEFAULT_CONTEXT_KEYWORD_COUNTS_SCHOLARLY = pd.read_excel(CONSTANTS_RESOURCES_FOLDER+"default_context_keyword_amounts_scholarly.xlsx", 
        index_col=0).squeeze("columns")
DEFAULT_CONTEXT_SOURCE_TITLE_COUNTS_SCHOLARLY = pd.read_excel(CONSTANTS_RESOURCES_FOLDER+"default_context_source_title_amounts_scholarly.xlsx", 
        index_col=0).squeeze("columns")
DEFAULT_CONTEXT_KEYWORD_COUNTS_PATENTS = pd.read_excel(CONSTANTS_RESOURCES_FOLDER+"default_context_keyword_amounts_patents.xlsx", 
        index_col=0).squeeze("columns")
DEFAULT_CONTEXT_IPCR_CLASSIFICATION_COUNTS_PATENTS = pd.read_excel(CONSTANTS_RESOURCES_FOLDER+"default_context_ipcr_classification_amounts_patents.xlsx", 
        index_col=0).squeeze("columns")
INDEX_DIRECTORY = "whoosh_index/"

DEFAULT_DELETE_ARGS = {"sleep":6, "retry":1, "aftersleep":5}
WORKING_DIRECTORY = ".lens_keywords/"

DEFAULT_INDEX_DIRECTORY = ".whoosh_index/"

STANDARD_KEYWORD_CUTOFF = 5

SEARCH_TRIES = 4
SEARCH_PAUSE = 2 # seconds



