# news-image-20261125 v2 (rebuild) — Daylight wire desk

"Sum up 25 November's world news in one image" — 46 verified stories
from Wednesday 25 November 2026, 7 regions, in a single 1024x1024
poster. Daylight wire desk: paper-white ground, ink-black masthead
band, signal-red rules and square number chips, teal accents, linocut
scenes with heavy black outlines.

## Files

- `render_poster.py` — draws `entry.png` (1024x1024 RGB PNG) and
  `preview-300.png` from the story data in the file. Needs Pillow
  (`pip install pillow`) and the DejaVu fonts
  (`/usr/share/fonts/truetype/dejavu/`). Byte-deterministic across
  renders; sharpened (UnsharpMask radius 2, 150%).
- `main.py` — the entrypoint. Pure stdlib: validates and copies the
  bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (else
  `/output/entry.png`, else `output.png`), chmod 0644.
- `STRATEGY.md` — the winning approach and the rebuild note.
- `tests/` — 6 tests: determinism, clearance 0, main.py stdlib only,
  main.py runs as uid 65534 on a read-only repo copy and writes a
  byte-identical output mode 0644, entry.png is 1024x1024 RGB.

## Render and test

```sh
python3 render_poster.py
python3 -m unittest discover -s tests
python3 main.py   # with MAKEFUN_OUTPUT_DIR set to check the copy
```

## Verify

- `entry.png` is 1024x1024, byte-identical across two renders.
- Clearance violations: 0 (no text touches a border line; every label
  sits inside its shape with clearance).
- Masthead + 3 hero headlines + KPI numbers read at 300px
  (see `preview-300.png`); ALSO ON items 42–46 complete with no
  truncation.
