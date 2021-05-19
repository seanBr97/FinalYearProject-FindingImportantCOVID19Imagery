import os
from ftplib import FTP
import re

ftp_url = 'ftp.ncbi.nlm.nih.gov'
ftp_path = 'pub/pmc'
ftp = FTP(ftp_url)
ftp.login()
ftp.cwd(ftp_path)

# Example: ftp_location: oa_package/**/**/PMC123456.tar.gz

# Outputs 'oa_package/**/**'
def get_prefix (ftp_location):    
    return (ftp_location[:16])

# Outputs 'PMC123456.tar.gz'
def get_filename (ftp_location):    
    search = re.search('PMC(.+?).tar.gz', ftp_location)
    return (search.group(0))

# Saves to CWD
def get_oa_file_list():    
    filename = 'oa_file_list.csv'
    ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)    

# Save Tar Files From PMC FTP Server to output_directory
def get_archive_files(ftp_locations, output_directory):
    top_level_directory = os.getcwd()    
    os.chdir(output_directory)    
    ftp_parent_directory = ftp.pwd()    
            
    for location in ftp_locations:    
        if (location != '-1'):            
            ftp.cwd(get_prefix(location))
            filename = get_filename(location)                
            ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
            ftp.cwd(ftp_parent_directory)
    os.chdir(top_level_directory)
