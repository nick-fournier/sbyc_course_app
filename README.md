# SBYC FNS course charts

Course maps and signal flags for South Beach Yacht Club's Friday Night Series,
served at https://fns.nicholasfournier.com.

It's a static site: `build.py` turns the YAML course data in `data/` into
`dist/data/courses.js` and `dist/data/flags.js`, and copies the page from `site/`.
The browser does everything else, including GPX export and the port/starboard swap.

## Local development

```bash
uv run build.py                   # or: pip install pyyaml && python build.py
python -m http.server -d dist     # http://localhost:8000
```

## Updating courses for a new season

1. Copy the current season, e.g. `cp -r data/map_data data/map_data_fall26`, to keep an archive.
2. Edit `data/map_data/course_{marks,objects,order}.yaml`. A trailing `(S)` or `(P)` on a
   mark in `course_order.yaml` forces starboard or port rounding for that mark.
3. Run `uv run build.py`. It fails loudly on bad data, and so does CI.
4. Push to `main`. CI builds `nichfournier/fns:latest`. Then deploy on razz:
   `docker compose pull fns && docker compose up -d fns` in `clubhouse-server/razz`.

## Layout

| Path | What |
|---|---|
| `build.py` | YAML -> JS data files; copies `site/` into `dist/` |
| `data/` | course YAML per season (`map_data` is the live one) and `flags.yaml` |
| `site/` | `index.html` (chart), `flags.html`, CSS, JS, flag images |
| `Dockerfile` | builds `dist/`, then serves it with nginx |
