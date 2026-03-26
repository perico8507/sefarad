import os
import glob
import re
import unicodedata
import json

TRANSCRIPCIONES_DIR = 'transcripciones'
PERFILES_DIR = 'perfiles'
ACTAS_DIR = 'assets/actas'
INDEX_FILE = 'index.html'
DATA_FILE = 'supabase_data.json'

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil de {name} - Museo Sefarad MX</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/profile.css">
</head>
<body oncontextmenu="return false;">
    <div class="zoom-overlay" id="zoomOverlay" onclick="this.style.display='none'">
        <img id="zoomImg" src="" oncontextmenu="return false;" draggable="false">
    </div>

    <div class="container">
        <a href="../index.html" class="back-link">← Volver al Archivo Central</a>
        
        <h1>Expediente Histórico: {name}</h1>
        
        {image_html}
        
        <h2>Transcripción Paleográfica</h2>
        <div class="transcription-box">{transcription}</div>

        <div class="lineage-vault">
            <h2>Mapa de Linaje Dinámico</h2>
            <div id="tree-content">
                <p style="color: #888; font-style: italic;">Cargando conexiones del linaje...</p>
            </div>
        </div>
    </div>

    <script src="../js/tree.js"></script>
    <script>
        function zoomImage(src) {{
            document.getElementById('zoomImg').src = src;
            document.getElementById('zoomOverlay').style.display = 'block';
        }}
        
        // Initialize tree for this specific individual
        document.addEventListener('DOMContentLoaded', () => {{
            const indiId = "{indi_id}";
            if (indiId && window.initDynamicTree) {{
                window.initDynamicTree(indiId);
            }}
        }});
    </script>
</body>
</html>
"""

def remove_accents(input_str):
    if not input_str: return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_str(s):
    return re.sub(r'[^a-zA-Z0-9]', '', remove_accents(s).lower())

def get_tokens(s):
    words = re.split(r'[^a-zA-Z0-9]+', remove_accents(s).lower())
    return set(w for w in words if len(w) > 2 and w not in ['de', 'la', 'del', 'los', 'las', 'y'])

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def find_best_indi(base_name, data):
    if not data: return ""
    clean_base = clean_str(base_name)
    best_id = ""
    
    # Try exact or partial match in full_name
    for indi_id, info in data['individuals'].items():
        if clean_base in clean_str(info['full_name']) or clean_str(info['full_name']) in clean_base:
            return indi_id
            
    return ""

def generate_profiles():
    os.makedirs(PERFILES_DIR, exist_ok=True)
    
    data = load_data()
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
            
        # Match individual ID
        indi_id = find_best_indi(base_name, data)
            
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
            <img src="../assets/actas/{best_match}" alt="Documento Original de {display_name}" onclick="zoomImage(this.src)" oncontextmenu="return false;" draggable="false">
            <p style="color: #888; font-size: 0.85em; font-style: italic; margin-top: 10px;">Manuscrito Original (Clic para ampliar)</p>
        </div>'''
        
        html_content = TEMPLATE.format(
            name=display_name,
            image_html=image_html,
            transcription=transcription_text,
            indi_id=indi_id
        )
        
        html_filename = f"{base_name.lower()}.html"
        html_path = os.path.join(PERFILES_DIR, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        generated_links.append((display_name, html_filename))
        
    return generated_links

def update_index(generated_links):
    if not os.path.exists(INDEX_FILE): return
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Build new list HTML
    list_html = "<ul>\n"
    for display_name, html_filename in sorted(generated_links, key=lambda x: x[0]):
        list_html += f'            <li><a href="perfiles/{html_filename}">Expediente: {display_name}</a><br><span style="font-size: 0.8em; color: #888;">Archivo Sefarad MX</span></li>\n'
    list_html += "        </ul>"
    
    # Inject into index.html using placeholder
    placeholder = "<!-- LISTA_EXPEDIENTES -->"
    if placeholder in content:
        new_content = content.replace(placeholder, list_html)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("index.html updated successfully via placeholder.")
    else:
        # Fallback to regex
        pattern = re.compile(r'(<div class="documents-hall"[^>]*>\s*)<ul>.*?</ul>(\s*</div>)', re.DOTALL)
        if pattern.search(content):
            new_content = pattern.sub(rf'\g<1><ul>\n{list_html}\n</ul>\g<2>', content)
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("index.html updated successfully via regex.")
        else:
            print("Could not find injection point in index.html")

if __name__ == '__main__':
    links = generate_profiles()
    print(f"Generated {len(links)} HTML profiles.")
    update_index(links)
