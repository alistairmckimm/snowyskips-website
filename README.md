# Snowy Skips website — generator source (branch `source`)

Not served by GitHub Pages (Pages serves `main`). This branch holds the scripts and images that build the site.

1. `sh setup.sh` — restores /home/claude/site and /tmp/blobmap.json
2. Build: `cd /home/claude/site && LIVE=1 python3 build_site.py && python3 -I gen_towns.py && python3 -I gen_pages.py`
3. Deploy: clone `main` to /home/claude/repo, delete everything except .git, .nojekyll, README.md, copy /home/claude/website-live/* in, commit, push.

- `site/project/*.dc.html` — page sections (from the design canvas)
- `site/gen_pages.py` — splits into pages, FAQ, articles (`mains[...]`, `PAGES`, `META`), sitemap
- `site/gen_towns.py`, `site/towns.py` — town pages
- After editing source, commit back to this branch.
