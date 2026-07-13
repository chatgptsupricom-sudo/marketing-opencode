import re, json

with open(r'C:\Users\MDIGITAL01\Desktop\MARKETING OPENCODE\_content\copys_s1_julio2026.md', 'r', encoding='utf-8') as f:
    md = f.read()

pieces = re.split(r'(?=## PIEZA #\d+)', md)
captions = {}

for p in pieces:
    m = re.match(r'## PIEZA #(\d+)', p)
    if not m:
        continue
    num = int(m.group(1))
    m2 = re.search(r'### CAPTION\s*\n(.*?)(?:\n---|\n## PIEZA|\Z)', p, re.DOTALL)
    if m2:
        cap = m2.group(1).strip()
        captions[num] = cap

with open(r'C:\Users\MDIGITAL01\Desktop\MARKETING OPENCODE\ESTRATEGA\plan_julio2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

cap_json = json.dumps({k: captions[k] for k in sorted(captions.keys())}, ensure_ascii=False, indent=2)
cap_js_block = '// --- CAPTIONS DATA ---\nconst CAPTIONS = ' + cap_json + ';\n\n'

marker = '// \u2500\u2500\u2500 EXPAND/COLLAPSE (non-copy pieces) \u2500\u2500\u2500'
html = html.replace(marker, cap_js_block + marker)

with open(r'C:\Users\MDIGITAL01\Desktop\MARKETING OPENCODE\ESTRATEGA\plan_julio2026.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Embedded {len(captions)} captions OK')
