import pandas as pd
from numpy import log
from .constants import *


def count_strings_in_texts(strings:pd.Series, texts:pd.Series):
    texts = texts.fillna("")
    counts = strings.apply(lambda s: sum(texts.str.contains(s)))
    counts.index = strings.values
    return counts

def count_separated_strings(separated_strings:pd.Series, separator=SEPARATOR, remove_nan_index=True):
    split_strings = _split_strings(separated_strings, separator)
    counts = _value_counts_from_dataframe(split_strings)
    if remove_nan_index:
        counts = counts[counts.index.notnull()]
        if "" in counts.index:
            counts = counts.drop(index="")
    return counts

def _split_strings(strings:pd.Series, separator:str):
    split_strings = strings.str.split(separator, expand=True)
    return split_strings

def _value_counts_from_dataframe(dataframe):
    counts = pd.DataFrame([dataframe[col].value_counts() for col in dataframe.columns]).sum(axis=0)
    counts = counts.sort_values(ascending=False)
    return counts


def get_tfidf(term_amounts, all_term_amounts, reference_term_amounts, all_reference_term_amounts):
    tf = term_amounts/all_term_amounts
    idf = log(1/(reference_term_amounts/all_reference_term_amounts))
    idf.name = tf.name
    
    covered_ix = [ix for ix in tf.index if ix in idf.index]
    
    tfidf = pd.Series(index=tf.index)
    tfidf.loc[covered_ix] = tf[covered_ix]*idf[covered_ix]
    
    tfidf = tfidf.sort_values(ascending=False)
    tfidf.name = TFIDF_COL
    
    return tfidf
        
