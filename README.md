# ResumeIQ — Explainable Resume Matching

**Live demo:** https://resumeiq-ten-blue.vercel.app

ResumeIQ is a Flask + Python NLP application that compares up to five PDF or
TXT resumes with a job description. It detects relevant technologies, computes
an explainable heuristic, and ranks candidate documents in an interactive
report. It is an educational decision-support prototype, **not a certified
ATS or automated hiring system**.

## Features

- In-memory PDF/TXT parsing with type, size and page limits
- Curated technical-skills taxonomy and aliases (Python, C++, C#, Node.js, etc.)
- Transparent 65% skill coverage / 35% TF-IDF cosine similarity heuristic
- Ranked candidate reports and missing-skill explanations
- Original upload-first interface, with a multi-resume ranking report
- Responsive UI and keyboard-accessible candidate selection
- Flask health endpoint, automated integration tests, GitHub Actions CI

## Tech stack

Python 3.12, Flask, scikit-learn, pdfplumber, Jinja templates, vanilla
JavaScript, CSS, pytest, GitHub Actions, and Vercel.

## Run locally

~~~bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
python app.py
~~~

Open http://127.0.0.1:5001, upload a PDF/TXT resume, paste a job description and select **Screen & Rank Resumes**.

For production, configure a strong, stable FLASK_SECRET_KEY environment
variable in Vercel; do not commit it to the repository.

## Run the tests

~~~bash
python -m pytest -q
~~~

The suite checks candidate rankings, skill aliases, invalid uploads,
safe rendering, actual PDF extraction, the restored interface, and Flask endpoint behavior.
GitHub Actions runs tests on every feature-branch and main push.

## Matching algorithm

1. Validate PDF/TXT uploads and extract selectable text in memory.
2. Detect canonical skills in the original text, including aliases.
3. Calculate TF-IDF bigram cosine text similarity.
4. Calculate coverage of recognized job-description skills.
5. Combine 65% skill coverage + 35% cosine similarity, or use cosine
   similarity alone if no recognized job skills are present.
6. Rank by relevance score and show matching and missing skills in the original report layout.

The result is **not a measured ATS score**, employer decision, hiring
probability or validated capability assessment. Human review is essential.

## Project layout

~~~text
app.py                   Flask WSGI entry point
resumeiq/
  __init__.py            App factory / configuration
  routes.py              HTTP request handling
  parser.py              PDF/TXT validation and extraction
  skills.py              Canonical skill mapping and aliases
  scoring.py             TF-IDF and transparent heuristic
  service.py             Candidate screening workflow
data/skills.json         Curated vocabulary
public/static/           Browser JS and original CSS theme
templates/               HTML/Jinja views
samples/                 Fictional resumes
tests/                   Unit and integration tests
docs/                    Architecture, evaluation, security
.github/workflows/       Automated CI
~~~

Read [architecture](docs/architecture.md), [evaluation](docs/evaluation.md)
and [security](docs/security.md) for details.

## Deployment and constraints

Hosted as a Flask Python function on Vercel. The standard function
request-body cap is 4.5 MB, and the app enforces 4 MiB. Individual resumes
are capped at 3 MiB, batches at 5 files, and PDFs at 15 pages. Scanned PDFs
without selectable text are not yet supported. No resume database is used.

## Interview discussion topics

- How do TF-IDF vectors and cosine similarity compare documents?
- How do you prevent false matches for special terms like C++ and Node.js?
- Why combine coverage and similarity? What happens without ground truth?
- How do you secure file uploads and prevent browser-side XSS?
- Why separate routes, parsing, extraction, and scoring modules?
- How do unit, integration, security and deployment checks differ?
- Why is human review necessary in automated candidate ranking?
