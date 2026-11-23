# ResumeIQ architecture

## End-to-end flow

Browser -> Flask Blueprint -> upload validation -> in-memory PDF/TXT extraction
-> canonical skill detection -> TF-IDF similarity -> heuristic score
-> ranked HTML report shown in the original upload-first interface.

## Responsibilities

- app.py: stable WSGI entry point for Vercel.
- resumeiq/__init__.py: Flask app factory and request-size configuration.
- resumeiq/routes.py: input checks, upload route, and health check.
- resumeiq/parser.py: in-memory file validation and extraction.
- resumeiq/skills.py: curated JSON taxonomy and alias matching.
- resumeiq/scoring.py: normalized text, TF-IDF similarity, heuristic ranking.
- resumeiq/service.py: end-to-end screening, sample fixtures for tests, deterministic sorting.
- templates/: Jinja server-rendered HTML.
- public/static/: Vercel CDN stylesheets and browser scripts.
- tests/: isolated unit and Flask integration tests.

## Why Flask?

Screening is a small, synchronous workflow. Flask is easy to demonstrate, test
and deploy. Splitting it into microservices or queues would add operational
complexity without a proven need. Large scikit-learn imports are deferred
until an actual screening request.

## Ranking formula

The heuristic relevance score uses 65% recognized job-skill coverage
plus 35% TF-IDF bigram cosine similarity. When no skills are recognized in the
job description, scoring falls back to cosine similarity alone.

Scores measure a limited kind of text relevance. They are **not ATS scores**,
hiring probabilities, independently validated assessments or grounds for
automatic rejection.

## Privacy and retention

Resume content is read into server memory, analyzed and used to generate a
report. This application does not intentionally persist resumes, add a
database, or forward documents to an external LLM. The browser displays the ranked report without downloading or retaining uploads.

## Limitations

- PDFs must contain selectable text; OCR is not implemented.
- The taxonomy misses synonyms that have not been curated.
- Keyword overlap is not a proxy for job ability or work experience.
- Vercel's request-size limits constrain batch uploads.
- Human review is mandatory for consequential hiring decisions.
