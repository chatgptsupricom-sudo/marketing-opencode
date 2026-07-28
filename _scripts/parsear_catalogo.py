#!/usr/bin/env python3
"""
Parsea el catálogo SUPRICOM y genera un objeto JavaScript
con los datos de inventario para el visor en HTML.
"""
import re
import json

def parsear_catalogo(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()

    lineas = contenido.split('\n')
    
    catalogo = {
        'CARACAS': {},
        'VALENCIA': {}
    }
    
    sede_actual = None
    categoria_actual = None
    en_bluetti = False
    en_bluetti_reg = False
    bluetti_productos = []
    
    for linea in lineas:
        linea = linea.strip()
        
        # Detectar sección BLUETTI
        if '## BLUETTI' in linea:
            en_bluetti = True
            sede_actual = None
            categoria_actual = None
            continue
        
        # Detectar sede (must start with ## to avoid false matches in BLUETTI description)
        if linea.startswith('## SUPRICOM CARACAS'):
            sede_actual = 'CARACAS'
            en_bluetti = False
            en_bluetti_reg = True
            continue
        elif linea.startswith('## SUPRICOM VALENCIA'):
            sede_actual = 'VALENCIA'
            en_bluetti = False
            en_bluetti_reg = True
            continue
        
        # Detectar categoría (### NOMBRE)
        if linea.startswith('### '):
            if en_bluetti:
                continue  # Ignorar subcategorías de BLUETTI
            if sede_actual:
                categoria_actual = linea[4:].strip()
                if categoria_actual not in catalogo[sede_actual]:
                    catalogo[sede_actual][categoria_actual] = []
            continue
        
        # Detectar líneas de datos de la tabla BLUETTI (3 columnas: Código, Descripción, Precio)
        if linea.startswith('|') and en_bluetti and not en_bluetti_reg:
            # Remove escaped pipes first, then split
            clean = linea.replace('\\|', ' ')
            partes = [p.strip() for p in clean.split('|')]
            if len(partes) >= 4:  # | empty | código | descripción | precio | empty |
                ref = partes[1]
                desc = partes[2]
                precio_str = partes[3]
                
                # Saltar cabeceras y separadores
                if ref == 'Código' or ref.startswith('---') or not ref:
                    continue
                
                # Limpiar precio
                precio_str = precio_str.replace('$', '').replace(',', '').strip()
                try:
                    precio = float(precio_str)
                except:
                    continue
                
                producto = {
                    'sku': ref,
                    'nombre': desc,
                    'marca': 'BLUETTI',
                    'cantidad': 0,  # BLUETTI no tiene cantidad en el catálogo
                    'precio': precio
                }
                
                bluetti_productos.append(producto)
        
        # Detectar líneas de datos de la tabla regular (5 columnas)
        if linea.startswith('|') and sede_actual and categoria_actual:
            partes = [p.strip() for p in linea.split('|')]
            if len(partes) >= 6:  # | ref | nombre | marca | cantidad | precio |
                ref = partes[1]
                nombre = partes[2]
                marca = partes[3]
                cantidad_str = partes[4]
                precio_str = partes[5]
                
                # Saltar cabeceras y separadores
                if ref == 'Referencia' or ref.startswith('---') or not ref:
                    continue
                
                try:
                    cantidad = int(cantidad_str)
                except:
                    continue
                
                try:
                    precio = float(precio_str)
                except:
                    continue
                
                producto = {
                    'sku': ref,
                    'nombre': nombre,
                    'marca': marca,
                    'cantidad': cantidad,
                    'precio': precio
                }
                
                catalogo[sede_actual][categoria_actual].append(producto)
    
    # Agregar productos BLUETTI a ambas sedes bajo "UPS Y REGULADORES"
    for sede in ['CARACAS', 'VALENCIA']:
        if 'UPS Y REGULADORES' not in catalogo[sede]:
            catalogo[sede]['UPS Y REGULADORES'] = []
        catalogo[sede]['UPS Y REGULADORES'].extend(bluetti_productos)
    
    return catalogo

def generar_js(catalogo):
    """Genera el código JavaScript con los datos del catálogo"""
    # Calcular inventario general (sumar ambas sedes)
    general = {}
    for sede in ['CARACAS', 'VALENCIA']:
        for cat, productos in catalogo[sede].items():
            if cat not in general:
                general[cat] = {}
            for p in productos:
                key = p['sku']
                if key in general[cat]:
                    general[cat][key]['cantidad'] += p['cantidad']
                else:
                    general[cat][key] = {
                        'sku': p['sku'],
                        'nombre': p['nombre'],
                        'marca': p['marca'],
                        'cantidad': p['cantidad'],
                        'precio': p['precio']
                    }
    
    # Convertir a listas
    general_lista = {}
    for cat, items in general.items():
        general_lista[cat] = list(items.values())
    
    js = f"const CATALOGO = {json.dumps({'GENERAL': general_lista, 'CARACAS': catalogo['CARACAS'], 'VALENCIA': catalogo['VALENCIA']}, ensure_ascii=False, indent=2)};"
    return js

if __name__ == '__main__':
    ruta = '_catalogs/CATALOGO_SUPRICOM_13-07.md'
    catalogo = parsear_catalogo(ruta)
    
    # Imprimir estadísticas
    for sede in ['CARACAS', 'VALENCIA']:
        total = sum(len(p) for p in catalogo[sede].values())
        cats = list(catalogo[sede].keys())
        print(f"{sede}: {total} productos en {len(cats)} categorías")
        for cat in cats:
            print(f"  {cat}: {len(catalogo[sede][cat])} productos")
    
    # Generar JS
    js = generar_js(catalogo)
    
    # Guardar
    with open('_scripts/catalogo_data.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print(f"\nArchivo generado: _scripts/catalogo_data.js")
    print(f"Tamaño: {len(js)} caracteres")
