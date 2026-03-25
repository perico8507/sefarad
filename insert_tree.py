with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('tree_snippet.html', 'r', encoding='utf-8') as f:
    tree_html = f.read()

# Insert at line 106 (index 105)
lines.insert(105, tree_html + '\n')

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
