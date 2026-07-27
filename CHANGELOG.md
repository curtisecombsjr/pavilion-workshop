# Changelog

Notable changes to the Pavilion workshop deck, demos, configs, and plugins.
Dates are when the work landed; newest first.

## 2026-07-26

### Repository
- Reorganized into `deck/`, `demo/`, `configs/`, `plugins/` with a README in each; added
  `requirements.txt` and this changelog. `build_deck.py` now writes the `.pptx` next to itself, so
  the build works from any directory.

### Deck (`deck/build_deck.py` → 48 slides)
- Converted **all demos from the `raw` scheduler to PBS**; every `pav run` slide is now followed by
  `qstat -a` to prove scheduler dispatch.
- Added inheritance slides (a benefit bullet, a simple `inherits_from` example), a second
  "anatomy" slide, and reordered so the simple test config precedes the fuller one.
- Added dedicated **mode-file**, **series-file**, **Results** (table vs `--json`), and
  **disk-usage** content; folded disk-usage into the custom-commands slide to reclaim space.
- Reworked the saLog slide to show run → PBS → CSV output (no script on screen).
- Permutations now demonstrate **one PBS job per instance** (`share_allocation: false`), with the
  real 6-job `qstat` output.
- All YAML on code slides switched to expanded **block** style (dashes) for readability.
- Front-matter polish: links to the Pavilion GitHub + ReadTheDocs, a searchable-history slide, and
  a "Built for" slide.

### Configs (`configs/`)
- Authored PBS-scheduled test suites (`demo_pbs`, `demo_perms`, `demo_modes`), a series
  (`demo_series`), and mode overlays (`pbs`, `prod`).
- Converted every file from condensed flow YAML to block/dashed style; re-verified live on the
  cluster (pass/fail, parsed metrics, 6-job permutations, series, and mode override).

### Plugins (`plugins/`)
- Added a **MySQL result logger** — one row per result, passwordless via unix_socket auth,
  non-fatal if the database is down.

### Demos (`demo/`)
- Twelve verified run-scripts (`01`–`12`) plus `_lib.sh` and a run-of-show, all exercising PBS +
  `qstat`. Scrubbed of internal infrastructure details for public release.

## Earlier
- Initial deck, demo ladder, and cluster setup; MariaDB installed for the MySQL logger; command
  plugins (`hello`, `recent`, `test-summary`, `disk-usage`) fixed and deployed (they live in the
  framework project). First public push to GitHub.
