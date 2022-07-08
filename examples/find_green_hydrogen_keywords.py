"""
This script takes a Lens export of scholarly works, and finds similar keywords and source titles
to the search the export was originally based on.

This is based on occurence of keywords/source titles compared to overall occurence in the Lens.

The second part of the script does the same for patents, but then for keywords and IPCR classifications.

The results are exported to four Excel files with two tabs each. The tab 'With context' denotes keywords for which 
overall occurence in the Lens was identified. For the tab 'Without context', the overall occurence in the Lens
was too small to make it into the sample that is used for this contextualization, 
and only the counts in the Lens export is included.
"""
import os
import sys
import pandas as pd

# to make sure we can load the lens_keywords package in any environment:
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                            '../src'))
if package_path not in sys.path:
    sys.path.insert(0, package_path)

import lens_keywords_public as lk

# resources:
RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/")
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"out/")

# scholarly works:
areas = ["green-steam-reforming", "other-green-hydrogen-production", "hydrogen-fermentation", "biohydrogen",
    "hydrogen-transport", "hydrogen-usage", "hydrogen-storage", "hydrogen-catalysis"]
areas = []
for area in areas:
    print(area)
    lens_export_scholarly = pd.read_csv(RESOURCES_FOLDER+area+".csv")
    
    # find similar keywords
    scholarly_keywords_with_context, scholarly_keywords_without_context = lk.find_similar_keywords_scholarly(lens_export_scholarly)
    writer = pd.ExcelWriter(OUTPUT_FOLDER+f'{area}_scholarly_keywords_in_context.xlsx')
    scholarly_keywords_with_context.to_excel(writer, sheet_name="With Context")
    scholarly_keywords_without_context.to_excel(writer, sheet_name="Without Context")
    writer.save()

    # find similar source titles
    source_titles_with_context, source_titles_without_context = lk.find_similar_source_titles(lens_export_scholarly)
    writer = pd.ExcelWriter(OUTPUT_FOLDER+f'{area}_source_titles_in_context.xlsx')
    source_titles_with_context.to_excel(writer, sheet_name="With Context")
    source_titles_without_context.to_excel(writer, sheet_name="Without Context")
    writer.save()

# patents:
areas = ["green-steam-reforming"]
for area in areas:
    lens_export_scholarly = pd.read_csv(RESOURCES_FOLDER+area+".csv")
    lens_export_patents = pd.read_csv(RESOURCES_FOLDER+area+"_patents.csv")

    # find similar keywords
    patent_keywords_with_context, patent_keywords_without_context = lk.find_similar_keywords_patents(lens_export_patents, 
        lens_export_scholarly_for_keywords=lens_export_scholarly)
    writer = pd.ExcelWriter(OUTPUT_FOLDER+f'{area}_patent_keywords_in_context.xlsx')
    patent_keywords_with_context.to_excel(writer, sheet_name="With Context")
    patent_keywords_without_context.to_excel(writer, sheet_name="Without Context")
    writer.save()

    # find similar ipcr classifications
    ipcr_classifications_with_context, ipcr_classifications_without_context = lk.find_similar_ipcr_classifications(lens_export_patents)
    writer = pd.ExcelWriter(OUTPUT_FOLDER+f'{area}_ipcr_classifications_in_context.xlsx')
    ipcr_classifications_with_context.to_excel(writer, sheet_name="With Context")
    ipcr_classifications_without_context.to_excel(writer, sheet_name="Without Context")
    writer.save()
