filepath = '_content/base_temas_genericos_SUPRICOM.md'
with open(filepath, encoding='utf-8') as f:
    content = f.read()

# ---- 1. REMOVE Arquetipo 15 (Interaccion) ----
# Find it between Arq 14 end and Arq 16 start
idx14_end = content.find('\n### ARQUETIPO 15:')
idx16_start = content.find('\n### ARQUETIPO 16:', idx14_end)
if idx14_end >= 0 and idx16_start >= 0:
    content = content[:idx14_end] + content[idx16_start:]
    print('Removed Arq 15')
else:
    print('Arq 15 boundaries not found')
    # Find the boundaries differently
    start = content.find('ARQUETIPO 15:')
    end = content.find('ARQUETIPO 16:', start)
    if start >= 0 and end >= 0:
        # Go back to the ### line
        line_start = content.rfind('\n###', 0, start)
        content = content[:line_start] + content[end-1:]
        print('Removed Arq 15 (alt method)')
    else:
        print('FAILED to find Arq 15')

# ---- 2. RENUMBER Arq 16 -> 15 ----
content = content.replace('ARQUETIPO 16:', 'ARQUETIPO 15:')
# Also renumber topic numbers: 156-160 -> 146-150
for old_n, new_n in [(156, 146), (157, 147), (158, 148), (159, 149), (160, 150)]:
    content = content.replace('| ' + str(old_n) + ' |', '| ' + str(new_n) + ' |')

print('Renumbered Arq 16 -> 15')

# ---- 3. RENUMBER Arq 17, 18, 19, 20 -> 16, 17, 18, 19 (temporarily) ----
for old_arq, new_arq in [(17, 16), (18, 17), (19, 18), (20, 19)]:
    old = 'ARQUETIPO ' + str(old_arq) + ':'
    new = 'ARQUETIPO ' + str(new_arq) + ':'
    content = content.replace(old, new)
    
    # Renumber topics for each arquetipo
    # Arq 16 (was 17): 161-165 -> 151-155
    # Arq 17 (was 18): 166-170 -> 156-160
    # Arq 18 (was 19): 171-175 -> 161-165
    # Arq 19 (was 20): 176-180 -> 166-170
    pass

# Topic renumbering
maps = [
    (161, 151), (162, 152), (163, 153), (164, 154), (165, 155),
    (166, 156), (167, 157), (168, 158), (169, 159), (170, 160),
    (171, 161), (172, 162), (173, 163), (174, 164), (175, 165),
    (176, 166), (177, 167), (178, 168), (179, 169), (180, 170),
]
for old_n, new_n in maps:
    content = content.replace('| ' + str(old_n) + ' |', '| ' + str(new_n) + ' |')

print('Renumbered topics 161-180 -> 151-170')

# ---- 4. REWRITE Arq "LIQUIDACION" -> "OPORTUNIDAD DE STOCK" ----
content = content.replace(
    'ARQUETIPO 16: LIQUIDACIÓN Y OPORTUNIDAD',
    'ARQUETIPO 16: OPORTUNIDAD DE STOCK'
)
content = content.replace(
    '*Fórmula: oportunidad + tiempo limitado + acción*',
    '*Fórmula: disponibilidad + beneficio de comprar ahora*'
)

# Replace the Liquidacion topics with Oportunidad de Stock topics
old_table = """| 151 | Últimas unidades de [producto] — una vez que se acaben, no sabemos cuándo vuelven | Productos con stock bajo | Post + Stories |
| 152 | [Producto] a precio especial esta semana | Cualquier producto | Post |
| 153 | Lote especial de [categoría] con condiciones preferenciales | Categorías | Post + carrusel |
| 154 | Oferta por volumen en [producto]: mientras más llevas, mejor el precio | Productos con margen | Post |
| 155 | Descuento por pronta compra en [categoría] — solo [X] días | Categorías | Post + Stories |"""

