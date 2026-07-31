import re, json, os

html = open('ESTRATEGA/plan_julio2026.html', encoding='utf-8').read()

# Split into week sections by week-card id markers
# Find positions of each week card
week_starts = [(m.start(), m.group(1)) for m in re.finditer(r'class="week-card" id="(s\d+)"', html)]
# Also find end markers (end of month-content or next week-card or email panel)
month_end = html.find('<div class="email-panel"')

weeks = []

for idx, (start_pos, week_id) in enumerate(week_starts):
    # End position is next week card or month end
    if idx + 1 < len(week_starts):
        end_pos = week_starts[idx + 1][0]
    else:
        end_pos = month_end if month_end > 0 else len(html)
    
    section = html[start_pos:end_pos]
    
    # Extract week header
    week_head = re.search(r'<h2>S(\d+).*?(\d+ al \d+[^<]*)</h2>', section)
    week_num = week_head.group(1) if week_head else '?'
    week_dates = week_head.group(2).strip() if week_head else ''
    
    # Extract tags (actual tag text, not color codes)
    tags_match = re.search(r'<div class="tags">(.*?)</div>', section, re.DOTALL)
    tags = re.findall(r'<span[^>]*>(.*?)</span>', tags_match.group(1)) if tags_match else []
    
    # Extract focus (remove HTML tags)
    focus_match = re.search(r'Foco:\s*(.*?)</div>', section, re.DOTALL)
    focus = re.sub(r'<[^>]+>', '', focus_match.group(1)).strip() if focus_match else ''
    
    # Extract pieces
    pieces = []
    piece_starts = [(m.start(), m.group(1), int(m.group(2))) 
                    for m in re.finditer(r'class="piece piece-with-copy" data-format="([^"]*)"[^>]*data-piece="(\d+)"', section)]
    
    # Also extract data-brand if present
    piece_brands_attr = {}
    for m in re.finditer(r'class="piece piece-with-copy" data-format="([^"]*)"[^>]*data-piece="(\d+)"', section):
        # Get the data-brand attribute from the tag
        tag_start = m.start()
        tag_end = section.find('>', tag_start)
        tag_text = section[tag_start:tag_end]
        brand_match = re.search(r'data-brand="([^"]*)"', tag_text)
        brand = brand_match.group(1) if brand_match else None
        piece_brands_attr[int(m.group(2))] = brand
    
    for pidx, (ps, pfmt, pnum) in enumerate(piece_starts):
        if pidx + 1 < len(piece_starts):
            pend = piece_starts[pidx + 1][0]
        else:
            pend = len(section)
        
        phtml = section[ps:pend]
        
        # Num
        num_match = re.search(r'<div class="num">(.*?)</div>', phtml)
        num_text = num_match.group(1).strip() if num_match else str(pnum)
        
        # Fmt span
        fmt_match = re.search(r'<span class="fmt ([^"]*)"[^>]*>(.*?)</span>', phtml, re.DOTALL)
        fmt_class = fmt_match.group(1).strip() if fmt_match else pfmt
        fmt_text = fmt_match.group(2).strip() if fmt_match else ''
        fmt_text = re.sub(r'<[^>]+>', '', fmt_text).strip()
        
        # VE badge
        ve = 've-badge' in phtml
        
        # HP brand attribute
        data_brand = piece_brands_attr.get(pnum)
        
        # Pillar
        pillar_match = re.search(r'<div class="pillar">(.*?)</div>', phtml)
        pillar = pillar_match.group(1).strip() if pillar_match else ''
        
        # Topic
        topic_match = re.search(r'<div class="topic">(.*?)</div>', phtml, re.DOTALL)
        topic = re.sub(r'<[^>]+>', '', topic_match.group(1)).strip() if topic_match else ''
        
        # Brands
        brands_match = re.search(r'<div class="brands">(.*?)</div>', phtml)
        brands = brands_match.group(1).strip() if brands_match else ''
        
        # Day and date from column
        # Search backwards in section for col-head before this piece
        before = section[:ps]
        last_col = before.rfind('class="col-head"')
        day = date = ''
        if last_col > 0:
            col_m = re.search(r'<span class="day">(.*?)</span><span class="date">(.*?)</span>', before[last_col:last_col+200])
            if col_m:
                day = col_m.group(1).strip()
                date = col_m.group(2).strip()
        
        # Products
        products = []
        prods_match = re.search(r'<details class="prods">(.*?)</details>', phtml, re.DOTALL)
        if prods_match:
            for pm in re.finditer(r'<span class="name">(.*?)</span><span class="sku">(.*?)</span><span class="sto">(.*?)</span>', prods_match.group(1)):
                products.append({
                    'name': pm.group(1).strip(),
                    'sku': pm.group(2).strip(),
                    'sto': pm.group(3).strip()
                })
        
        # Copy data (slides)
        slides = []
        copy_match = re.search(r'<div class="copy-data"[^>]*>(.*?)</div>', phtml, re.DOTALL)
        if copy_match:
            try:
                slides = json.loads(copy_match.group(1).strip())
            except:
                slides = []
        
        pieces.append({
            'num': pnum,
            'numText': num_text,
            'format': pfmt,
            'fmtClass': fmt_class,
            'fmtText': fmt_text,
            'pillar': pillar,
            'topic': topic,
            'brands': brands,
            've': ve,
            'dataBrand': data_brand,
            'day': day,
            'date': date,
            'products': products,
            'slides': slides
        })
    
    weeks.append({
        'id': week_id,
        'num': week_num,
        'dates': week_dates,
        'tags': tags,
        'focus': focus,
        'pieces': pieces
    })

