# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the static website for **NEFIN** (Núcleo de Estudos em Finanças e Investimentos / Center for Research in Financial Economics at the University of São Paulo), hosted at `nefin.com.br` via GitHub Pages. The site is based on the **Enlight Bootstrap theme** by ProBootstrap.com and has been heavily customized.

## Build System

The project uses **Gulp** for asset compilation. There is no package-lock.json, so install with:

```bash
npm install
```

Key Gulp tasks:
- `gulp sass` — compile `scss/style.scss` → `css/style.css` and `css/style.min.css`
- `gulp scripts` — bundle vendor JS into `js/scripts.js` and `js/scripts.min.js`
- `gulp merge-styles` — concatenate all vendor CSS into `css/styles-merged.css`
- `gulp default` — run sass + scripts + browser-sync with file watching

> Note: The `browser-sync` task is configured for a local proxy (`localhost/probootstrap/enlight`). For static file serving, edit `gulpfile.js` to use the `server: { baseDir: './' }` option (commented out in the file).

For CSS-only changes, just edit `css/custom.css` directly (no build step needed — it's loaded last and overrides the theme).

## Architecture

### File Structure
- **Root HTML files** — one `.html` per page (no templating engine; pages share nav/footer HTML by copy-paste)
- **`css/`** — compiled CSS; `styles-merged.css` is the vendor bundle, `style.css`/`style.min.css` are compiled from SCSS, `custom.css` is hand-edited site-specific overrides
- **`scss/`** — two files: `style.scss` (theme styles) and `_custom-settings.scss` (variables)
- **`js/main.js`** — site JavaScript (carousel, parallax, back-to-top, mobile detection); `js/custom.js` is for additional custom JS
- **`js/vendor/`** — pre-bundled third-party libraries (jQuery, Bootstrap, Owl Carousel, FlexSlider, PhotoSwipe, Isotope, etc.)
- **`data/`** — financial data files (CSV, XLS) and their corresponding HTML display pages; `data/Portfolios/` holds portfolio-sorted Excel files
- **`resources/`** — downloadable research data organized by category (cost_of_capital, risk_factors, spot_rate_curve, portfolios, volatility_index, etc.) and PDF methodology documents
- **`templates/`** — `graphs.html` and `panel.html` used as layout references when building new data pages
- **`python_general_scripts/`** — Jupyter notebook (`converting_xls_to_csv.ipynb`) for batch-converting XLS data files to CSV using pandas

### CSS Loading Order
1. `css/styles-merged.css` (vendor bundle)
2. `css/style.css` (theme SCSS compiled)
3. `css/custom.css` (site-specific overrides — edit this for visual changes)

### Data Pages Pattern
Pages under `data/` (e.g., `risk_factors.html`, `dividend_yield.html`) follow a consistent layout: navbar shared with the main site, a data table or chart, and download links pointing to files in `data/` or `resources/`. Use `templates/panel.html` or `templates/graphs.html` as the starting point when creating new data pages.

### No Build Required for HTML/CSS Changes
Since pages are plain HTML, edits take effect immediately — just open in a browser. The SCSS build is only needed when modifying `scss/` files; otherwise edit `css/custom.css` directly.

## Data Update Workflow

When updating financial data:
1. Place new XLS/CSV files in `data/` or the appropriate `resources/` subdirectory
2. Run `python_general_scripts/converting_xls_to_csv.ipynb` if converting XLS → CSV (uses pandas; run from the `python_general_scripts/` directory so relative paths resolve correctly)
3. Update the corresponding HTML page's download links and displayed dates
