"""Curated technology taxonomy, canonical names, and regex alias matching."""
import json
import re
from functools import lru_cache
from pathlib import Path

SKILLS_PATH = Path(__file__).resolve().parent.parent / "data" / "skills.json"


@lru_cache(maxsize=1)
def skill_catalog():
    with SKILLS_PATH.open(encoding="utf-8") as handle:
        catalog = json.load(handle)
    return catalog


@lru_cache(maxsize=1)
def skill_patterns():
    compiled = []
    for category, items in skill_catalog().items():
        for canonical, aliases in items.items():
            for alias in [canonical, *aliases]:
                # Letter/digit lookarounds preserve special technologies like C++, C#, Node.js.
                # A phrase may contain whitespace, but it must not be a substring of another word.
                escaped = re.escape(alias).replace(r"\ ", r"\s+")
                pattern = re.compile(
                    rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])",
                    re.IGNORECASE,
                )
                compiled.append((canonical, category, pattern))
    return compiled


def extract_skills(text):
    """Return unique canonical skill names found in unmodified resume/JD text."""
    found = set()
    for name, _category, pattern in skill_patterns():
        if pattern.search(text or ""):
            found.add(name)
    return sorted(found, key=str.casefold)


def categorize(skills):
    """Group detected skills for an explainable UI."""
    skill_set = set(skills)
    return {
        category: sorted(skill_set.intersection(items), key=str.casefold)
        for category, items in skill_catalog().items()
        if skill_set.intersection(items)
    }


def compare_skills(resume_skills, job_skills):
    resume, job = set(resume_skills), set(job_skills)
    return (
        sorted(resume & job, key=str.casefold),
        sorted(job - resume, key=str.casefold),
    )