new_table = """| 151 | [Producto] con stock disponible hoy — entrega inmediata | Cualquier producto | Post |
| 152 | Repusimos stock de [marca] — vuelve a estar disponible | Marcas con re-stock | Post |
| 153 | [Producto]: disponibilidad confirmada para la semana | Productos con stock estable | Post |
| 154 | Lote disponible de [categoría] — consulta unidades por modelo | Categorías con variedad | Post |
| 155 | Pedido especial de [producto] con entrega programada | Productos a pedido | Post |"""

if old_table in content:
    content = content.replace(old_table, new_table)
    print('Replaced Liquidacion table')
else:
    print('Liquidacion table NOT found, trying alt approach')
    # Find by section header
    idx = content.find('ARQUETIPO 16: OPORTUNIDAD DE STOCK')
    if idx >= 0:
        # Find the table lines after the header
        table_start = content.find('\n| 15', idx)
        table_end = content.find('\n\n###', table_start)
        if table_end < 0:
            table_end = content.find('\n\n---', table_start)
        old = content[table_start:table_end]
        content = content[:table_start] + new_table + content[table_end:]
        print('Replaced table by index')

# ---- 5. ADD new Arq: CONTEXTO VENEZUELA & ECOSISTEMA ----
# Insert after Arq 15 (Contenido Generativo) which ends before the "---" separator
new_arquetipos = """

### ARQUETIPO 16: CONTEXTO VENEZUELA
*Fórmula: situación país + implicación para la tienda + oportunidad*

| # | Título genérico | Aplica a | Formato recomendado |
| 151 | Cómo la [situación eléctrica/coyuntura] afecta la demanda de [categoría] en Venezuela | Categorías sensibles a contexto | Carrusel |
| 152 | Lo que todo dueño de tienda debe saber sobre [tema país] y su impacto en [categoría] | Cualquier categoría | Post |
| 153 | Por qué la [situación país] hace que [categoría] sea prioridad para tu cliente | Categorías críticas | Carrusel |
| 154 | [Mes]: el mes en que [situación país] tradicionalmente afecta a [categoría] | Estacional contexto | Post |
| 155 | ¿Cómo proteger el inventario de tu tienda ante [situación país]? | Gestión | Carrusel |
| 156 | Lo que los comercios venezolanos están haciendo para adaptarse a [situación país] | Resiliencia | Post + carrusel |
| 157 | [Categoría] en Venezuela: lo que cambió en los últimos [X] meses | Evolución mercado | Carrusel |
| 158 | La [situación país] está redefiniendo lo que los clientes finales compran | Cambio demanda | Post |
| 159 | Por qué [categoría] es la respuesta a [problema del país] que tu cliente tiene hoy | Solución coyuntural | Carrusel |
| 160 | El dato de [contexto Venezuela] que todo revendedor debería usar en su argumento de venta | Argumento | Post |

### ARQUETIPO 17: ECOSISTEMA / INTEGRACIÓN DE CATEGORÍAS
*Fórmula: necesidad del cliente final + solución integrada + componentes*

| # | Título genérico | Aplica a | Formato recomendado |
| 161 | Tu cliente no compra un [producto], compra [solución]: el ecosistema completo | Categorías complementarias | Carrusel |
| 162 | Cómo armar una solución completa de [necesidad] con 3 productos de nuestro catálogo | Kits por necesidad | Carrusel |
| 163 | De [producto suelto] a [solución integrada]: el argumento que sube tu ticket | Escalabilidad | Carrusel |
| 164 | Los [X] componentes de un [sistema] que tu cliente necesita y tú puedes venderle | Sistemas | Carrusel 8 slides |
| 165 | [Producto] no funciona solo: lo que tu cliente necesita COMPLEMENTARIO para que [beneficio] | Complementos | Post |
| 166 | La diferencia entre vender un [producto] y vender una [solución]: cómo explicarlo | Mentalidad | Post |
| 167 | El ecosistema [marca]: cómo los productos de una misma marca se potencian entre sí | Marcas con portafolio amplio | Carrusel |
| 168 | 3 necesidades comunes del cliente final que requieren 2+ categorías de nuestro portafolio | Necesidades cruzadas | Carrusel |
| 169 | [Producto A] + [Producto B] + [Producto C]: el triángulo de venta de [sector/vertical] | Vertical específica | Carrusel |
| 170 | Por qué el cliente que compra una [solución completa] no devuelve nada | Retención | Post |

### ARQUETIPO 18: OPORTUNIDAD DE STOCK"""

