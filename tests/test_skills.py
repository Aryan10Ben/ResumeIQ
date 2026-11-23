from resumeiq.skills import categorize, compare_skills, extract_skills, skill_catalog


def test_technical_punctuation_and_aliases_are_preserved():
    text = "Python, Node.js, React.js, C++, C#, PostgreSQL, sklearn, and CI/CD"
    found = extract_skills(text)
    for skill in ("Python", "Node.js", "React", "C++", "C#", "PostgreSQL", "Scikit-learn", "CI/CD"):
        assert skill in found


def test_no_substring_false_positives():
    assert "Java" not in extract_skills("JavaScript")
    assert "Rust" not in extract_skills("trustworthy")
    assert "React" not in extract_skills("reaction")


def test_skills_are_deduplicated_and_comparable():
    resume = extract_skills("Python python3 Django React.js")
    job = extract_skills("Python React MongoDB")
    matched, missing = compare_skills(resume, job)
    assert matched == ["Python", "React"]
    assert missing == ["MongoDB"]


def test_catalog_is_curated():
    catalog = skill_catalog()
    names = [name for group in catalog.values() for name in group]
    assert len(names) >= 90
    assert len(names) == len(set(names))
    assert not any("Fantasy" in name or "Cricket" in name for name in names)
    assert categorize(["Python", "React"])["Programming languages"] == ["Python"]
