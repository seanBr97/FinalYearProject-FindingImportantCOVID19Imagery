import os
import csv
import pandas as pd
from cleanup import extension_to_text, is_jpg

def get_pmcid (filename):        
    return (filename.split('_')[0])

def get_pmc_score_pairs(df, pmc_ids):        
    influence_scores = df.iloc[:, 3]
    #popularity_scores = df.iloc[:, 5]
    return(dict(zip(pmc_ids, influence_scores)))

def get_pmc_doi_pairs(df, pmc_ids):
    doi_names = df.iloc[:, 2]
    return(dict(zip(pmc_ids, doi_names)))

# Traverse 'pmc_figures_captions' Directory and Store the Location & Metadata of Every Image
def create_search_index(ranked_dataset_name):    
    df = pd.read_csv(ranked_dataset_name, header = None, keep_default_na = False)
    pmc_ids = df.iloc[:, 1]        
    pmc_score_pairs = get_pmc_score_pairs(df, pmc_ids)
    pmc_doi_pairs = get_pmc_doi_pairs(df, pmc_ids)

    pmc_ids = []
    scores = []
    captions = []
    urls = []
    locations = []
    
    fig_cap_directory = os.path.join(os.getcwd(), 'pmc_figures_captions')
    fig_cap_files = os.listdir(fig_cap_directory)
        for item in fig_cap_files:        
        path = os.path.join(fig_cap_directory, item)        
        if (os.path.isdir(path)):                        
            pmc_id = get_pmcid(item)        
            score = pmc_score_pairs[pmc_id]                
            output_files = os.listdir(path)
            if (pmc_doi_pairs[pmc_id] != 'N/A'):
                url = 'doi.org/' + pmc_doi_pairs[pmc_id]    
            else:
                url = '-1'
            for file in output_files:
                if (is_jpg(file)):                    
                    pmc_ids.append(pmc_id)                    
                    scores.append(score)
                    # some characters use an undefined encoding, ignore these
                    with open(os.path.join(path, extension_to_text(file)), errors = 'ignore') as f:
                        captions.append(f.readline())
                        f.close()
                    urls.append(url) 
                    locations.append(os.path.join(path, file))
                    
       # write final outputs to a csv
        rows = zip(pmc_ids, scores, captions, urls, locations)
        with open('Search_Index.csv', "w", newline = "", encoding = "utf-8") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
            f.close()
