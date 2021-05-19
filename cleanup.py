import os
import shutil
from glob import glob

# DELETE IMAGES WITH NO CAPTION (NON-SEARCHABLE/JUNK EXTRACTS)

def get_file_extension(filename):
    return (filename[-4:])

def extension_to_text(filename):
    return (filename[:-4] + '.txt')

def is_jpg (filename):
    return (get_file_extension(filename) == '.jpg')
    

# Delete Images Without Captions && Folders Without Images
def cleanup():    
    root = os.getcwd()
    fig_cap_directory = os.path.join(os.getcwd(), 'pmc_figures_captions')
    fig_cap_files = os.listdir(fig_cap_directory)    
    for item in fig_cap_files:
        path = os.path.join(fig_cap_directory, item)
        if (os.path.isdir(path)):
            output_files = os.listdir(path)
            for file in output_files:            
                # If no text file associated with image --> delete image
                if ( (is_jpg(file)) and (extension_to_text(file) not in output_files) ):
                    os.remove(os.path.join(path, file))
                
            # if folder has no images --> delete it
            os.chdir(path)        
            if not glob('*.jpg'):
                    os.chdir(os.path.join(path, '..'))
                    shutil.rmtree(path)
    os.chdir(root)
