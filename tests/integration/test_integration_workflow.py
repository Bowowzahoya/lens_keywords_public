import pandas as pd

from integration_context import lens_keywords_public, RESOURCES_FOLDER, OUTPUT_FOLDER, COMPARE_FOLDER
from integration_context import dataframes_equal, series_equal
from lens_keywords_public import workflow as wf

TEST_EXPORT_SCHOLARLY = pd.read_csv(RESOURCES_FOLDER+"medium.csv")
TEST_EXPORT_SCHOLARLY_WITH_QUOTES = pd.read_csv(RESOURCES_FOLDER+"green-hydrogen-scholarly.csv")
TEST_EXPORT_PATENTS = pd.read_csv(RESOURCES_FOLDER+"biochar_patents_raw.csv")
TEST_EXPORT_SCHOLARLY_FOR_KEYWORDS = pd.read_csv(RESOURCES_FOLDER+"biochar-scholarly.csv")
TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"metal-air-batteries_families_in_rest.xlsx")

COMPARE_FAMILIES = pd.read_excel(COMPARE_FOLDER+"families_keywords_full.xlsx", index_col=0)

COMPARE_KEYWORDS_WITH_CONTEXT = pd.read_excel(COMPARE_FOLDER+"scholarly_keywords_with_context.xlsx", index_col=0)
COMPARE_KEYWORDS_WITH_CONTEXT_PATENTS_KEYWORDS_BY_CONTEXT = pd.read_excel(COMPARE_FOLDER+"keywords_patents_with_context_keywords_by_context.xlsx", index_col=0)
COMPARE_KEYWORDS_WITH_CONTEXT_PATENTS_KEYWORDS_BY_SCHOLARLY = pd.read_excel(COMPARE_FOLDER+"keywords_patents_with_context_keywords_by_scholarly.xlsx", index_col=0)
COMPARE_IPCR_CLASSIFICATIONS_WITH_CONTEXT = pd.read_excel(COMPARE_FOLDER+"ipcr_classifications_with_context.xlsx", index_col=0)
COMPARE_SOURCE_TITLES_WITH_CONTEXT = pd.read_excel(COMPARE_FOLDER+"source_titles_with_context.xlsx", index_col=0)
COMPARE_SOURCE_TITLES_WITH_CONTEXT_WITH_QUOTES = pd.read_excel(COMPARE_FOLDER+"source_titles_with_context_with_quotes.xlsx", index_col=0)

def test_find_similar_keywords_scholarly():
    keywords_with_context, keywords_without_context = wf.find_similar_keywords_scholarly(TEST_EXPORT_SCHOLARLY, real_amount=82_642)
    keywords_with_context.to_excel(OUTPUT_FOLDER+"scholarly_keywords_with_context.xlsx")
    assert dataframes_equal(keywords_with_context, COMPARE_KEYWORDS_WITH_CONTEXT)

def test_find_similar_keywords_patents_keywords_by_context():
    keywords_with_context, keywords_without_context = wf.find_similar_keywords_patents(TEST_EXPORT_PATENTS, real_amount=5020)
    keywords_with_context.to_excel(OUTPUT_FOLDER+"keywords_patents_with_context_keywords_by_context.xlsx")
    assert dataframes_equal(keywords_with_context, COMPARE_KEYWORDS_WITH_CONTEXT_PATENTS_KEYWORDS_BY_CONTEXT)

def test_find_similar_keywords_patents_keywords_by_scholarly():
    keywords_with_context, keywords_without_context = wf.find_similar_keywords_patents(TEST_EXPORT_PATENTS, real_amount=5020,
        lens_export_scholarly_for_keywords=TEST_EXPORT_SCHOLARLY_FOR_KEYWORDS)
    keywords_with_context.to_excel(OUTPUT_FOLDER+"keywords_patents_with_context_keywords_by_scholarly.xlsx")
    assert dataframes_equal(keywords_with_context, COMPARE_KEYWORDS_WITH_CONTEXT_PATENTS_KEYWORDS_BY_SCHOLARLY)

def test_find_similar_ipcr_classifications():
    ipcr_classifications_with_context, ipcr_classifications_without_context = wf.find_similar_ipcr_classifications(TEST_EXPORT_PATENTS, real_amount=5020)
    ipcr_classifications_with_context.to_excel(OUTPUT_FOLDER+"ipcr_classifications_with_context.xlsx")
    assert dataframes_equal(ipcr_classifications_with_context, COMPARE_IPCR_CLASSIFICATIONS_WITH_CONTEXT)

def test_find_similar_source_titles():
    source_titles_with_context, source_titles_without_context  = wf.find_similar_source_titles(TEST_EXPORT_SCHOLARLY, real_amount=82_642)
    source_titles_with_context.to_excel(OUTPUT_FOLDER+"source_titles_with_context.xlsx")
    assert dataframes_equal(source_titles_with_context, COMPARE_SOURCE_TITLES_WITH_CONTEXT)

def test_find_similar_source_titles_with_quotes():
    source_titles_with_context, source_titles_without_context = wf.find_similar_source_titles(TEST_EXPORT_SCHOLARLY_WITH_QUOTES)
    source_titles_with_context.to_excel(OUTPUT_FOLDER+"source_titles_with_context_with_quotes.xlsx")
    assert dataframes_equal(source_titles_with_context, COMPARE_SOURCE_TITLES_WITH_CONTEXT_WITH_QUOTES)

def test_find_keywords_patent_families():
    families = wf.find_keywords_patent_families(TEST_FAMILIES, TEST_EXPORT_SCHOLARLY)
    families.to_excel(OUTPUT_FOLDER+"families_keywords_full.xlsx")
    assert dataframes_equal(families, COMPARE_FAMILIES)

