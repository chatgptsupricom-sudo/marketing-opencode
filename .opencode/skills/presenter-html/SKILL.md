# SKILL: presenter-html — Presentaciones HTML SUPRICOM

Genera documentos HTML profesionales alineados a la marca SUPRICOM a partir de contenido markdown.

## Brand Kit SUPRICOM

| Token | Valor | Uso |
|-------|-------|-----|
| `--primary` | `#1A1A2E` | Fondo de header, footer, tablas, nav |
| `--primary-light` | `#2D2D4A` | Gradientes, hover estados |
| `--accent` | `#CC7A00` | CTAs, bordes, highlights, acentos |
| `--accent-hover` | `#E68A00` | Hover de botones/accent |
| `--success` | `#00CC88` | Cajas de éxito, KPIs positivos |
| `--text` | `#1A1A2E` | Texto principal |
| `--text-light` | `#666` | Texto secundario |
| `--bg` | `#F5F5F8` | Fondo de página |
| `--white` | `#FFFFFF` | Fondos de sección |
| `--border` | `#E0E0E8` | Bordes de tabla y cards |
| Font | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` | Tipografía general |

## Componentes Visuales

Ensambla la página usando estos bloques predefinidos:

### 1. Hero (encabezado principal)
```
.hero — gradiente primary→primary-light, texto blanco centrado
  .hero .badge — badge naranja (accent)
  .hero h1 — título grande con <span> para acento
  .hero .meta — metadatos (fecha, costo, cobertura)
```

### 2. Navegación
```
nav — fixed top, primary bg, 56px height
  .brand — logo/texto con <span> accent
  nav ul li a — links a secciones, .active en scroll
  .menu-toggle — ☰ botón mobile
```

### 3. Secciones
```
section — white card, 12px radius, shadow, 32px padding
  section h2 — 26px, primary, border-bottom accent 3px
  section h3 — 18px, primary
  section h4 — 15px, uppercase, accent
  section p — 333 color, 12px mb
  section ul/ol — 24px left margin
```

### 4. Tablas
```
table — 100%, collapsed, 13px
  th — primary bg, white text, 10px 12px padding
  td — border-bottom, even row #FAFAFC
```

### 5. KPI Grid
```
.kpi-grid — CSS grid, auto-fill minmax(200px, 1fr), 16px gap
  .kpi-card — bg #F5F5F8, 10px radius, centered
    .kpi-card .num — 32px, 800 weight, accent
    .kpi-card .label — 12px, text-light
    .kpi-card .desc — 12px, #888
```

### 6. Highlight Boxes
```
.highlight-box — bg #FFF8F0, border-left 4px accent, 8px radius
.success-box — bg #F0FFF8, border-left 4px success
```

### 7. Role Cards
```
.role-grid — CSS grid, auto-fill minmax(220px, 1fr), 16px gap
  .role-card — white bg, border, 10px radius
    .role-card — border-top 4px accent
    .role-card h4 — título del rol
    .role-card .who — label del rol, 12px, accent
```

### 8. Flow Steps (procesos)
```
.flow-steps — flex column, 0 gap
  .flow-step — flex row, 16px gap, border-bottom
    .step-num — 32px circle, accent bg, white text
    .step-body — flex 1
      .step-body strong — 14px, primary
      .step-body span — 13px, text-light
```

### 9. Comparación (vs box)
```
.vs-grid — CSS grid, 2 cols, 16px gap
  .vs-col — padding 20px, border 1px, radius 10px
    .vs-col h4 — accent, centered, uppercase
```

### 10. Feature List (checklist)
```
.feature-list — list-style none, 8px gap
  .feature-list li — 14px, padding-left 28px
    .feature-list li::before — checkmark icon accent
```

## Workflow

### De markdown a HTML

1. Extraer contenido relevante del .md (secciones, tablas, datos clave)
2. Elegir componentes según el tipo de contenido:
   - Propuesta formal → Hero + Secciones + Tablas + Highlight Boxes
   - Dashboard/reporte → KPI Grid + Tablas + Flow Steps
   - Perfil de lead → Hero + Cards + Comparación
3. Aplicar frameworks de contenido SUPRICOM si aplica (AGES, HAVPC)
4. Verificar reglas de marca (prohibido: "oferta", "revendedor", etc.)
5. Probar responsive (<768px) y hover states

### Estructura de archivo HTML

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SUPRICOM — Título</title>
  <style>
    /* Pegar CSS del template + personalizaciones */
  </style>
</head>
<body>
  <!-- NAV -->
  <!-- HERO (opcional) -->
  <!-- MAIN .main-wrapper > main -->
    <!-- SECTIONs repetir -->
  <!-- FOOTER -->
  <!-- JS (scrollspy) -->
</body>
</html>
```

### Dónde guardar

- HTML publicados en `ESTRATEGA/<nombre>.html`
- GitHub Pages los sirve en `https://chatgptsupricom-sudo.github.io/marketing/ESTRATEGA/<nombre>.html`

## Reglas de Marca (NO NEGOCIABLE)

- Tono consultivo, profesional, español venezolano neutro
- Prohibido: "llévatelo", "aprovecha", "últimas unidades", "rebajón", "oferta", "revendedor"
- Prohibido: precios, stock, datos internos en contenido público
- Permitido: "disponible", "aliado", "comercio", "tu tienda", "portafolio"
- Cierre institucional: `SUPRICOM. Tu mayorista de confianza.`

## Archivos de la skill

| Archivo | Propósito |
|---------|-----------|
| `SKILL.md` | Esta documentación |
| `template.html` | Template HTML base con brand kit y todos los componentes |
| `ejemplo_propuesta.html` | Ejemplo: propuesta formal con hero, secciones, tablas, roles |
| `ejemplo_reporte.html` | Ejemplo: reporte/dashboard con KPI grid, flow steps |

## Carga la skill

```
/skill presenter-html
```

Luego describe el contenido a convertir y la skill generará el HTML.
