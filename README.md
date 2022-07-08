# lens_keywords_public
Enables easier keyword analyses using Lens Scholarly and Lens Patents export.

There are four functions that make it easier to find similar content to a lens export. This can for example be used to create definitions of a field of science through keywords, source titles and patent categories.
- find_similar_keywords_scholarly()
- find_similar_source_titles()
- find_similar_keywords_patents()
- find_similar_ipcr_classifications()

Two other functions focus on adding a keyword column to a lens export for further analysis.
- find_keywords_patent_families()
- find_keywords_scholarly_export()

## Find similar keyword functions
### find_similar_keywords_scholarly()
takes a DataFrame of a lens scholarly export (possibly with the keywords in the query provided) and provides an overview of prevalence of co-occuring keywords.
They are ranked by occurence in the export compared to overall occurence in the whole of the Lens as context ('Ratio to Context'). This ranking is essentially an indication of how close/unique the keywords are to the content of the lens_export you used.
The overall occurence in the Lens was pre-calculated from 11 50,000 documents exports from 2010-2020 (550,000 documents in total),
and extrapolated to the expected amount for the whole of the Lens scholarly. 
You can also include your own occurence Series through the 'context_amounts' argument.

```
import lens_keywords as lk
lens_export = pd.read_csv("nanocrystals.csv")
keywords_with_context, keywords_without_context = \ 	
	lk.find_similar_keywords_scholarly(lens_export, 
		real_amount=82346, 
		queried_keywords=["nanocrystals", "nano crystals"])
```
						 
Setting the real_amount is necessary to get correct estimates if the export has hit the 50,000 limit of Lens and the actual search had more results.
queried_keywords specifies which keywords were queried for the provided lens_export (assumed queried in title, abstract and field_of_research). Please note the keywords needs to be all lower case.
If per_column=True, the amounts in abstract, title, keyword columns will also be calculated separately (slower). 

The function will return two dataframes. The first dataframe contains the keywords for which a context amount is available. The column 'Ratio to Context' is an indication of how specific the particular keyword is to your lens export. Please note that the context amounts included in the module are themselves estimates, and only include the years 2010-2020. Therefore it is possible to have a 'Ratio to Context' of over 1 (otherwise you would have to conclude a keyword in your lens_export has more mentions than the whole database).
The second DataFrame contains the keywords for which no context amount is available. This means the keywords have less mentions in the database than the smallest keyword included in the context. Therefore a 'Maximum Context Amount' and a 'Minimum Ratio to Context' can be calculated. These will often be more specific keywords.

### find_similar_source_titles()
Same as above but then for source titles.

### find_similar_keywords_patents()
Same as above but then for patent exports. Since patent exports in Lens don't have a keyword column (such as Field of Study in scholarly works), the function will use predetermined keywords by default, based on the context. However, it could be that the area you are looking at is too niche, and the keywords are too small to be included in the context. In this case, you could also opt to use a scholarly export to provide keywords, using the keyword 'lens_export_scholarly_for_keywords'.

```
import lens_keywords as lk
lens_export_patents = pd.read_csv("biochar-patents.csv")
lens_export_scholarly = pd.read_csv("biochar-scholarly.csv")
lk.find_similar_keywords_patents(lens_export_patents, 
    lens_export_scholarly_for_keywords=lens_export_scholarly)
```

### find_similar_ipcr_classifications()
Same as above but for IPCR classifications.

## Keyword column functions	 
### find_keywords_patent_families()
add a keyword column to a patent families DataFrame by using keywords extracted from titles and abstract column. A patent families DataFrame is assumed of the format that is exported by the "lens_analysis" package (see https://github.com/Bowowzahoya/lens_analysis).

```
families = find_keywords_patent_families(families, scholarly_export, cutoff=5)
```

### find_keywords_scholarly_export()
Same as above but then for scholarly exports.
