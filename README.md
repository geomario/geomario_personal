# Mario — portfolio (Django MVP)

Server-rendered Django version of the portfolio page: one app
(`portfolio`), no database, no build step. Content lives in
`portfolio/data.py` as plain Python lists/dicts — edit that file to
change projects, writing, or the career timeline.

The Projects/Writing tabs, the focus-area filter chips, and the writing
"mesh" grid all work the same as the React version, reimplemented in
`portfolio/static/portfolio/js/app.js` with plain JavaScript (no
framework) — small enough that it doesn't need one.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

## Where things live

- `portfolio/data.py` — all page content (edit this for text changes)
- `portfolio/templates/portfolio/index.html` — the Django template
- `portfolio/static/portfolio/css/style.css` — all styling (same design
  tokens/palette as the artifact version, light + dark mode via
  `prefers-color-scheme`)
- `portfolio/static/portfolio/js/app.js` — tab/filter interactivity
- `portfolio/views.py` — passes `data.py`'s content into the template

## Known placeholders

- The hero photo is an initial ("M") on a tinted square, not a real
  photo — swap in an `<img>` inside `.hero-photo` in the template
  once you have one.

## Growing past an MVP

Right now content is hand-edited Python. The natural next step, given
you're already comfortable with Django, is to turn `Project`, `Post`,
and `TimelineEntry` into real models and manage them from `/admin`
instead of editing `data.py` — the templates already just loop over
lists of dicts with these same keys, so that migration doesn't touch
the HTML or CSS at all.
