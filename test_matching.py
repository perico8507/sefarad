import os
import glob
import re
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_str(s):
    return re.sub(r'[^a-zA-Z0-9]', '', remove_accents(s).lower())

def get_tokens(s):
    # split by anything that isn't a letter or number
    words = re.split(r'[^a-zA-Z0-9]+', remove_accents(s).lower())
    return set(w for w in words if len(w) > 2 and w not in ['de', 'la', 'del', 'los', 'las', 'y'])

ACTAS_DIR = 'assets/actas'
TRANSCRIPCIONES_DIR = 'transcripciones'

images = glob.glob(os.path.join(ACTAS_DIR, '*'))
txt_files = glob.glob(os.path.join(TRANSCRIPCIONES_DIR, '*.txt'))

image_basenames = {os.path.basename(img): get_tokens(os.path.basename(img)) for img in images}

matches = {}
for txt_path in txt_files:
    filename = os.path.basename(txt_path)
    base_name = os.path.splitext(filename)[0]
    txt_tokens = get_tokens(base_name)
    
    best_match = None
    best_score = 0
    for img_name, img_tokens in image_basenames.items():
        overlap = len(txt_tokens.intersection(img_tokens))
        if overlap > best_score:
            best_score = overlap
            best_match = img_name
            
    if best_score <= 1: # if poor token match, try substring
        c_txt = clean_str(base_name)
        for img_name in image_basenames.keys():
            c_img = clean_str(img_name)
            if c_txt in c_img or c_img in c_txt:
                best_match = img_name
                best_score = 99
                break

    matches[txt_path] = (best_match, best_score)

no_matches = []
for txt, (img, score) in matches.items():
    if not img or score == 0:
        no_matches.append(txt)

print(f"Matches found: {len(matches) - len(no_matches)} out of {len(txt_files)}")
if no_matches:
    print("NO MATCH FOR:")
    for nm in no_matches:
        print(nm)
