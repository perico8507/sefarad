import os
import re
import json
import difflib

# Configuration
GEDCOM_FILE = "/root/sefarad/Francisco Javier García Gaona.ged"
TRANS_DIR = 'transcripciones/'
MEDIA_EXTS = ('.jpeg', '.jpg', '.png', '.pdf')

def parse_gedcom(file_path):
    individuals = {}
    families = {}
    sources = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_record = None
    current_id = None
    current_event = None
    
    for line in lines:
        line = line.strip()
        if not line: continue
            
        parts = line.split(' ', 2)
        level = parts[0]
        
        if level == '0':
            if len(parts) > 2 and parts[2] in ['INDI', 'FAM', 'SOUR']:
                current_id = parts[1]
                current_record = parts[2]
                if current_record == 'INDI':
                    individuals[current_id] = {'full_name': 'Unknown', 'first_name': '', 'last_name': '', 'gender': 'U', 'birth_date': None, 'birth_place': None, 'death_date': None, 'death_place': None}
                elif current_record == 'FAM':
                    families[current_id] = {'husb': None, 'wife': None, 'chil': [], 'marr_date': None, 'marr_place': None}
                elif current_record == 'SOUR':
                    sources[current_id] = {'title': 'Untitled Source', 'author': None}
            current_event = None
        
        elif level == '1':
            tag = parts[1]
            if current_record == 'INDI':
                if tag == 'NAME' and len(parts) > 2:
                    full = parts[2].replace('/', '').strip()
                    individuals[current_id]['full_name'] = full
                    # Basic splitting
                    if ' ' in full:
                        individuals[current_id]['first_name'] = full.split(' ')[0]
                        individuals[current_id]['last_name'] = ' '.join(full.split(' ')[1:])
                elif tag == 'SEX' and len(parts) > 2:
                    individuals[current_id]['gender'] = parts[2]
                elif tag == 'BIRT': current_event = 'birth'
                elif tag == 'DEAT': current_event = 'death'
                elif tag == 'PLAC' and len(parts) > 2 and current_event:
                    individuals[current_id][f'{current_event}_place'] = parts[2]
            
            elif current_record == 'FAM':
                if tag == 'HUSB' and len(parts) > 2: families[current_id]['husb'] = parts[2]
                elif tag == 'WIFE' and len(parts) > 2: families[current_id]['wife'] = parts[2]
                elif tag == 'CHIL' and len(parts) > 2: families[current_id]['chil'].append(parts[2])
                elif tag == 'MARR': current_event = 'marr'
                elif tag == 'PLAC' and len(parts) > 2 and current_event == 'marr':
                    families[current_id]['marr_place'] = parts[2]

            elif current_record == 'SOUR':
                if tag == 'TITL' and len(parts) > 2: sources[current_id]['title'] = parts[2]
                elif tag == 'AUTH' and len(parts) > 2: sources[current_id]['author'] = parts[2]

        elif level == '2':
            tag = parts[1]
            if tag == 'DATE' and len(parts) > 2 and current_event:
                if current_record == 'INDI':
                    individuals[current_id][f'{current_event}_date'] = parts[2]
                elif current_record == 'FAM' and current_event == 'marr':
                    families[current_id]['marr_date'] = parts[2]

    return individuals, families, sources

def scan_transcriptions():
    trans = {}
    if not os.path.exists(TRANS_DIR): return trans
    for f in os.listdir(TRANS_DIR):
        if f.endswith('.txt'):
            with open(os.path.join(TRANS_DIR, f), 'r', encoding='utf-8', errors='ignore') as tf:
                trans[f] = tf.read()
    return trans

def scan_media():
    media = []
    for f in os.listdir('.'):
        if f.lower().endswith(MEDIA_EXTS):
            media.append(f)
    return media

def fuzzy_match(name, candidates):
    matches = difflib.get_close_matches(name, candidates, n=1, cutoff=0.6)
    return matches[0] if matches else None

def main():
    print("Parsing GEDCOM...")
    indis, fams, sours = parse_gedcom(GEDCOM_FILE)
    print(f"Found {len(indis)} individuals, {len(fams)} families.")
    
    transcriptions = scan_transcriptions()
    media_files = scan_media()
    
    # Matching Logic
    indi_names = {i['full_name']: id for id, i in indis.items()}
    name_list = list(indi_names.keys())
    
    citations = []
    
    print("Matching transcriptions and media...")
    for t_file, content in transcriptions.items():
        # Try to find person in filename
        clean_name = t_file.replace('.txt', '').replace('_', ' ')
        match = fuzzy_match(clean_name, name_list)
        if match:
            indi_id = indi_names[match]
            # Try to find corresponding media
            media_match = fuzzy_match(clean_name, media_files)
            citations.append({
                'individual_id': indi_id,
                'transcription': content,
                'file_name': media_match,
                'source_name': t_file
            })

    # Prepare final JSON
    data = {
        'individuals': indis,
        'families': fams,
        'sources': sours,
        'citations': citations
    }
    
    with open('supabase_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Extraction complete. {len(citations)} citations generated. Data saved to supabase_data.json")

if __name__ == "__main__":
    main()
