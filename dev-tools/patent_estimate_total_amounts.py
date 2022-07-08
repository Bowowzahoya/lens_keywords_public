"""
A tool to estimate context amounts for keywords based on broad Lens exports
"""
import os
import sys
import pandas as pd

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                            '../src'))
if package_path not in sys.path:
    sys.path.insert(0, package_path)
print(package_path)

RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/patent/")
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"out/patent/")

import lens_keywords
from lens_keywords import count as cnt
from lens_keywords import utils as ut

total_amount = 54_922_120 # 2010-2020 patent documents
lens_export_all = pd.DataFrame()
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]:
    print(year)
    lens_export = pd.read_csv(RESOURCES_FOLDER+f"{year}.csv")
    lens_export_all = lens_export_all.append(lens_export, ignore_index=True)
 
def count_keywords():
    filename_keywords_from_scholarly = "Known_keyword_counts.xlsx"
    folder_keywords_from_scholarly = os.path.join(os.path.dirname(os.path.realpath(__file__)),"out/scholarly/")
    keywords_from_scholarly = pd.read_excel(folder_keywords_from_scholarly+filename_keywords_from_scholarly, index_col=0)
    print("Starting keyword counting...")
    keyword_amounts = cnt.count_strings(lens_export_all, keywords_from_scholarly.index.astype(str).to_list(), 
                                        per_column=False,
                                        keyword_columns=[])
    keyword_amounts["Amount"] = keyword_amounts["Count in All Columns"]*total_amount/len(lens_export_all)
    print(keyword_amounts)
    keyword_amounts.to_excel(OUTPUT_FOLDER+f"Known_keyword_counts_patents.xlsx")
    
def count_classifications():
    keyword_amounts = ut.count_separated_strings(lens_export_all["IPCR Classifications"], separator=";;")
    keyword_amounts.name = "Count"
    keyword_amounts = pd.DataFrame(keyword_amounts)
    keyword_amounts["Amount"] = keyword_amounts["Count"]*total_amount/len(lens_export_all)
    print(keyword_amounts)
    keyword_amounts.to_excel(OUTPUT_FOLDER+f"Known_classification_counts.xlsx")
    
count_keywords()


