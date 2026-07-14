import re

with open('ESTRATEGA/plan_julio2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

videos = {
    3:  'FORZA. La marca que los comercios conocen y piden. Showcase visual de la l\u00ednea de protecci\u00f3n.',
    5:  'Dato clave sobre protecci\u00f3n el\u00e9ctrica. Visualizaci\u00f3n educativa.',
    7:  '\u00abTu cliente compra una laptop. \u00bfLe ofreces protecci\u00f3n?\u00bb. C\u00f3mo aumentar el ticket cuidando la inversi\u00f3n del cliente.',
    9:  '\u00abLo que est\u00e1 pasando con la protecci\u00f3n el\u00e9ctrica en Venezuela\u00bb. An\u00e1lisis del contexto, tendencias de compra, Q3.',
    11: 'NEXXT HOME + HAVIT + TP-LINK. Portafolio completo de seguridad. Showcase visual.',
    15: 'Dato clave sobre conectividad. Visualizaci\u00f3n educativa.',
    17: '\u00abTodo lo que tu cliente necesita para no perder vigilancia ni conectividad\u00bb. El vocero arma el combo.',
    19: '\u00abEl futuro de la conectividad\u00bb. WiFi 6, MESH, hogares inteligentes. Hacia d\u00f3nde va.',
    21: 'MSI Mini PC. Potencia compacta. Por qu\u00e9 los negocios migran a este formato.',
    25: '\u00ab\u00bfCu\u00e1nto dura un UPS en un apag\u00f3n?\u00bb. Clave para dimensionar correctamente.',
    27: '\u00abPrepara tu inventario para Q3\u00bb. El vocero comparte su visi\u00f3n de cierre de mes.',
    29: '\u00abQ3: lo que viene en protecci\u00f3n, conectividad y c\u00f3mputo\u00bb. Reflexi\u00f3n sobre el mercado.'
}

for piece_num, title in videos.items():
    # 1. Change opening div
    old_open = (
        f'      <div class="piece" data-format="video" onclick="togglePiece(this)">\n'
        f'        <div class="num">{piece_num}</div>'
    )
    new_open = (
        f'      <div class="piece carrusel-with-copy" data-format="video" data-piece="{piece_num}" onclick="openCopyModal({piece_num}, event)">\n'
        f'        <div class="num">{piece_num}</div>'
    )
    html = html.replace(old_open, new_open)

    # 2. Add copy-data after </details>
    # Find the closing pattern: </details> followed by newline + 6 spaces + </div>
    search_from = html.find(f'data-piece="{piece_num}"')
    if search_from == -1:
        print(f"#{piece_num}: opening NOT FOUND")
        continue

    det_pos = html.find('</details>', search_from)
    if det_pos == -1:
        print(f"#{piece_num}: </details> NOT FOUND")
        continue

    # After </details>, we expect: \n      </div>
    rest = html[det_pos+10:]  # after '</details>'
    # Look for '\n      </div>'
    closing_div_pos = rest.find('\n      </div>')
    if closing_div_pos == -1:
        print(f"#{piece_num}: closing </div> NOT FOUND after details")
        continue

    # Insert copy-data right before the closing </div>
    insert_pos = det_pos + 10 + closing_div_pos  # position of '\n      </div>'

    title_esc = title.replace('\\', '\\\\').replace('"', '\\"')
    copy_data = (
        '\n        <div class="copy-data" style="display:none">'
        '[{"slide":"Video","texto":"' + title_esc + '",'
        '"frase":"Guion pr\u00f3ximamente",'
        '"nota":"Video \u2014 pendiente gui\u00f3n"}]'
        '</div>'
    )

    html = html[:insert_pos] + copy_data + html[insert_pos:]
    print(f"#{piece_num}: OK")

with open('ESTRATEGA/plan_julio2026.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\nDone")
