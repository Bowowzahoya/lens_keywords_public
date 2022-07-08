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

RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/scholarly/")
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"out/scholarly/")

import lens_keywords
from lens_keywords import count as cnt

total_amount = 55_563_710 # 2010-2020 and has abstract
lens_export_all = pd.DataFrame()
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]:
    print(year)
    lens_export = pd.read_csv(RESOURCES_FOLDER+f"{year}.csv")
    lens_export_all = lens_export_all.append(lens_export, ignore_index=True)
 
print("Starting journal counting...")
journal_counts = pd.DataFrame()
lens_export_all["Source Title"] = lens_export_all["Source Title"].str.lower()
journal_counts["Amounts"] = lens_export_all["Source Title"].value_counts()
journal_counts["Compensated Amounts"] = journal_counts["Amounts"]*total_amount/len(lens_export_all)
print(journal_counts)
journal_counts.to_excel(OUTPUT_FOLDER+"Known_journal_counts.xlsx")

print("Starting keyword counting...")
keyword_amounts = cnt.count_keywords(lens_export_all, per_column = False,
                                      cutoff=10)
keyword_amounts["Amount"] = keyword_amounts["Count in All Columns"]*total_amount/len(lens_export_all)
print(keyword_amounts)
keyword_amounts.to_excel(OUTPUT_FOLDER+f"Known_keyword_counts.xlsx")

