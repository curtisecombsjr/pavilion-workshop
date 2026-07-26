# pavilion-presentation

Monday workshop showing off **Pavilion** (HPC test framework) with **9 live demos** on the PBS
cluster. Built together; **verified working end-to-end**.

## Deliverables

- **`pavilion-workshop.pptx`** — the deck (35 slides + speaker notes). **Upload to Google Slides.**
- **`pavilion-workshop.pdf`** — a rendered handout (bonus).
- **`build_deck.py`** — regenerates the .pptx. Content is a plain `SLIDES` list — edit and re-run:
  `./.venv/bin/python build_deck.py`
- **`demo/`** — the 9 run-scripts + **`demo/README.md`** (run-of-show for the day).
- **`configs/`** — the test/mode/series YAML I authored (deployed to the cluster).

## Running the demos

See **`demo/README.md`**. Short version: `ssh root@pbs-server` → `sudo -iu pavilion` →
`cd ~/pav_demo` → `./01-basic.sh` … `./09-opensearch.sh`.

## Editing the deck

Open `build_deck.py`, edit the `SLIDES` list (each entry is a `title` / `section` / `bullets` /
`code` / `demo` dict, with an optional `notes` for speaker notes), then re-run it. Styling is kept
deliberately simple so Google Slides imports it cleanly.

## Notes

- Cluster / access / gotchas: see the vault note `vault/projects/hpc/pavilion-presentation/index.md`.
- ⚠️ Never show `pavilion.yaml` on screen (plaintext OpenSearch password). The deck uses a redacted version.
- Framework project (PBS plugin, loggers, rules): `../pavilion2/` and its vault notes.
