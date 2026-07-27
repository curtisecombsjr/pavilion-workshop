# configs/

The Pavilion test suites, mode overlays, and series that the live demos use. All YAML is written
in expanded **block** style (dashes) rather than condensed flow style, for readability on slides.

## Deploying to the cluster

These files live in the repo as the source of truth and are copied into Pavilion's config tree on
`pbs-server` (as the `pavilion` user):

| File | Deploys to | Address as |
|------|-----------|------------|
| `demo_pbs.yaml`    | `~/pavilion2/config/suites/demo_pbs.yaml`    | `demo_pbs.pass` · `demo_pbs.fail` · `demo_pbs.metrics` |
| `demo_perms.yaml`  | `~/pavilion2/config/suites/demo_perms.yaml`  | `demo_perms.matrix` |
| `demo_modes.yaml`  | `~/pavilion2/config/suites/demo_modes.yaml`  | `demo_modes.mode_demo` |
| `demo_series.yaml` | `~/pavilion2/config/series/demo_series.yaml` | `pav series run demo_series` |
| `mode-pbs.yaml`    | `~/pavilion2/config/modes/pbs.yaml`          | `pav run -m pbs <test>` |
| `mode-prod.yaml`   | `~/pavilion2/config/modes/prod.yaml`         | `pav run -m prod <test>` |

## What each one shows

- **`demo_pbs.yaml`** — the basics, all scheduled through PBS. `pass` (trivial PASS), `fail`
  (intentional `exit 7`), and `metrics` (three `echo`s parsed into `throughput_mbs` / `latency_ms`
  / `errors` via `result_parse`).
- **`demo_perms.yaml`** — `permute_on: [size, mode]` expands one definition into 6 test instances.
  `schedule.share_allocation: false` makes Pavilion submit **one PBS job per instance** (the
  default packs them into a single shared allocation).
- **`demo_modes.yaml`** — a test with an `env_label` variable, used to show a mode overriding it.
- **`demo_series.yaml`** — two test sets (`smoke` + `perf`), `ordered: False` so they run
  concurrently (robust for a live run); each set becomes its own PBS job.
- **`mode-pbs.yaml`** — a mode overlay that sets `scheduler: pbs` + the schedule block, so any test
  can be pushed through PBS with `-m pbs`.
- **`mode-prod.yaml`** — a tiny mode overlay that overrides `env_label` to `production`.
