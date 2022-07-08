from .count import count_keywords, count_strings
from .context import add_context
from .keyword_column import get_keyword_column
from .workflow import find_similar_keywords_scholarly, find_similar_source_titles
from .workflow import find_similar_keywords_patents, find_similar_ipcr_classifications
from .workflow import find_keywords_patent_families, find_keywords_scholarly_export

import logging
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s: %(name)s / %(levelname)s - %(message)s', level=logging.INFO)