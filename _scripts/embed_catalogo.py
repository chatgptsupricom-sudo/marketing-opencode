import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js_path = os.path.join(base, '_scripts', 'catalogo_data.js')
html_path = os.path.join(base, 'ESTRATEGA', 'plan_julio2026.html')

with open(js_path, encoding='utf-8') as f:
    js_data = f.read()

with open(html_path, encoding='utf-8') as f:
    html = f.read()

old_tag = '<script src="../_scripts/catalogo_data.js"></script>'
inline_tag = '<script>\n' + js_data + '\n</script>'

if old_tag in html:
    html = html.replace(old_tag, inline_tag)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK - embedded catalogo data inline. New size:', len(html))
else:
    print('Tag not found - checking if already embedded')
    if 'const CATALOGO' in html:
        print('Already embedded.')
    else:
        print('ERROR: tag not found and data not present.')
