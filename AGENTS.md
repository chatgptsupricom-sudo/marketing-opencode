# AGENTS.md — SUPRICOM Marketing

## Repo purpose
Marketing strategy & content hub for SUPRICOM, a B2B tech wholesaler in Venezuela. Contains:
- Content plans (`plan_contenido_julio2026.md`)
- Lead lists (`nuevos_leads_*.md`, `reporte_prospeccion_*.md`)
- Strategic analysis (`ESTRATEGA/`)
- Brand assets, catalogs, product copys

## Key directories
| Path | Purpose |
|------|---------|
| `ESTRATEGA/` | Strategic analysis, proposals, master context, HTML deliverables |
| `.opencode/skills/prospector-tiendas/` | OpenCode skill for Venezuelan tech store prospecting |
| `.opencode/skills/presenter-html/` | OpenCode skill for HTML presentations with SUPRICOM brand kit |

## Architecture
- **No build system**, no package.json — pure markdown + Python scripts
- Python scripts (`md_to_docx.py`, `generar_propuesta_mi_gran_idea.py`) generate `.docx` from Python using `python-docx` (v1.2.0)
- Git repo at `github.com/chatgptsupricom-sudo/marketing` with GitHub Pages enabled
- HTML deliverables go live at `https://chatgptsupricom-sudo.github.io/marketing/ESTRATEGA/<file>.html`

## Commands
```powershell
# Generate .docx from Python script
python generar_propuesta_mi_gran_idea.py
python md_to_docx.py

# Git (after PATH refresh — close & reopen terminal)
git add -A && git commit -m "msg"
git push

# GitHub CLI (after `gh auth login`)
gh repo create <name> --public --push --source=.

# Load a skill via slash command
/skill presenter-html
/skill prospector-tiendas
```

## Framework conventions (content strategy)
- **AGES**: 30% Awareness, 30% Interest, 25% Education, 15% Sales
- **HAVPC**: Hook → Agitation → Visualization → Proof → CTA (video)
- **Swipe to Learn**: title → problem → solution → data → CTA (carrusel)
- Brand tone: consultivo, profesional. **Prohibited words**: "oferta", "revendedor", "aprovecha", "últimas unidades", "llévatelo", "rebajón"
- **Permitted**: "disponible", "aliado", "comercio", "tu tienda", "portafolio"
- Cierre institucional: `SUPRICOM. Tu mayorista de confianza.`

## Environment quirks
- `git` and `gh` installed via `winget` — **must refresh PATH** in each new terminal session before use: `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')`
- PowerShell 5.1 — no `&&`, no heredoc `<<`. Use `; if ($?) { }` for chaining.
- File paths with spaces **must** be quoted for PowerShell cmdlets

## Key data sources (read these first)
| File | What it contains |
|------|------------------|
| `ESTRATEGA/CONTEXTO_MAESTRO.md` | Complete business context, buyer persona, frameworks |
| `plan_contenido_julio2026.md` | Current content plan (36 pieces, Jul 2026) |
| `base_temas_genericos_SUPRICOM.md` | 180 generic topics × 23 categories = 4,140 combinations |
| `dossier_TELTRONICS_2026-07-07.md` | Example lead dossier format |
| `.opencode/skills/prospector-tiendas/SKILL.md` | Prospecting methodology & lead scoring |
| `.opencode/skills/presenter-html/SKILL.md` | HTML presentation framework with brand kit & components |

## Lead scoring
- **ALTO**: física + redes activas, +1000 seguidores, NO vende protección eléctrica
- **MEDIO**: solo online o solo física, 500-1000 seguidores
- **BAJO**: <500 seguidores, sin tienda física, sin web

## Prohibited content rules
- No precios, stock, datos internos visibles en contenido público
- No mencionar "revendedor" — usar "aliado", "comercio", "tu tienda"
- No lenguaje minorista ("aprovecha", "últimas unidades")
