# SKILL: layout-copywriter — Copy para diseño de redes sociales SUPRICOM

Genera textos listos para que la diseñadora los monte en imágenes (carrusel, post, Reel) usando Gemini u otras herramientas de diseño.

---

## Workflow del agente

### Paso 1: Investigación web profunda

Antes de escribir UNA SOLA línea de copy, investigá a fondo:

1. **Buscar tendencias, estadísticas y datos recientes** sobre el tema/categoría/producto
2. **Identificar ángulos** que estén funcionando en el mercado venezolano/latinoamericano
3. **Extraer 3-5 datos concretos** (números, fechas, estudios) que den peso al copy
4. **Detectar pain points** actuales del buyer (problemas eléctricos, de conectividad, etc.)
5. **Revisar fuentes** como: Google Trends, artículos de tecnología, foros, redes sociales

> ⚠️ Sin esta investigación no se escribe nada. El copy sin datos pierde autoridad.

### Paso 2: Mapear el contenido

Con la investigación hecha, identificar:

- **Pilar del contenido** (diagnóstico, solución, comparativa, perfil, tendencia, etc.)
- **Formato visual** (carrusel = múltiples slides, post = idea única, Reel = HAVPC)
- **Productos/SKUs** asociados (del catálogo SUPRICOM)
- **Contexto Venezuela** (sí/no — solo si aplica a diagnóstico, visión o tendencia)

### Paso 3: Escribir el copy

Aplicar reglas de marca y estructura según formato.

---

## Reglas de marca SUPRICOM (no negociables)

- **Tono:** consultivo, profesional, español venezolano neutro
- **Prohibido:** "llévatelo", "aprovecha", "últimas unidades", "rebajón", "oferta", "revendedor"
- **Prohibido:** precios, stock, datos internos, números de inventario visibles en público
- **Permitido:** "disponible", "aliado", "comercio", "tu tienda", "portafolio", "tu negocio", "tu cliente"
- **Cierre institucional:** `SUPRICOM. Tu mayorista de confianza.`
- **Supri IA:** boca cerrada, circuitos color #00FF88, cajas selladas

---

## Estructuras por formato

### Carrusel (multi-slide)

```
Slide 1 — Portada
  H1: [Titular potente — 6-8 palabras]
  H2: [Subtítulo — 10-14 palabras]
  CTA visual: "Desliza →"

Slide 2 — Problema / Contexto
  H1: [El dolor/necesidad]
  Body: [2-3 líneas explicativas]
  (Opcional: dato de investigación)

Slide 3 — Solución / Producto
  H1: [Propuesta de valor — nombre del producto]
  Body: [Beneficio clave, no especificaciones técnicas]
  (Opcional: icono o imagen del producto)

Slide 4 — Perfil / Cuándo aplica
  H1: ¿[pregunta de perfil]?
  Body: [A quién le sirve / en qué caso]

Slide 5 — Cierre
  H1: [Conclusión / moraleja]
  Body: [CTA — "Escríbenos al DM" / "Disponible en nuestras sucursales"]
  Marca: SUPRICOM. Tu mayorista de confianza.
```

### Post (idea única)

```
Titular: [1-2 líneas, gancho]
Body: [4-6 líneas, argumento consultivo + dato de investigación]
Cierre: [Llamado a la acción sutil]
Marca: SUPRICOM. Tu mayorista de confianza.
```

### Reel (HAVPC)

```
Hook (0-3s): [Pregunta o afirmación que rompe el scroll]
Agitation (3-8s): [Contexto del problema — conectar con el buyer]
Visualization (8-13s): [Producto en acción — mostrar, no solo decir]
Proof (13-17s): [Dato de investigación o argumento de autoridad]
CTA (17-20s): [WhatsApp en el perfil / DM / sucursales]
Marca: SUPRICOM. Tu mayorista de confianza.
```

---

## Formato de salida para la diseñadora

El output debe ser en markdown limpio, listo para pegarse en Gemini o herramienta de diseño:

```markdown
## [Título del contenido]

### Formato: [Carrusel / Post / Reel]
### Productos/SKUs: [lista]
### Contexto VE: [Sí / No]

---

### SLIDE 1 — Portada
- Texto imagen: "[titular principal]"
- Nota visual: [indicación para la diseñadora]

### SLIDE 2 — ...
```

---

## Archivos de referencia

| Archivo | Propósito |
|---------|-----------|
| `SKILL.md` | Esta documentación |
| `_content/plan_contenido_julio2026.md` | Plan de contenido actual |
| `_content/base_temas_genericos_SUPRICOM.md` | 180 temas base × 23 categorías |
| `_catalogs/` | Catálogos con SKUs reales |
| `_campaigns/bluetti/` | Guías de copy BLUETTI |
