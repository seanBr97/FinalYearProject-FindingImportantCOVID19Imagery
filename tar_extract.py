import tarfile
import os

def get_pmcid (filename):        
    pmcid = filename[:-7]
    return pmcid    

# Extract PDF Files From 'tar.gz' Archives to a Destination Folder
def extract_archives():
    tar_directory = os.path.join(os.getcwd(), 'pmc_archives')
    pdf_directory = os.path.join(os.getcwd(), 'pmc_pdfs')       # input folder for docker
        
    tar_files = os.listdir(tar_directory)

    for tar_file in tar_files:    
        with tarfile.open(os.path.join(tar_directory, tar_file), "r") as tar:
            pmcid = get_pmcid(tar_file)
            archive_files = tar.getmembers()
            x = 1
            # extract pdfs files from tar archive
            for file in archive_files:
                if file.name.endswith('.pdf'):
                    file.name = os.path.basename(file.name)                                                    
                    tar.extract(file, pdf_directory)                                
                    new_name = pmcid + '_' + str(x) + '.pdf'
                    os.rename(os.path.join(pdf_directory, file.name), os.path.join(pdf_directory, new_name))                    
                    x += 1        
            tar.close()
            # delete tar file
            #tar_path = os.path.join(tar_directory, tar_file)
            #os.remove(tar_path)
