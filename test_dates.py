import re
with open('tree_snippet.html', 'r', encoding='utf-8') as f:
    html = f.read()

dates = re.findall(r'b\. (\d{4})', html)
dates = [int(d) for d in dates]
if dates:
    print(f"Earliest year found: {min(dates)}")
    print(f"Total individuals with birth dates: {len(dates)}")
else:
    print("No dates found.")