# Print summary
print('=== EXTRACTED DATA ===')
total_pieces = 0
for w in weeks:
    print(f'{w["id"]}: S{w["num"]} ({w["dates"]}) - {len(w["pieces"])} pieces')
    total_pieces += len(w["pieces"])
    for p in w['pieces']:
        ve_tag = ' VE' if p['ve'] else ''
        print(f'  #{p["num"]:2d} {p["day"]:3s} {p["date"]:2s} {p["format"]:10s} {p["pillar"]:14s} slides:{len(p["slides"])}{ve_tag}')
print(f'Total pieces: {total_pieces}')

# Count videos per week
total_videos = sum(1 for w in weeks for p in w['pieces'] if p['format'] == 'video')

# Generate JS
js_lines = []
js_lines.append('// Auto-generated from plan_julio2026.html')
js_lines.append('// Do not edit manually')
js_lines.append('')
js_lines.append("const MONTHS = {")
js_lines.append("  '2026-07': { label: 'Julio', year: 2026, pieces: %d, videos: %d, semanas: %d, ctx: 5 }," % (total_pieces, total_videos, len(weeks)))
js_lines.append("  '2026-08': { label: 'Agosto', year: 2026, pieces: 0, videos: 0, semanas: 0, ctx: 0 },")
js_lines.append("  '2026-09': { label: 'Septiembre', year: 2026, pieces: 0, videos: 0, semanas: 0, ctx: 0 },")
js_lines.append("  '2026-10': { label: 'Octubre', year: 2026, pieces: 0, videos: 0, semanas: 0, ctx: 0 },")
js_lines.append("  '2026-11': { label: 'Noviembre', year: 2026, pieces: 0, videos: 0, semanas: 0, ctx: 0 },")
js_lines.append("  '2026-12': { label: 'Diciembre', year: 2026, pieces: 0, videos: 0, semanas: 0, ctx: 0 },")
js_lines.append("};")
js_lines.append('')
js_lines.append("const MONTH_DATA = {")
js_lines.append("  '2026-07': {")
js_lines.append("    config: MONTHS['2026-07'],")
js_lines.append("    weeks: [")

for w in weeks:
    js_lines.append("      {")
    js_lines.append("        id: '%s'," % w['id'])
    js_lines.append("        num: %s," % w['num'])
    js_lines.append("        dates: '%s'," % w['dates'])
    js_lines.append("        tags: %s," % json.dumps(w['tags']))
    js_lines.append("        focus: %s," % json.dumps(w['focus']))
    js_lines.append("        pieces: [")
    
    for p in w['pieces']:
        js_lines.append("          {")
        js_lines.append("            num: %d," % p['num'])
        js_lines.append("            numText: '%s'," % p['numText'].replace("'", "\\'"))
        js_lines.append("            format: '%s'," % p['format'])
        js_lines.append("            fmtClass: '%s'," % p['fmtClass'])
        js_lines.append("            fmtText: %s," % json.dumps(p['fmtText']))
        js_lines.append("            pillar: '%s'," % p['pillar'])
        js_lines.append("            topic: %s," % json.dumps(p['topic']))
        js_lines.append("            brands: %s," % json.dumps(p['brands']))
        js_lines.append("            ve: %s," % json.dumps(p['ve']))
        js_lines.append("            dataBrand: %s," % json.dumps(p.get('dataBrand')))
        js_lines.append("            day: '%s'," % p['day'])
        js_lines.append("            date: '%s'," % p['date'])
        js_lines.append("            products: %s," % json.dumps(p['products'], ensure_ascii=False, indent=22).replace('\n', '\n' + ' ' * 22))
        js_lines.append("            slides: %s" % json.dumps(p['slides'], ensure_ascii=False, indent=22).replace('\n', '\n' + ' ' * 22))
        js_lines.append("          },")
    
    js_lines.append("        ]")
    js_lines.append("      },")

js_lines.append("    ]")
js_lines.append("  },")
js_lines.append("};")

js_content = '\n'.join(js_lines)

os.makedirs('_content', exist_ok=True)
with open('_content/data_julio.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f'\nWritten to _content/data_julio.js ({len(js_content)} bytes)')
