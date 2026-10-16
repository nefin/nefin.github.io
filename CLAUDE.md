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

**Hugo version:** CI and `netlify.toml` both pin **0.164.0 extended**. A newer local Hugo usually works, but if a build passes locally and fails in CI, check the version first; bump both files together.

### Before pushing
Every push to `main` deploys straight to production, so run what CI runs:
```bash
python3 python_general_scripts/update_dataset_dates.py --check   # needs pandas + xlrd
hugo --minify                                                     # must finish with no ERROR lines
```
Changes made through the CMS are committed to `main` directly by Decap, so `git pull` before starting work.

## Architecture

### File Structure
- **`content/`** — Markdown source files organized by section:
  - `_index.md` — homepage content
  - `datasets/` — one `.md` per dataset: nine pages in all. Eight have data files under `static/nefindata/`; `illiquidity-index` is `no_data: true` (methodology only), so it has no data folder and is not in `update_dataset_dates.py`. Of the eight with data, only `risk-factors` and `short-interest` are maintained; the other six are `discontinued: true`
  - `people/` — faculty, researchers, students, alumni. `_index.md` cascades `build.render: never` to the individual person pages: people are rendered inside the section lists, never as standalone pages
  - `research/` — papers, working papers and books. Same `render: never` cascade
  - `insights/` — two kinds of writing, published at `/insights/<filename>/`: guest essays by invited (non-NEFIN) researchers about their own work, and didactic/informative pieces (tutorials, explainers) written by the NEFIN team itself
- **`layouts/`** — Hugo HTML templates:
  - `index.html` — homepage template
  - `_default/` — fallback layouts. `baseof.html` is the page shell (it loads KaTeX only when the page sets `math: true`); `taxonomy.html` / `terms.html` render `/topics/` and `/topics/<term>/`
  - `insights/` — `list.html` (the post index) and `single.html` (a post, including the EN/PT language switch for `bilingual: true` posts)
  - `shortcodes/` — usable inside markdown bodies:
    - `{{% lang-en %}}…{{% /lang-en %}}` / `{{% lang-pt %}}…{{% /lang-pt %}}` — the two halves of a bilingual post (see **Adding a New Insights Post**)
    - `{{< math >}}…{{< /math >}}` (inline) and `{{< math display="true" >}}…{{< /math >}}` (block) — raw LaTeX rendered by KaTeX. Requires `math: true` in front matter. Use the shortcode, not bare `$…$`: goldmark would eat the backslashes and underscores
  - `datasets/`, `people/`, `research/` — section-specific templates. `people/list.html` serves every People section (it renders a hub when the section has children, a card grid otherwise); `people/alumni/list.html` overrides it with a table
  - `404.html` — not-found page
  - `partials/` — reusable components. Notable ones:
    - `person-card.html`, `dataset-card.html`, `insight-card.html` — the single source of truth for each card, used by both the homepage and the section lists
    - `dataset-freshness.html` — returns `{state, label, months}` for a dataset, derived from `last_observation`. Every freshness badge and warning on the site comes from here
    - `insight-author.html` — resolves a post's author details (front matter, falling back to a matching People page)
    - `research-tabs.html` — the Published / Working / Books tab strip
