import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('tree_snippet.html', 'r', encoding='utf-8') as f:
    tree_html = f.read()

# Find insertion point: right before <h2 id="El_Legado_Sefardí">
insertion_point = '<h2><span class="mw-headline" id="El_Legado_Sefardí">'

if insertion_point in content:
    new_content = content.replace(insertion_point, tree_html + '\n\n' + insertion_point)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Tree injected successfully.")
else:
    print("Insertion point not found.")
