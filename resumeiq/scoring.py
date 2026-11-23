"""Transparent relevance heuristics (not ATS or hiring-probability estimates)."""
import re


def normalize_for_similarity(text):
    """Keep meaningful tech punctuation while normalizing prose."""
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9+#./\-\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def cosine_text_similarity(resume_text, job_description):
    """TF-IDF bigram cosine similarity, 0-100. Uses lazy ML imports."""
    a = normalize_for_similarity(resume_text)
    b = normalize_for_similarity(job_description)
    if not a or not b:
        return 0.0
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    try:
        vectors = TfidfVectorizer(
            stop_words="english", ngram_range=(1, 2), max_features=10_000
        ).fit_transform([a, b])
        return round(float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0]) * 100, 2)
    except ValueError:
        return 0.0


def calculate_score(resume_text, job_description, matched_skills, job_skills):
    similarity = cosine_text_similarity(resume_text, job_description)
    coverage = round(100 * len(matched_skills) / len(job_skills), 2) if job_skills else None
    # No skills in JD? Do not fabricate 100% coverage.
    score = round(0.65 * coverage + 0.35 * similarity, 2) if coverage is not None else similarity
    return {
        "score": score,
        "text_similarity": similarity,
        "skill_coverage": coverage,
        "score_method": "65% listed-skill coverage + 35% TF-IDF cosine similarity"
        if coverage is not None else "TF-IDF cosine similarity (no recognized JD skills)",
    }


def recruiter_summary(score, matched, missing):
    """Neutral screening guidance, not automated hiring/rejection decisions."""
    if score >= 70:
        return {
            "headline": "Strong evidence of role overlap",
            "explanation": "This resume has relatively strong overlap with the supplied job description. Verify depth of experience in an interview.",
            "recommendation": "Review examples of relevant work and supporting evidence.",
            "status_class": "success",
        }
    if score >= 40:
        return {
            "headline": "Partial role overlap",
            "explanation": "Several requirements overlap, but relevant gaps or terminology differences remain. Manual review is recommended.",
            "recommendation": "Discuss transferable experience and listed skill gaps.",
            "status_class": "warning",
        }
    return {
        "headline": "Limited detected overlap",
        "explanation": "The heuristic found limited overlap. Missing keywords do not establish a lack of real-world capability.",
        "recommendation": "Use human review; do not automatically reject a candidate.",
        "status_class": "info",
    }
