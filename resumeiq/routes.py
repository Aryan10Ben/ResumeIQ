"""HTTP-only request handling. Parsing and matching live in services."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from resumeiq.service import screen_documents
from resumeiq.skills import skill_catalog

screening = Blueprint("screening", __name__)


@screening.get("/")
def index():
    return render_template("index.html")


@screening.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ResumeIQ",
        "skills_loaded": sum(len(group) for group in skill_catalog().values()),
    }


def render_results(documents, jd):
    results, errors = screen_documents(
        documents, jd, max_bytes=current_app.config["MAX_FILE_BYTES"]
    )
    for error in errors:
        flash(error, "error")
    if not results:
        if not errors:
            flash("No readable resumes were provided.", "error")
        return redirect(url_for("screening.index"))
    return render_template(
        "result.html",
        results=results,
        job_description=jd,
        total_candidates=len(results),
        best_match=results[0],
    )


@screening.post("/match")
def match():
    jd = request.form.get("job_description", "").strip()
    if not jd:
        flash("Please paste a job description.", "error")
        return redirect(url_for("screening.index"))
    if len(jd) > current_app.config["MAX_JOB_DESCRIPTION_CHARS"]:
        flash("The job description exceeds the 5,000-character limit.", "error")
        return redirect(url_for("screening.index"))

    uploaded = [f for f in request.files.getlist("resumes") if f and f.filename]
    if not uploaded:
        flash("Please upload at least one PDF or TXT resume.", "error")
        return redirect(url_for("screening.index"))
    if len(uploaded) > current_app.config["MAX_UPLOAD_FILES"]:
        flash("You can compare up to five resumes per request.", "error")
        return redirect(url_for("screening.index"))

    # Read only max+1 bytes, avoiding unbounded memory consumption.
    maximum = current_app.config["MAX_FILE_BYTES"]
    documents = [(f.filename, f.stream.read(maximum + 1)) for f in uploaded]
    return render_results(documents, jd)
