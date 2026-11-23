import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Import our custom utilities
from utils.text_processing import extract_text, clean_text
from utils.skill_extraction import load_skills, compile_skill_patterns, extract_skills_from_text, compare_skills

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(32)

# Load and compile skill lexicon on startup
print("Loading skill database...")
SKILLS_LIST = load_skills()
COMPILED_SKILLS = compile_skill_patterns(SKILLS_LIST)
print(f"Loaded {len(SKILLS_LIST)} skills.")

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    """
    Checks if the uploaded file has a supported extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """
    Renders the homepage containing upload form and job description text area.
    """
    return render_template('index.html')

@app.get('/health')
def health():
    """Basic readiness check for deployment monitoring."""
    return {'status': 'ok', 'service': 'ResumeIQ', 'skills_loaded': len(SKILLS_LIST)}

@app.route('/match', methods=['POST'])
def match():
    """
    Processes the uploaded resume(s) and job description, then returns matching stats.
    """
    job_description = request.form.get('job_description', '').strip()
    
    if not job_description:
        flash("Please paste a job description.", "error")
        return redirect(url_for('index'))
        
    # Check if files were uploaded
    if 'resumes' not in request.files:
        flash("No resume file uploaded.", "error")
        return redirect(url_for('index'))
        
    uploaded_files = request.files.getlist('resumes')
    
    # Filter files and ensure at least one is valid
    valid_files = [f for f in uploaded_files if f and f.filename and allowed_file(f.filename)]
    
    if not valid_files:
        flash("Please upload at least one valid resume file (.pdf or .txt).", "error")
        return redirect(url_for('index'))

    # Import larger machine-learning libraries only for resume analysis, not initial page load.
    from utils.matching import calculate_match_percentage, generate_recommendation

    # Clean job description text
    cleaned_jd = clean_text(job_description)
    jd_skills = extract_skills_from_text(cleaned_jd, COMPILED_SKILLS)
    
    results = []
    
    for file in valid_files:
        filename = secure_filename(file.filename)
        
        # Save file to a secure temporary path to read it and clean it up immediately
        suffix = os.path.splitext(filename)[1]
        temp_fd, temp_path = tempfile.mkstemp(suffix=suffix)
        
        try:
            with os.fdopen(temp_fd, 'wb') as temp_file:
                file.save(temp_file)
                
            # Process resume text
            raw_text = extract_text(temp_path)
            cleaned_resume = clean_text(raw_text)
            
            # Compute match metrics
            score = calculate_match_percentage(cleaned_resume, cleaned_jd)
            resume_skills = extract_skills_from_text(cleaned_resume, COMPILED_SKILLS)
            
            # Compare skills
            matched_skills, missing_skills = compare_skills(resume_skills, jd_skills)
            
            # Generate recruiter review recommendation
            rec = generate_recommendation(score, matched_skills, missing_skills)
            
            results.append({
                "filename": filename,
                "score": score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "rec_headline": rec["headline"],
                "rec_explanation": rec["explanation"],
                "rec_recommendation": rec["recommendation"],
                "rec_status_class": rec["status_class"],
                "skills_count": {
                    "matched": len(matched_skills),
                    "missing": len(missing_skills)
                }
            })
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            flash(f"Error processing file {filename}", "error")
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    if not results:
        flash("Could not parse or process any of the uploaded resumes.", "error")
        return redirect(url_for('index'))

    # Sort candidates by similarity score descending (hiring dashboard style)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Calculate global details for rendering
    total_candidates = len(results)
    best_match = results[0] if results else None
    
    return render_template(
        'result.html',
        results=results,
        job_description=job_description,
        total_candidates=total_candidates,
        best_match=best_match
    )

if __name__ == '__main__':
    # Run development server, loading port from environment (e.g., for cloud deployment compatibility)
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=os.environ.get('FLASK_DEBUG', '').lower() == 'true', host='0.0.0.0', port=port)
