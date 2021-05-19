import pandas as pd
import re
import spacy
from rank_bm25 import BM25Okapi
import tkinter
import PIL
from PIL import Image, ImageOps
from PIL import ImageTk

MAX_WIDTH = 1500
MAX_HEIGHT = 690

def get_page_number (file_location):
    search = re.findall(r'\d+_\d+', file_location)
    return (search[1].split('_')[0])

# Adapted from https://stackoverflow.com/questions/17504570/creating-simply-image-gallery-in-python-tkinter-pil
# Handles Changing of Images
def move(delta):    
    global current
    if not (0 <= current + delta < len(locations)):
        tkMessageBox.showinfo('End', 'No more image.')
        return
    current += delta
    image = Image.open(locations[current])    

    # scale images to better fit screen
    width , height = image.size    
    if (height > MAX_HEIGHT):
        scaling_factor = MAX_HEIGHT / height
        height = MAX_HEIGHT
        width = round(width * scaling_factor)
    if (width > MAX_WIDTH):
        scaling_factor = MAX_WIDTH / width
        width = MAX_WIDTH
        height = round(height * scaling_factor)                    

    photo = ImageTk.PhotoImage(image)
    image = image.resize((width, height), Image.ANTIALIAS)    
    photo = ImageTk.PhotoImage(image)
    print(captions[current])    
    # generate label under image
    space = '      '        
    if (urls[current] != '-1'):
        url = urls[current]
    else:
        url = 'N/A'        
    photo_information = pmcs[current] + space + 'PAGE: ' + get_page_number(locations[current]) + space + 'URL: ' + urls[current] + space + 'IMPACT x RELEVANCE SCORE: ' + str(round(scores[current], 6))
    
    label['text'] = photo_information
    label['image'] = photo
    label.photo = photo

# Load Search Index
df = pd.read_csv('Search_Index.csv', header = None, engine = 'python')
pmc_ids = df.iloc[:, 0]        
influence_scores = df.iloc[:, 1]
image_captions = df.iloc[:, 2]
doi_urls = df.iloc[:, 3]
image_locations = df.iloc[:, 4]

# Tokenize Captions
nlp = spacy.load("en_core_web_sm")
tokenised_captions = []
corpus = nlp.pipe(image_captions.str.lower().values, disable = ['tagger', 'parser', 'ner', 'lemmatizer'])
for doc in corpus:
        token = [t.text for t in doc if t.is_alpha]
        tokenised_captions.append(token)
# Create BM25 Index
bm25 = BM25Okapi(tokenised_captions)

# Ask User for Input, Return Results
run = True
while (run == True):
    query = input("Enter Search Term(s): ")
    if (query == 'quit'):
        run = False
    else:
        tokenised_query = query.lower().split(" ")
        matching_scores = bm25.get_scores(tokenised_query)

        # get data associated with query results
        pmcs = []
        captions = []
        scores = []
        urls = []
        locations = []        
        for index, matching_score in enumerate(matching_scores):
            if (matching_score > 0):
                pmcs.append(pmc_ids[index])
                captions.append(image_captions[index])
                scores.append(matching_score * influence_scores[index])
                urls.append(doi_urls[index])
                locations.append(image_locations[index])        

        num_results = len(pmcs)

        # sort lists by score
        sorted_by_score = sorted(zip(pmcs, captions, scores, urls, locations), reverse = True, key = lambda x:x[2])
        pmcs, captions, scores, urls, locations = [[x[i] for x in sorted_by_score] for i in range(5)]    

        # UI Stuff
        current = 0

        root = tkinter.Tk()
        root.title(str(num_results) + ' Result(s) for "' + query.capitalize() + '":')

        label = tkinter.Label(root, compound = tkinter.TOP, bd = 4, font = ("Times", 19))
        label.pack()

        frame = tkinter.Frame(root)
        frame.pack()

        tkinter.Button(frame, text ='Previous picture', command = lambda: move(-1)).pack(side = tkinter.LEFT)
        tkinter.Button(frame, text = 'Next picture', command = lambda: move(+1)).pack(side = tkinter.LEFT)
        tkinter.Button(frame, text = 'Quit', command = root.quit).pack(side = tkinter.LEFT)

        move(0)

        root.mainloop()
        root.destroy()
