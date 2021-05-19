import os
import subprocess
import pandas as pd
from preprocess import filter_dataset, get_sample, add_ftp_locations
from pmc_ftp import get_oa_file_list, get_archive_files
from tar_extract import extract_archives
from cleanup import cleanup
from search_index import create_search_index

pmcid_column_number = 1

# Prerequisites: HAVE IMPACT METRICS DATASET IN THE CURRENT DIRECTORY, articles_by_influence.csv in this case
# Output : EXTRACTED FIGURES & CAPTIONS IN A CHOSEN DIRECTORY

# oa_file_list contains ftp locations for every pmc entry in the oa subset
print('Getting Open Access File List...')
get_oa_file_list()


# create new impact metric dataset containing only pmc entries
print('Creating PMC Dataset...')
filter_dataset('articles_by_influence.csv', pmcid_column_number)

# take sample of size 'sample_size' from the ranked dataset and create a new csv
sample_size = 100
print('Creating Sample of size', sample_size)
get_sample(sample_size, 'articles_by_influence_filtered.csv')

# append ftp locations to the filtered dataset
print('Finding file locations on PMC FTP server...')
add_ftp_locations('articles_by_influence_filtered100.csv')

# download archive files for pmc publications
print('Downloading PMC archive files....')
df = pd.read_csv('articles_by_influence_filtered100.csv', header = None)
ftp_locations = df.iloc[:,8]
get_archive_files(ftp_locations, os.path.join(os.getcwd(), 'pmc_archives'))

# extract PDF files from archives
print('Extracting PDFs from archive files....')
extract_archives()

# extract figures&captions with PDFigCapx running in Docker
# executed by a shell script which runs in the background
print('Extracting figures and captions from PDFs....')                   
input_folder = os.path.join(os.getcwd(), 'pmc_pdfs')
output_folder = os.path.join(os.getcwd(), 'pmc_figures_captions')
container_name = 'new_curation:clean'   
command = 'docker run -w /home/curation-pipeline/src/test -it -v "' + input_folder + '":/mnt/input -v "' + output_folder + '":/mnt/output ' + container_name + ' /bin/bash -c "python3 test_pdfigcapx.py"'
subprocess.run(command, shell = True)

# remove figures with no captions 
print('Cleaning up figures & captions....')
cleanup()

# create search index 
print('Creating Search Index')
create_search_index('articles_by_influence_filtered100.csv')

print("Finished!")
