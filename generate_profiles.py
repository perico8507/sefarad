import os
import glob
import re
import unicodedata

TRANSCRIPCIONES_DIR = 'transcripciones'
PERFILES_DIR = 'perfiles'
ACTAS_DIR = 'assets/actas'
INDEX_FILE = 'index.html'

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil de {name} - Museo Sefarad MX</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0d0c0b;
            --text-main: #e8e3d9;
            --accent-gold: #d4af37;
            --accent-gold-dim: #8b7355;
            --card-bg: #161513;
        }}
        
        body {{
            font-family: 'Libre Baskerville', serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            background-image: radial-gradient(circle at center, #1a1816 0%, #0d0c0b 100%);
            background-attachment: fixed;
        }}
        
        .container {{
            max-width: 900px;
            margin: 50px auto;
            padding: 40px;
            background: var(--card-bg);
            border: 1px solid #2a2620;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 15px rgba(212, 175, 55, 0.1);
            position: relative;
        }}
        
        .container::before {{
            content: '';
            position: absolute;
            top: 10px; left: 10px; right: 10px; bottom: 10px;
            border: 1px solid var(--accent-gold-dim);
            pointer-events: none;
        }}

        .back-link {{
            color: var(--accent-gold-dim);
            text-decoration: none;
            font-family: 'Cinzel', serif;
            font-size: 0.9em;
            display: inline-block;
            margin-bottom: 20px;
            transition: color 0.3s ease;
            position: relative;
            z-index: 2;
        }}

        .back-link:hover {{
            color: var(--accent-gold);
        }}

        h1, h2 {{
            font-family: 'Cinzel', serif;
            color: var(--accent-gold);
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.2em;
            margin-bottom: 30px;
            border-bottom: 2px solid var(--accent-gold-dim);
            padding-bottom: 20px;
        }}

        .document-container {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .document-container img {{
            max-width: 100%;
            border: 3px solid #000;
            box-shadow: 0 15px 30px rgba(0,0,0,0.8);
            filter: sepia(20%);
        }}
        
        .transcription-box {{
            background: #050505;
            padding: 30px;
            border-left: 3px solid var(--accent-gold);
            font-family: 'Libre Baskerville', serif;
            color: #ccc;
            white-space: pre-wrap;
            margin-top: 30px;
            box-shadow: inset 0 0 20px rgba(0,0,0,1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← Volver a la Galería</a>
        
        <h1>Archivo Histórico: {name}</h1>
        
        {image_html}
        
        <h2>Transcripción del Documento</h2>
        <div class="transcription-box">{transcription}</div>
    </div>
</body>
</html>
"""

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_str(s):
    return re.sub(r'[^a-zA-Z0-9]', '', remove_accents(s).lower())

def get_tokens(s):
    words = re.split(r'[^a-zA-Z0-9]+', remove_accents(s).lower())
    return set(w for w in words if len(w) > 2 and w not in ['de', 'la', 'del', 'los', 'las', 'y'])

def generate_profiles():
    os.makedirs(PERFILES_DIR, exist_ok=True)
    
    txt_files = glob.glob(os.path.join(TRANSCRIPCIONES_DIR, '*.txt'))
    images = glob.glob(os.path.join(ACTAS_DIR, '*'))
    
    image_basenames = {os.path.basename(img): get_tokens(os.path.basename(img)) for img in images}
    
    generated_links = []
    
    for txt_path in txt_files:
        filename = os.path.basename(txt_path)
        base_name = os.path.splitext(filename)[0]
        display_name = base_name.replace('_', ' ').replace('FS', '').strip()
        txt_tokens = get_tokens(base_name)
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            transcription_text = f.read()
            
        # Match image
        best_match = None
        best_score = 0
        for img_name, img_tokens in image_basenames.items():
            overlap = len(txt_tokens.intersection(img_tokens))
            if overlap > best_score:
                best_score = overlap
                best_match = img_name
                
        if best_score <= 1:
            c_txt = clean_str(base_name)
            for img_name in image_basenames.keys():
                c_img = clean_str(img_name)
                if c_txt in c_img or c_img in c_txt:
                    best_match = img_name
                    break
                    
        image_html = ""
        if best_match:
            image_html = f'''
        <div class="document-container">
            <img src="../assets/actas/{best_match}" alt="Documento Original de {display_name}">
            <p style="color: #888; font-size: 0.85em; font-style: italic; margin-top: 10px;">Manuscrito Original</p>
        </div>'''
        
        html_content = TEMPLATE.format(
            name=display_name,
            image_html=image_html,
            transcription=transcription_text
        )
        
        html_filename = f"{base_name.lower()}.html"
        html_path = os.path.join(PERFILES_DIR, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        generated_links.append((display_name, html_filename))
        
    return generated_links

def update_index(generated_links):
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Build new list HTML
    list_html = "<ul>\n"
    for display_name, html_filename in sorted(generated_links, key=lambda x: x[0]):
        list_html += f'            <li><a href="perfiles/{html_filename}">Expediente: {display_name}</a><br><span style="font-size: 0.8em; color: #888;">Archivo Sefarad MX</span></li>\n'
    list_html += "        </ul>"
    
    # Inject into index.html
    pattern = re.compile(r'(<div class="documents-hall">\s*)<ul>.*?</ul>(\s*</div>)', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(rf'\g<1>{list_html}\g<2>', content)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("index.html updated successfully with new profile links.")
    else:
        print("Could not find <div class=\"documents-hall\"> in index.html")

if __name__ == '__main__':
    links = generate_profiles()
    print(f"Generated {len(links)} HTML profiles.")
    update_index(links)
