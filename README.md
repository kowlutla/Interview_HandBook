# Interview Prep

A complete, offline-friendly website for preparing for senior engineering interviews: system design first, then topic-by-topic interview questions (Git so far, more topics being added). Pure static HTML, inline SVG diagrams, no build step, no external dependencies.

**Live site:** enable GitHub Pages (Settings, Pages, Source: `main` branch, folder `/docs`) and open `https://<your-user>.github.io/System-Design/`.

## What is inside
- **System Design Handbook** (`docs/handbook`): 61 chapters from first principles to microservices, 32 worked case studies, 4 cheat sheets and an A-Z glossary.
- **System Design Quick Notes** (`docs/quicknotes`): 14 revision sheets (including a 60-question practice bank) and 32 case sheets, in plain words with diagrams and interview Q&A.
- **Interview Book** (`docs/interview`): interview questions per topic with model answers, difficulty levels, diagrams, follow-ups and real-life scenarios. Git is done; Java, Spring, Kafka and others are next.
- **Search** (`docs/search.html`) across everything, with the home page at `docs/index.html`.

## Run locally
Open `docs/index.html`, or run `python -m http.server` inside `docs` and visit `http://localhost:8000`.

## Maintain
- `python -I docs/tools/build_site.py` regenerates Quick Notes navigation, indexes and the home page.
- `python -I docs/tools/build_search.py` rebuilds the search index.
- `python -I docs/tools/check_site.py` checks every link and anchor.
- Page quality checkers: `docs/handbook/tools/check.py`, `docs/quicknotes/tools/check_quick.py` and `docs/interview/tools/check_interview.py`.

## Archive
`archive/` holds the earlier markdown notes, real-world example summaries, books and course PDFs. It is not part of the site.
