"""Resume screening workflow shared by uploads and the one-click demo."""
from pathlib import Path
from werkzeug.utils import secure_filename

from resumeiq.parser import extract_text, validate_upload, InvalidResume
from resumeiq.scoring import calculate_score, recruiter_summary
from resumeiq.skills import compare_skills, extract_skills, categorize

ROOT = Path(__file__).resolve().parent.parent

DEMO_JOB_DESCRIPTION = """Full-Stack Software Engineer
Build applications using Python, Flask, React, JavaScript, and SQL.
Required Skills: Python, Flask, React, JavaScript, PostgreSQL, Docker, Git.
Preferred Skills: AWS, TypeScript.
"""


def screen_documents(documents, job_description, *, max_bytes=3 * 1024 * 1024):
    """Return ranked, explainable candidate reports.

    documents: iterable[(filename, bytes)]
    Parsing and extraction errors are reported per file without storing uploads.
    """
    job_skills = extract_skills(job_description)
    results, errors = [], []
    for filename, data in documents:
        safe_name = secure_filename(filename or "") or "resume"
        try:
            suffix = validate_upload(filename, data, max_bytes=max_bytes)
            raw_text = extract_text(data, suffix)
            resume_skills = extract_skills(raw_text)
            matched, missing = compare_skills(resume_skills, job_skills)
            score_data = calculate_score(raw_text, job_description, matched, job_skills)
            recommendation = recruiter_summary(score_data["score"], matched, missing)
            results.append({
                "filename": safe_name,
                "matched_skills": matched,
                "missing_skills": missing,
                "resume_skills": resume_skills,
                "skill_categories": categorize(matched),
                "skills_count": {"matched": len(matched), "missing": len(missing)},
                **score_data,
                "rec_headline": recommendation["headline"],
                "rec_explanation": recommendation["explanation"],
                "rec_recommendation": recommendation["recommendation"],
                "rec_status_class": recommendation["status_class"],
            })
        except (InvalidResume, UnicodeError) as exc:
            errors.append(f"{safe_name}: {exc}")
    results.sort(key=lambda r: (-r["score"], r["filename"].casefold()))
    return results, errors


def sample_documents():
    """Bundled fictional resumes for an instant, privacy-friendly demo."""
    names = ["alice_dev.txt", "bob_ds.txt", "carol_design.txt"]
    return [(name, (ROOT / "samples" / name).read_bytes()) for name in names]
