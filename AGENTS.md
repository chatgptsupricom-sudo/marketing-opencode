# AGENTS.md — SUPRICOM Marketing

## Repo purpose
Marketing strategy & content hub for **SUPRICOM**, a B2B tech wholesaler in Venezuela. Two GitHub remotes:
- `origin` → `github.com/chatgptsupricom-sudo/marketing` (GitHub Pages: `chatgptsupricom-sudo.github.io/marketing`)
- `new-origin` → `github.com/chatgptsupricom-sudo/marketing-opencode` (Pages: `chatgptsupricom-sudo.github.io/marketing-opencode`)

## Directory structure

| Path | Contents |
|------|----------|
| `ESTRATEGA/` | Strategic analysis, proposals, **HTML deliverables** (published via Pages) |
| `_prospecting/` | Lead lists, prospecting reports, dossiers |
| `_campaigns/bluetti/` | BLUETTI campaign copys, messaging guides |
| `_scripts/` | Python scripts (`md_to_docx.py`, `generar_propuesta_mi_gran_idea.py`) |
| `_catalogs/` | Supplier catalogs (Valencia PDF) |
| `_content/` | Content plans (`.md` + `.docx`), topic bases, proposals |
| `.opencode/skills/` | OpenCode skills (prospector-tiendas, presenter-html, layout-copywriter) |

## Key data sources

| File | What it contains |
|------|------------------|
| `_content/plan_contenido_julio2026.md` | Current content plan (30 pieces, Jul 2026) |
| `_content/base_temas_genericos_SUPRICOM.md` | 180 generic topics × 23 categories = 4,140 combinations |
| `_content/Propuesta_Mi_Gran_Idea_SUPRICOM.docx` | Formal proposal document |
| `_prospecting/dossier_TELTRONICS_2026-07-07.md` | Example lead dossier format |
| `_prospecting/nuevos_leads_*.md` | New leads (generated daily) |
| `_prospecting/reporte_prospeccion_*.md` | Prospecting reports |
| `_campaigns/bluetti/` | BLUETTI brand messaging & copy guide |
| `_catalogs/Catalogo_Completo_SUPRICOM VALENCIA.pdf` | Valencia branch product catalog with SKUs |
| `ESTRATEGA/CONTEXTO_MAESTRO.md` | Complete business context, buyer persona, frameworks |
| `ESTRATEGA/plan_julio2026.html` | Visual calendar HTML (30 pieces, Jul 2026) |

## Portfolio (combined Caracas + Valencia)

- **Protección eléctrica:** FORZA · SMARTBITT · APC · BLUETTI · HAVIT
- **Cámaras + Domótica:** NEXXT HOME · HAVIT · TP-LINK
- **Routers / Redes:** HIKVISION · NEXXT HOME · Linksys · Xiaomi · TP-LINK
- **Laptops:** Acer · ASUS · Dell · HP · Lenovo
- **Mini PC:** MSI
- **Monitores:** AOC · HIKVISION · HP · MSI
- **Almacenamiento:** ADATA · Kingston · WD · Toshiba
- **Periféricos:** Logitech · Havit · Redragon · Targus · Primus · Klipxtreme
- **Impresoras:** Canon · Epson · HP · SAT · Xerox

## Commands

```powershell
# Generate .docx from Python script
python _scripts/generar_propuesta_mi_gran_idea.py
python _scripts/md_to_docx.py

# Git (after PATH refresh)
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
git add -A; if ($?) { git commit -m "msg" }
git push new-origin main

# GitHub CLI
gh repo create <name> --public --push --source=.

# Load skills
/skill presenter-html
/skill layout-copywriter
/skill prospector-tiendas
```

## Content frameworks

### AGES distribution
**30% Awareness** (9) — concepto, visión, tendencia, diagnóstico
**30% Interest** (9) — solución, perfil, alternativa, sinergia
**25% Education** (8) — guía, comparativa, error común, ecosistema
**15% Sales** (4) — showcase, inversión, cierre, vocero

### AGES by week
| Semana | A | I | E | S |
|--------|---|---|---|---|
| S1     | 4 | 3 | 2 | 1 |
| S2     | 3 | 3 | 3 | 1 |
| S3     | 2 | 3 | 3 | 2 |

### HAVPC for Reels (vocero & voz en off)
**Hook** (0-3s) → **Agitation** (3-8s) → **Visualization** (8-13s) → **Proof** (13-17s) → **CTA** (17-20s)

### Content structure rules
- **Each day = two opposite pillars** (never repeat pillar in same day)
- **No Saturdays** — lun–vie only
- **Venezuela context: max 1 piece/day, never two consecutive days** (~20% = 6/30)
- **100% consultivo** — no interactive posts, no surveys, no "cuéntanos"
- **Format:** carrusel for multi-slide, post for single idea

## Brand rules (non-negotiable)

- **Tono:** consultivo, profesional, español venezolano neutro
- **Prohibido:** "llévatelo", "aprovecha", "últimas unidades", "rebajón", "oferta", "revendedor"
- **Prohibido:** precios, stock, datos internos, números de inventario visibles en público
- **Permitido:** "disponible", "aliado", "comercio", "tu tienda", "portafolio", "tu negocio", "tu cliente"
- **Cierre institucional:** `SUPRICOM. Tu mayorista de confianza.`
- **Supri IA:** boca cerrada, circuitos color #00FF88, cajas selladas
- **BLUETTI disponible en ambas sucursales** (Caracas + Valencia)

## Brand kit (HTML)

| Token | Value | Use |
|-------|-------|-----|
| `--primary` | `#0056DB` | Header, footer, nav, tables |
| `--primary-light` | `#0791F4` | CTAs, borders, highlights, accent text |
| `--bg` | `#F3F3F3` | Page background |
| `--gradient-hero` | `linear-gradient(135deg, #015CDE 0%, #068AF1 100%)` | Hero gradient |
| `--success` | `#00CC88` | Positive KPIs |
| `--text` | `#1A1A2E` | Main text |
| Font | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto` | -- |

## Lead scoring

| Level | Criteria |
|-------|----------|
| **ALTO** | Tienda física + redes activas, +1000 seguidores, NO vende protección eléctrica |
| **MEDIO** | Solo online o solo física, 500-1000 seguidores |
| **BAJO** | <500 seguidores, sin tienda física, sin web |

## Venezuela context dosage

- S1: lun (#2 diagnóstico) + vie (#9 tendencia)
- S2: mar (#14 solución ecosistema)
- S3: mar (#23 visión) + mié (#28 error)
- Never two consecutive days. Max 1 piece/day.
- Only in diagnosis, vision, or trend pillars (never in showcases, comparisons, or investment)
