# Interview Prep

A static website for senior engineering interview preparation: a System Design Handbook, Quick Notes, and an Interview Book (37 topics, Java to security and your own project stories). Pure HTML, inline SVG diagrams, no external dependencies.

## Layout
| Folder | What it is |
|---|---|
| `site/` | The published website (handbook, quicknotes, interview, search, home). |
| `tools/` | Build and check scripts (Python, standard library only). |
| `authoring/` | Writing guides used to produce the pages. |

## Run locally
```
python -m http.server --directory site 8000
```
Then open http://localhost:8000.

## Maintain
Run from the repo root:
```
python -I tools/build_site.py      # navigation, indexes, hub pages
python -I tools/build_search.py    # search index
python -I tools/check_site.py      # every link and anchor
python -I tools/check_interview.py topics/<page>.html   # per-page checks (also check_handbook.py, check_quick.py)
```

## Publish
`.github/workflows/pages.yml` builds, checks and deploys `site/` to GitHub Pages on every push to `main`. In the repo settings, set Pages source to "GitHub Actions".
