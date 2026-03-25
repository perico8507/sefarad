import re

def parse_gedcom(file_path):
    individuals = {}
    families = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_record = None
    current_id = None
    current_event = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 2)
        level = parts[0]
        
        if level == '0':
            if len(parts) > 2 and parts[2] in ['INDI', 'FAM']:
                current_id = parts[1]
                current_record = parts[2]
                if current_record == 'INDI':
                    individuals[current_id] = {'name': 'Desconocido', 'urls': [], 'fams': [], 'famc': [], 'birth': None, 'death': None}
                elif current_record == 'FAM':
                    families[current_id] = {'husb': None, 'wife': None, 'chil': []}
            current_event = None
        
        elif level == '1' and current_record == 'INDI':
            tag = parts[1]
            if tag == 'NAME' and len(parts) > 2:
                individuals[current_id]['name'] = parts[2].replace('/', '').strip()
            elif tag == 'FAMS' and len(parts) > 2:
                individuals[current_id]['fams'].append(parts[2])
            elif tag == 'FAMC' and len(parts) > 2:
                individuals[current_id]['famc'].append(parts[2])
            elif tag in ['BIRT', 'CHR']:
                current_event = 'birth'
            elif tag in ['DEAT', 'BUR']:
                current_event = 'death'
            else:
                current_event = None
                
        elif level == '2' and current_record == 'INDI':
            tag = parts[1]
            if tag == 'DATE' and len(parts) > 2 and current_event:
                date_str = parts[2]
                # Extract year
                year_match = re.search(r'\b(1[0-9]{3}|20[0-9]{2})\b', date_str)
                if year_match:
                    individuals[current_id][current_event] = year_match.group(1)
                
        elif level == '1' and current_record == 'FAM':
            tag = parts[1]
            if tag == 'HUSB' and len(parts) > 2:
                families[current_id]['husb'] = parts[2]
            elif tag == 'WIFE' and len(parts) > 2:
                families[current_id]['wife'] = parts[2]
            elif tag == 'CHIL' and len(parts) > 2:
                families[current_id]['chil'].append(parts[2])
                
        # Simple URL extraction
        if 'http' in line:
            urls = re.findall(r'(https?://[^\s]+)', line)
            if current_record == 'INDI' and current_id in individuals:
                individuals[current_id]['urls'].extend(urls)

    return individuals, families

indis, fams = parse_gedcom('Francisco Javier García Gaona.ged')

# Let's find the root person.
root_id = None
for i_id, i in indis.items():
    if 'Francisco Javier' in i['name'] and 'Gaona' in i['name']:
        root_id = i_id
        break

if not root_id and indis:
    root_id = list(indis.keys())[0]

# Generate HTML tree
def build_html_tree(ind_id, depth=0, max_depth=50, visited=None):
    if visited is None:
        visited = set()
    if not ind_id or ind_id not in indis or depth > max_depth or ind_id in visited:
        return ""
    
    visited.add(ind_id)
    ind = indis[ind_id]
    
    dates = []
    if ind['birth']: dates.append(f"b. {ind['birth']}")
    if ind['death']: dates.append(f"d. {ind['death']}")
    date_str = f" <span style='font-size:0.85em; color: #555; font-style: italic;'>({', '.join(dates)})</span>" if dates else ""
    
    html = f"<div class='tree-node' style='margin-left: {depth * 25}px; border-left: 1px solid #d4af37; padding-left: 10px; margin-bottom: 5px; position: relative;'>"
    html += f"<div style='position: absolute; left: -1px; top: 12px; width: 10px; height: 1px; background-color: #d4af37;'></div>"
    html += f"<strong style='color: #2c3e50; font-family: \"Libre Baskerville\", serif; font-size: 0.95em;'>{ind['name']}</strong>"
    html += date_str
    
    if ind['urls']:
        url = ind['urls'][0]
        html += f" <a href='{url}' target='_blank' style='font-size:0.75em; color: #a67c00; text-decoration: none;'>[Fuente]</a>"
    
    # We want ancestors (FAMC)
    for famc_id in ind['famc']:
        if famc_id in fams:
            fam = fams[famc_id]
            if fam['husb']:
                html += build_html_tree(fam['husb'], depth + 1, max_depth, visited.copy())
            if fam['wife']:
                html += build_html_tree(fam['wife'], depth + 1, max_depth, visited.copy())
    html += "</div>"
    return html

if root_id:
    tree_html = "<div class='family-tree-container' id='family-tree-container-div' style='background: #faf7f2; border: 1px solid #d4af37; padding: 20px; margin: 20px 0; overflow-x: auto; max-height: 800px; overflow-y: auto; box-shadow: inset 0 0 10px rgba(0,0,0,0.05);'>"
    tree_html += "<h3 style='font-family: \"Cinzel\", serif; color: #1a1a1a; margin-top:0;'>Árbol Genealógico Completo (Descendencia hasta 1500)</h3>"
    tree_html += build_html_tree(root_id, max_depth=50)  # PROFUNDIDAD DE 50 GENERACIONES
    tree_html += "</div>"
    
    with open('tree_snippet.html', 'w', encoding='utf-8') as f:
        f.write(tree_html)
    print("Tree HTML generated.")
