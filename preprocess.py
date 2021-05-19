import pandas as pd
import csv

# Creates New Dataset Containing Just PMC Publications 
def filter_dataset(dataset_name, column):
    filtered_dataset_name = dataset_name[:-4] + '_filtered.csv'
    with open(dataset_name, 'r', encoding = 'utf8') as raw, open(filtered_dataset_name, 'w', newline = '', encoding = 'utf8') as filtered:
        writer = csv.writer(filtered)
        for row in csv.reader(raw):
            if (row[column] != 'N/A'):
                writer.writerow(row)

# Row Selection Code Adapted From : https://www.daniweb.com/programming/software-development/threads/455130/copy-specific-rows-from-a-cvs-file-to-another-cvs-file
# Take Sample of Size 'sample_size' From the Ranked Dataset and Create a new CSV
def get_sample(sample_size, filename):    
    with open(filename[:-4] + str(sample_size) + '.csv', 'w', newline = '', encoding = 'utf8') as output:
        writer = csv.writer(output)
        with open(filename, 'r', encoding = 'utf8') as input:
            reader = csv.reader(input)
            for counter, row in enumerate(reader):
                if counter < 0: continue
                if counter >= sample_size: break
                writer.writerow(row)    

# Use Dictionary Containing oa_file_list's 'pmc + ftp_locations' Pairs to Return a List of Ftp Locations for PMC Entries in Ranked Dataset
def get_ranked_ftp_locations (pmc_all, ftp_locations, pmc_ranked):    
    ranked_ftp_locations = []
    pmc_ftp_pairs = dict(zip(pmc_all, ftp_locations))
    for pmc in pmc_ranked:
        ranked_ftp_locations.append(pmc_ftp_pairs.get(pmc, '-1'))
    return ranked_ftp_locations

# Write 'ftp_locations' to the Last Column of Input File (hardcoded as the 8th column)
def add_ftp_locations(ranked_dataset_filename):
    # read in open access subset index file
    df = pd.read_csv("oa_file_list.csv")
    pmc_all = df.iloc[:, 2]
    ftp_locations = df.iloc[:, 0]

    # articles_by_influence.csv
    df = pd.read_csv(ranked_dataset_filename, header = None)
    pmc_ranked = df.iloc[:, 1]    
    columns = [df.iloc[:,0],df.iloc[:,1],df.iloc[:,2],df.iloc[:,3],df.iloc[:,4],df.iloc[:,5],df.iloc[:,6],df.iloc[:,7]]

    ranked_ftp_locations = get_ranked_ftp_locations(pmc_all, ftp_locations, pmc_ranked)

    # write final outputs to a csv
    rows = zip(columns[0],columns[1],columns[2],columns[3],columns[4],columns[5],columns[6],columns[7],ranked_ftp_locations)
    with open(ranked_dataset_filename, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
        f.close()


