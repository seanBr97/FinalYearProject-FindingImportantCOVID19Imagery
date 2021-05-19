# FinalYearProject-FindingImportantCOVID19Imagery

ABSTRACT
The COVID-19 pandemic has resulted in an explosion of new information. This includes academic literature as well as deliberately false information designed to undermine public health responses. The World Health Organisation has declared this explosion of new information as an “infodemic”. During such a rapidly changing situation, there is a clear need to identify the important information from the unimportant. Here, a system is proposed to find important imagery related to COVID-19 to assist scientists and academics in their work. Importance is measured using the underlying citation network present among academic publications, this is referred to as the “impact” of a publication. The impact of a publication is used to lend credibility to the images contained inside it. Publications which have been identified as being high-impact are retrieved from the PubMed Central Open Access Subset and images are then extracted from these publications, indexed and made searchable by the corresponding figure caption. A user can then search this index to find high-impact images which match their search query. Three medical researchers evaluated the system and noted the usefulness of such a system as well as providing useful feedback for future improvements. Lastly, a new metric called the “Image Relevance Index” is proposed. This metric combines a number of common bibliometrics to more directly rank biological images contained within publications, rather than purely using the impact of the parent publication. This topic could be expanded upon in future research.

NOTE TO READER
To keep file size down, I have deleted most of the files from the pmc_archives, pmc_figures_captions, pmc_pdfs folders. 
I left a sample of 4 publications in these folders just so people can still see the typical inputs/outputs and also to run the system.

The oa_file_list was also reduced and now contains info for just these 4 publications as this file alone was roughly 500mb originally.

RUNNING PROGRAM
If you run search_engine.py (supports python 3.5+) and enter 'ct' as the search query it will return images from the sample of 4 publications (they were chosen because they all return images for that query specifically, just incase someone wanted to run the searcher).