# Insert before the "--" separator that precedes the Matrix section
separator = '\n---\n\n## MATRIZ DE APLICACIÓN RÁPIDA'
idx_sep = content.find(separator)
if idx_sep >= 0:
    content = content[:idx_sep] + new_arquetipos + content[idx_sep:]
    print('Added new arquetipos before matrix section')
else:
    print('Separator not found!')


# ---- 6. UPDATE the total count ----
content = content.replace(
    '180 temas genéricos × 23 categorías = 4,140 combinaciones',
    '190 temas genéricos × 23 categorías = 4,370 combinaciones'
)

# ---- 7. UPDATE frequency table ----
old_freq_table = """## FRECUENCIA SUGERIDA POR ARQUETIPO (semanal)

| Arquetipo | Posts/semana | Propósito |
|-----------|-------------|-----------|
| Prueba social / \"Lo que se vende\" | 2 | Urgencia + validación |
| Caso de negocio / \"Por qué tenerlo\" | 1 | Conversión |
| Educación / \"Cómo venderlo\" | 2 | Autoridad + utilidad |
| Inteligencia de mercado | 1 | Pensamiento líder |
| Stock y disponibilidad | 1 | Operacional |
| Comparativas | 1 | Decisión |
| Estacional | 1 | Timing |
| Detrás del mayorista | 1 | Confianza |
| Rentabilidad | 1 | ROI |
| Kits y combos | 1 | Ticket promedio |
| Objeciones | 1 | Cierre |
| Interacción | 1 | Comunidad |

**Total semanal aprox:** 14 posts (2/día promedio)"""

new_freq_table = """## FRECUENCIA SUGERIDA POR ARQUETIPO (semanal)

| Arquetipo | Piezas/mes | Propósito |
|-----------|-----------|-----------|
| Prueba social / \"Lo que se vende\" | 3 | Urgencia + validación |
| Caso de negocio / \"Por qué tenerlo\" | 2 | Conversión |
| Educación / \"Cómo venderlo\" | 4 | Autoridad + utilidad (Awareness) |
| Inteligencia de mercado | 2 | Pensamiento líder |
| Stock y disponibilidad | 2 | Operacional |
| Comparativas | 2 | Decisión (Interest) |
| Estacional | 1 | Timing |
| Detrás del mayorista | 1 | Confianza |
| Rentabilidad | 2 | ROI (Education) |
| Kits y combos | 3 | Ticket promedio (Sales) |
| Objeciones | 2 | Cierre |
| Contexto Venezuela | 2 | Relevancia país |
| Ecosistema | 2 | Integración (Sales) |
| Beneficio simple | 2 | Alcance amplio |

**Total mensual aprox:** 30 piezas (alineado con AGES: 30% Awareness · 30% Interest · 25% Education · 15% Sales)"""

if old_freq_table in content:
    content = content.replace(old_freq_table, new_freq_table)
    print('Updated frequency table')
else:
    print('Frequency table NOT found')
    # Try to find it by searching for the section
    idx_freq = content.find('FRECUENCIA SUGERIDA POR ARQUETIPO')
    if idx_freq >= 0:
        idx_plantilla = content.find('PLANTILLA DE ADAPTACIÓN RÁPIDA', idx_freq)
        if idx_plantilla >= 0:
            # Go back to previous blank line
            section_start = content.rfind('\n\n', 0, idx_freq)
            section_end = content.rfind('\n\n', 0, idx_plantilla)
            old_section = content[section_start:section_end]
            new_section = new_freq_table + '\n\n'
            content = content[:section_start] + new_section + content[section_end:]
            print('Replaced frequency section by index')
        else:
            print('Plantilla section not found')

# Save
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done. New length:', len(content))