- **`static/`** — assets copied verbatim to `public/` during build:
  - `css/main.css` — all site CSS (edit directly, no build step)
  - `img/` — images, one subfolder per use: `faculty/`, `researchers/`, `students/` (people photos, referenced by `photo:`; the folder reflects where the photo was first added, not the person's current section — several researchers' photos live in `faculty/`), `books/` (covers), `insights/` (post figures and OG images, prefixed with the post's slug, e.g. `troca-de-gestor-sharpe-en.png`), `logos/`. `uploads/` is where Decap CMS puts anything uploaded through the panel; it's created on first upload. Every image here is referenced by some page, **except** a few kept on purpose as brand/high-res assets: the `logos/` variants not used by the templates (`logo.png`, `logo_horizontal_*`, `Logo-FEA.jpg`, `Logo-USP.png`, `Logo-FIPE.jpg`) and the `books/*_full.jpg` + `analise_de_investimento.jpg` covers. Don't delete those as orphans. Unused photos, banners and news images from the old site were removed in 2026-10 and remain in git history (tag `site-antigo-bootstrap`)
  - `js/chart.umd.min.js` — Chart.js v4.4.4, self-hosted (no CDN)
  - `vendor/katex/` — KaTeX, self-hosted for the same reason; loaded only on `math: true` pages
  - `favicon.svg`
  - `nefindata/` — downloadable data files (CSV, XLS, PDF), one subfolder per dataset, named after that dataset's slug (`risk-factors/`, `cost-of-equity/`, `spot-rate-curve/`, `portfolios/`, `volatility-index/`, `dividend-yield/`, `loan-fees/`, `short-interest/`), plus a shared `methodology/` folder for `nefin_methodology.pdf`. See **Data file URLs** below and `static/nefindata/README.md` (published at `/nefindata/README.md`) for the full naming policy and file table — written for the Python data-loading library too, not just site maintainers
  - `admin/` — Decap CMS configuration (`config.yml`)
- **`hugo.toml`** — Hugo site configuration (base URL, permalink structure, params)
- **`netlify.toml`** — Netlify build settings (used only for CMS auth, not for hosting)
- **`python_general_scripts/`**
  - `converting_xls_to_csv.ipynb` — batch XLS → CSV with pandas
  - `update_dataset_dates.py` — rewrites `coverage_start` / `last_observation` in `content/datasets/*.md` from the data files themselves. CI runs it with `--check` and fails the build on drift
- **`docs/`** — reference material for maintainers, not published:
  - `VISUAL_IDENTITY.md` — design reference (palette, typography, logo use; old site vs. redesign). Read it before changing colors or fonts in `main.css`
  - `NEFIN_content.md` — content inventory scraped from the *old* site as input for the redesign. Historical; don't treat it as the current state of the site
- Not in git, never commit: `public/` (build output), `resources/` (Hugo's image cache), `.hugo_build.lock`, and the per-machine agent config `.mcp.json`, `settings.json` and `.claude/settings.local.json`, which hold local MCP tokens

### URL Structure
Dataset pages are published at `/data/<filename>/` and Insights posts at `/insights/<filename>/`, via the `:slugorcontentbasename` permalink token in `hugo.toml`. **The filename drives the URL** — an explicit `slug:` in the front matter overrides it. (This used to be plain `:slug`, which fell back to the *title*, so retitling a page silently broke its URL.) `/data/` is a URL path only; it has no relation to any `data/` directory in the repo.

### Data file URLs
Every downloadable data file lives at a fixed URL: **`nefin.com.br/nefindata/{datafolder}/{filename}.{filenametype}`**. `{datafolder}` is always the dataset's own slug (the same string as its `content/datasets/*.md` filename and its `/data/{slug}/` page), so the data folder for `content/datasets/cost-of-equity.md` is `static/nefindata/cost-of-equity/`. This is the one place the site deviates from "the filename drives the URL" for pages — here the *directory* is the fixed, citable part, since these links get pasted into papers, notebooks and — now — a Python data-loading library, not just read by a human. Consequences:
- `{datafolder}` is kebab-case (matches the URL slug); `{filename}` is lowercase snake_case, never containing a hyphen or a space — this split lets a parser separate the two unambiguously, and a space would force URL-encoding in every downstream script. `NEFIN_methodology.pdf` → `nefin_methodology.pdf` and `IVol-BR.csv` → `ivol_br.csv` are past mistakes fixed under this rule (2026-09) — don't reintroduce mixed case or in-filename hyphens
- `nefin_methodology.pdf` is the one file shared by every dataset page; it lives in `static/nefindata/methodology/`, not inside any single dataset's folder
- Moving or renaming a file under `static/nefindata/` breaks that fixed URL for anyone who already saved it — treat it as a public API, not an implementation detail. Update the corresponding `downloads[].url` (and `dashboard_csv` for risk-factors) in the dataset's front matter in the same change
- `python_general_scripts/update_dataset_dates.py`'s `SOURCES` map reads straight from `static/nefindata/...` — keep it in sync with any path change
- Full naming policy + current file table: `static/nefindata/README.md`

### Homepage dataset teaser
`layouts/index.html` shows **only the series NEFIN still produces** — every dataset whose front matter has neither `discontinued` nor `no_data` — followed by a dashed "All datasets" card linking to the full catalog. The list is derived, not hand-kept: retiring a series with `discontinued: true` removes it from the homepage automatically, and clearing the flag brings it back. As of 2026-09 only `risk-factors` and `short-interest` are live; six are `discontinued` archives and `illiquidity-index` is `no_data`. Don't reintroduce a hardcoded `slice` of `site.GetPage` calls here, and don't filter with `where`, which silently drops pages that simply lack the key.

### Legacy URLs
The pre-2026 Bootstrap site (removed from the tree in 2026-10; browse it with `git show site-antigo-bootstrap:DEPRECATED/<file>` or `git checkout site-antigo-bootstrap -- DEPRECATED`) used a different URL scheme, and its addresses are cited in papers and syllabi. GitHub Pages has **no server-side redirects**, so each old address is kept alive by an `aliases` entry in the front matter of the page that replaced it — Hugo publishes a `<meta http-equiv=refresh>` + `rel=canonical` stub at that path. Sixteen are mapped: the nine `/data/<name>.html` dataset pages, `/faculty.html`, `/researchers.html`, `/students.html`, `/alumni.html`, and `/research/{papers,working_papers,books}.html`.

Aliases are append-only — deleting one silently 404s a citation. Verify against **production**, not a local build: `curl -sI https://nefin.com.br/data/risk_factors.html`.

Still unmapped, because the new site has no equivalent: `/reports/funds.html`, `/reports/weekly_reports.html`, and the old resource paths `/resources/NEFIN_methodology.pdf` and `/resources/latest_report_nefin.pdf`. A `.pdf` path cannot be aliased — a redirect stub there would be served as `application/pdf` and break — so restoring those means copying the file back to the old path.

### Verifying links
`hugo --minify` (what CI runs) **strips attribute quotes**, so production HTML has `href=/data/` and a `href="([^"]+)"` regex silently matches nothing. Any link checker must accept quoted, single-quoted and bare attribute values, and should run against `hugo --minify` output or the live site — not a plain `hugo` build.

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
   - `discontinued: true` — when the series was **retired on purpose**, not merely left un-updated. The page then reads as a historical archive (neutral grey badge "Discontinued — ends <month>") instead of the red "not updated in N years" warning. Pair it with `successor_url` / `successor_label` when a maintained series replaced it, so the notice links there. This is never inferred from the dates: only a human knows the difference between a finished series and a neglected one
   A dataset within its update cycle shows "Updated <month>"; beyond it, "Last observation <month>" plus a visible warning. There is no free-text "updated" field any more — it was how pages ended up claiming "Updated Monthly" while the data sat three years old
3. The `layouts/datasets/` templates handle rendering automatically, including the Python/R access snippet and the "How to cite" block
4. The markdown **body** of a dataset page renders directly under the description (above any table or dashboard). Use it for caveats and cross-links — `description` is escaped, so a link only works in the body. `loan-fees.md` / `short-interest.md` use it to keep the two loan fee series (weekly, discontinued 2023 vs. daily, maintained) from being mistaken for each other

### Adding a New Insights Post
1. Duplicate `content/insights/modelo-de-post.md` (a `draft: true` template, never published) and rename it — the filename becomes the URL slug. Its front matter is deliberately all placeholders and its body is AI-written filler: never publish it, and never attribute a demo body to a real person
2. Frontmatter: `title`, `date`, `language` (`pt` or `en` — drives the language badge and date format; note the key is `language`, since Hugo removed `lang`), `author`, `summary`, `topics` (list)
   - **Bilingual post** (one file, EN/PT toggle on the page; `troca-de-gestor.md` is the reference): set `bilingual: true`, give every visible front-matter field a `_pt` twin (`title_pt`, `summary_pt`, `author_bio_pt`, …), and wrap the body in `{{% lang-en %}}…{{% /lang-en %}}` followed by `{{% lang-pt %}}…{{% /lang-pt %}}`. English is the default view. Language-specific figures get `-en` / `-pt` suffixes
   - **Equations**: add `math: true` and use the `math` shortcode (see `layouts/shortcodes/`)
3. Most posts are written by **invited guest researchers**, not NEFIN members — their details live in the post's own front matter: `author_affiliation`, `author_url`, `author_photo` (upload to `static/img/uploads/`), `author_bio` (renders the "About the author" box; may contain a plain `<a>` link — it's rendered with `safeHTML`). Every post currently carries the same guest-contribution disclaimer regardless of who wrote it — there's no `guest: false` switch yet for the NEFIN-authored didactic posts the section now also covers (see `content/insights/_index.md`), so a NEFIN team member publishing one still appears under "Guest essay by / Texto convidado por"
4. If `author` happens to match a name in `content/people/**`, that person's photo, role and personal URL fill in whichever `author_*` fields were left blank
5. `topics` feed the `topic` taxonomy at `/topics/:term/`; the section also emits RSS at `/insights/index.xml`
6. Researchers can do all of this through Decap CMS ("Insights" collection)
7. Share buttons (`layouts/partials/share.html`) are plain links — no third-party widgets. Preview cards come from the Open Graph tags in `head.html`; set `image` in the front matter (1200×630) or the author photo is used as fallback

## Data Update Workflow

When updating financial data files:
1. Place new XLS/CSV files in the appropriate `static/nefindata/<dataset-slug>/` subdirectory (see **Data file URLs** above)
2. Run `python_general_scripts/converting_xls_to_csv.ipynb` if converting XLS → CSV (run from the `python_general_scripts/` directory so relative paths resolve correctly)
3. Run `python3 python_general_scripts/update_dataset_dates.py` from the repo root — it rewrites `coverage_start` and `last_observation` from the files you just added. If you add a new dataset, register its file and date format in that script's `SOURCES` map
4. Update the corresponding `content/datasets/*.md` by hand only for things the script cannot know: `table` / `table_caption` (the summary statistics) and `downloads` URLs if filenames changed
5. CI runs `update_dataset_dates.py --check` and fails the build if any page disagrees with its data file
