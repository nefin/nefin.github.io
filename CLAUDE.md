# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the static website for **NEFIN** (Núcleo de Estudos em Finanças e Investimentos / Center for Research in Financial Economics at the University of São Paulo), hosted at `nefin.com.br` via GitHub Pages. The site is built with **Hugo** and managed via **Decap CMS**.

## Build System

The project uses **Hugo** as the static site generator. No npm/Gulp build step is needed.

```bash
# Local development server (live reload)
hugo server

# Production build
hugo --minify
# Output goes to public/
```

Deployment is handled automatically by GitHub Actions (`.github/workflows/hugo.yml`) on every push to `main`. The CMS admin panel is hosted separately on Netlify (`netlify.toml`) for authentication only.

## Architecture

### File Structure
- **`content/`** — Markdown source files organized by section:
  - `_index.md` — homepage content
  - `datasets/` — one `.md` per dataset (risk factors, cost of equity, etc.)
  - `people/` — faculty, researchers, students, alumni
  - `research/` — papers and working papers
- **`layouts/`** — Hugo HTML templates:
  - `index.html` — homepage template
  - `_default/` — fallback layouts
  - `datasets/`, `people/`, `research/` — section-specific templates
  - `partials/` — reusable components (`head.html`, `nav.html`, `footer.html`)
- **`static/`** — assets copied verbatim to `public/` during build:
  - `css/main.css` — all site CSS (edit directly, no build step)
  - `img/` — images
  - `resources/` — downloadable data files (CSV, XLS, PDF), organized by category (`risk_factors/`, `cost_of_capital/`, `spot_rate_curve/`, `portfolios/`, `volatility_index/`, `methodology/`, `report/`)
  - `admin/` — Decap CMS configuration (`config.yml`)
- **`hugo.toml`** — Hugo site configuration (base URL, permalink structure, params)
- **`netlify.toml`** — Netlify build settings (used only for CMS auth, not for hosting)
- **`python_general_scripts/`** — Jupyter notebook for batch-converting XLS → CSV using pandas
- **`DEPRECATED/`** — archived Bootstrap/Gulp site (kept for reference, not used by Hugo)

### URL Structure
Dataset content pages are published at `/data/:slug/` (configured in `hugo.toml` permalinks). This is the URL path of the generated HTML pages — it has no relation to any `data/` directory in the repo. Download links inside those pages point to `/resources/...`.

### CSS
Edit `static/css/main.css` directly — no compilation needed. Changes take effect immediately on `hugo server`.

### Adding a New Dataset Page
1. Create `content/datasets/my-dataset.md` following the frontmatter pattern of existing dataset files (title, description, url, downloads list, table data)
2. The `layouts/datasets/` templates handle rendering automatically

## Data Update Workflow

When updating financial data files:
1. Place new XLS/CSV files in the appropriate `static/resources/` subdirectory
2. Run `python_general_scripts/converting_xls_to_csv.ipynb` if converting XLS → CSV (run from the `python_general_scripts/` directory so relative paths resolve correctly)
3. Update the corresponding `content/datasets/*.md` file: adjust displayed dates, table data, and download URLs if filenames changed
