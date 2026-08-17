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
  - `people/` — faculty, researchers, students, alumni. `_index.md` cascades `build.render: never` to the individual person pages: people are rendered inside the section lists, never as standalone pages
  - `research/` — papers, working papers and books. Same `render: never` cascade
  - `insights/` — guest essays on finance research by invited (non-NEFIN) researchers, published at `/insights/<filename>/`
- **`layouts/`** — Hugo HTML templates:
  - `index.html` — homepage template
  - `_default/` — fallback layouts
  - `datasets/`, `people/`, `research/` — section-specific templates. `people/list.html` serves every People section (it renders a hub when the section has children, a card grid otherwise); `people/alumni/list.html` overrides it with a table
  - `404.html` — not-found page
  - `partials/` — reusable components. Notable ones:
    - `person-card.html`, `dataset-card.html`, `insight-card.html` — the single source of truth for each card, used by both the homepage and the section lists
    - `dataset-freshness.html` — returns `{state, label, months}` for a dataset, derived from `last_observation`. Every freshness badge and warning on the site comes from here
    - `insight-author.html` — resolves a post's author details (front matter, falling back to a matching People page)
    - `research-tabs.html` — the Published / Working / Books tab strip
- **`static/`** — assets copied verbatim to `public/` during build:
  - `css/main.css` — all site CSS (edit directly, no build step)
  - `img/` — images
  - `js/chart.umd.min.js` — Chart.js v4.4.4, self-hosted (no CDN)
  - `favicon.svg`
  - `resources/` — downloadable data files (CSV, XLS, PDF), organized by category (`risk_factors/`, `cost_of_capital/`, `spot_rate_curve/`, `portfolios/`, `volatility_index/`, `methodology/`, `report/`)
  - `admin/` — Decap CMS configuration (`config.yml`)
- **`hugo.toml`** — Hugo site configuration (base URL, permalink structure, params)
- **`netlify.toml`** — Netlify build settings (used only for CMS auth, not for hosting)
- **`python_general_scripts/`**
  - `converting_xls_to_csv.ipynb` — batch XLS → CSV with pandas
  - `update_dataset_dates.py` — rewrites `coverage_start` / `last_observation` in `content/datasets/*.md` from the data files themselves. CI runs it with `--check` and fails the build on drift
- **`DEPRECATED/`** — archived Bootstrap/Gulp site (kept for reference, not used by Hugo)

### URL Structure
Dataset pages are published at `/data/<filename>/` and Insights posts at `/insights/<filename>/`, via the `:slugorcontentbasename` permalink token in `hugo.toml`. **The filename drives the URL** — an explicit `slug:` in the front matter overrides it. (This used to be plain `:slug`, which fell back to the *title*, so retitling a page silently broke its URL.) `/data/` is a URL path only; it has no relation to any `data/` directory in the repo. Download links inside those pages point to `/resources/...`.

### Cross-cutting conventions
- **Never query pages by `Type`.** `content/research/papers/x.md` has `.Type == "research"`, not `"papers"`, so `where site.RegularPages "Type" "papers"` silently returns nothing for anything the CMS creates. Use `site.GetPage "/research/papers"` and range over `.Pages`.
- **`--accent` (`#C8963E`) is decorative only** — 2.66:1 on white, below WCAG AA. Use `--accent-text` for gold text on light backgrounds and `--accent-ink` for text on a gold fill.
- Inside `{{ range }}`, `$` is the *list* page, not the item. Use `.Title`, or bind a variable, when setting `alt` and similar per-item attributes.

### CSS
Edit `static/css/main.css` directly — no compilation needed. Changes take effect immediately on `hugo server`.

### Adding a New Dataset Page
1. Create `content/datasets/my-dataset.md` following the front matter pattern of the existing files: `title`, `summary` (card text), `description` (page intro), `downloads` (list of `{label, url}`), optionally `table` / `table_caption` and `dashboard`
2. Freshness fields — these drive the badge and the warning banner, so they describe **the data**, not the edit:
   - `last_observation` / `coverage_start` — ISO dates; run `update_dataset_dates.py` rather than typing them
   - `frequency` — `Daily` | `Weekly` | `Monthly` | `Quarterly`
   - `no_data: true` — when only the methodology exists; the page then says so explicitly
   A dataset within its update cycle shows "Updated <month>"; beyond it, "Last observation <month>" plus a visible warning. There is no free-text "updated" field any more — it was how pages ended up claiming "Updated Monthly" while the data sat three years old
3. The `layouts/datasets/` templates handle rendering automatically, including the Python/R access snippet and the "How to cite" block

### Adding a New Insights Post
1. Duplicate `content/insights/modelo-de-post.md` (a `draft: true` template, never published) and rename it — the filename becomes the URL slug. Its front matter is deliberately all placeholders and its body is AI-written filler: never publish it, and never attribute a demo body to a real person
2. Frontmatter: `title`, `date`, `language` (`pt` or `en` — drives the language badge and date format; note the key is `language`, since Hugo removed `lang`), `author`, `summary`, `topics` (list)
3. Posts are written by **invited guest researchers**, not NEFIN members. Their details live in the post's own front matter: `author_affiliation`, `author_url`, `author_photo` (upload to `static/img/uploads/`), `author_bio` (renders the "About the author" box). Every post automatically carries a guest-contribution disclaimer
4. If `author` happens to match a name in `content/people/**`, that person's photo, role and personal URL fill in whichever `author_*` fields were left blank
5. `topics` feed the `topic` taxonomy at `/topics/:term/`; the section also emits RSS at `/insights/index.xml`
6. Researchers can do all of this through Decap CMS ("Insights" collection)
7. Share buttons (`layouts/partials/share.html`) are plain links — no third-party widgets. Preview cards come from the Open Graph tags in `head.html`; set `image` in the front matter (1200×630) or the author photo is used as fallback

## Data Update Workflow

When updating financial data files:
1. Place new XLS/CSV files in the appropriate `static/resources/` subdirectory
2. Run `python_general_scripts/converting_xls_to_csv.ipynb` if converting XLS → CSV (run from the `python_general_scripts/` directory so relative paths resolve correctly)
3. Run `python3 python_general_scripts/update_dataset_dates.py` from the repo root — it rewrites `coverage_start` and `last_observation` from the files you just added. If you add a new dataset, register its file and date format in that script's `SOURCES` map
4. Update the corresponding `content/datasets/*.md` by hand only for things the script cannot know: `table` / `table_caption` (the summary statistics) and `downloads` URLs if filenames changed
5. CI runs `update_dataset_dates.py --check` and fails the build if any page disagrees with its data file
