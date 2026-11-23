# ResumeIQ evaluation and benchmarking

## Original baseline

Original ResumeIQ combined TF-IDF cosine text similarity with a noisy list
of hundreds of keywords, including unrelated terms. Its percentage was
not a calibrated hiring or ATS score.

## Revised baseline

The revised system uses a curated taxonomy, special-character-aware aliases,
separate overlap and similarity measurements, and an explicit heuristic
weighted score. These weights are a product choice, **not learned from
ground-truth labels**.

## Deterministic fictional fixtures

- samples/alice_dev.txt: full-stack engineer.
- samples/bob_ds.txt: data scientist.
- samples/carol_design.txt: product designer.

Automated tests verify Alice ranks highest for the bundled full-stack job
description and Bob for an example data-science description. These tests
show basic relevance, not statistical validity.

## Run tests

~~~bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
~~~

Tests cover alias extraction, punctuation, duplicate handling, TF-IDF edge
cases, invalid uploads, filename safety, app endpoints, a real in-memory PDF,
missing inputs and deterministic rankings.

## Next-stage evaluation

Collect a consented, de-identified, human-labelled benchmark of resumes
and job descriptions. Evaluate skill precision/recall, top-k ranking precision,
NDCG, runtime latency and known subgroup failure modes where ethically and
legally permissible. Do not claim model accuracy without such evidence.
