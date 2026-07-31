import re

html_path = 'ESTRATEGA/plan_julio2026.html'
iso_b64_path = '_assets/_iso_b64.txt'

with open(html_path, encoding='utf-8') as f:
    html = f.read()

with open(iso_b64_path, encoding='utf-8') as f:
    iso_b64 = f.read()

# Find the isotipo img tag in hero section
pattern = r'<img src="data:image/png;base64,[^"]+" alt="SUPRICOM" style="height:64px;width:auto">'
match = re.search(pattern, html)

if match:
    new_tag = '<img src="' + iso_b64 + '" alt="SUPRICOM" style="height:160px;width:auto;">'
    html = html[:match.start()] + new_tag + html[match.end():]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated isotipo to 160px with transparent bg')
else:
    print('Old tag not found')
