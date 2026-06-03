import os
import sys

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.text_processing import extract_text, clean_text
from utils.skill_extraction import load_skills, compile_skill_patterns, extract_skills_from_text, compare_skills
from utils.matching import calculate_match_percentage, generate_recommendation

# Mock job descriptions
FULL_STACK_JD = """
Full-Stack Web Developer Requirements:
- Build responsive and interactive user interfaces using React, HTML5, CSS3, and JavaScript/TypeScript.
- Design, build, and maintain RESTful API backends using Python and Flask.
- Integrate relational and non-relational database services such as PostgreSQL and MongoDB.
- Build secure, scalable applications utilizing Git version control, Docker containers, and CI/CD pipelines.
- Practice agile methodology (Scrum, Jira) to deliver clean, documented, and fully tested code.
- Knowledge of system design, Microservices, and cloud services (AWS or GCP).

Required Skills: Python, Flask, React, JavaScript, SQL, PostgreSQL, MongoDB, Git, Docker, Rest API.
"""

DATA_SCIENCE_JD = """
Data Scientist Responsibilities:
- Design, train, and deploy Machine Learning models (supervised/unsupervised) to solve complex predictive problems.
- Extract, clean, and process large datasets using Python, Pandas, and NumPy.
- Build natural language processing (NLP) pipelines for classification and text sentiment.
- Work closely with cloud infrastructure on AWS (S3, SageMaker) to run model pipelines at scale.
- Present findings using data visualization tools like Matplotlib, Seaborn, or Tableau.
- Work within an Agile Scrum team environment.

Required Skills: Python, Machine Learning, NLP, Pandas, NumPy, Scikit-learn, AWS, SQL, Docker, Tableau.
"""

def run_tests():
    print("==================================================")
    print("STARTING RESUME SCREENING PIPELINE INTEGRATION TESTS")
    print("==================================================")

    # 1. Load skill lexicon
    print("\n[Step 1] Loading skill lexicon...")
    skills = load_skills()
    print(f"Loaded {len(skills)} skills successfully.")
    compiled_skills = compile_skill_patterns(skills)
    
    # 2. Load resumes
    print("\n[Step 2] Reading sample resumes...")
    samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
    
    alice_path = os.path.join(samples_dir, 'alice_dev.txt')
    bob_path = os.path.join(samples_dir, 'bob_ds.txt')
    carol_path = os.path.join(samples_dir, 'carol_design.txt')
    
    alice_raw = extract_text(alice_path)
    bob_raw = extract_text(bob_path)
    carol_raw = extract_text(carol_path)
    
    print(f"Loaded Alice Resume: {len(alice_raw)} chars")
    print(f"Loaded Bob Resume: {len(bob_raw)} chars")
    print(f"Loaded Carol Resume: {len(carol_raw)} chars")
    
    # Check that reading succeeded
    assert len(alice_raw) > 0, "Failed to read Alice's resume!"
    assert len(bob_raw) > 0, "Failed to read Bob's resume!"
    assert len(carol_raw) > 0, "Failed to read Carol's resume!"

    # 3. Preprocessing
    print("\n[Step 3] Preprocessing texts...")
    cleaned_alice = clean_text(alice_raw)
    cleaned_bob = clean_text(bob_raw)
    cleaned_carol = clean_text(carol_raw)
    
    cleaned_fs_jd = clean_text(FULL_STACK_JD)
    cleaned_ds_jd = clean_text(DATA_SCIENCE_JD)
    
    print(f"Alice cleaned text (sample): {cleaned_alice[:100]}...")
    
    # 4. Run Matching Test 1: Full-Stack Developer Job Description
    print("\n[Step 4] Running matches for Full-Stack Developer JD...")
    
    # Skills in JD
    fs_jd_skills = extract_skills_from_text(cleaned_fs_jd, compiled_skills)
    print(f"Skills detected in Job Description: {fs_jd_skills}")
    
    # Alice Matching
    alice_score_fs = calculate_match_percentage(cleaned_alice, cleaned_fs_jd)
    alice_skills_fs = extract_skills_from_text(cleaned_alice, compiled_skills)
    alice_matched_fs, alice_missing_fs = compare_skills(alice_skills_fs, fs_jd_skills)
    
    # Bob Matching
    bob_score_fs = calculate_match_percentage(cleaned_bob, cleaned_fs_jd)
    bob_skills_fs = extract_skills_from_text(cleaned_bob, compiled_skills)
    bob_matched_fs, bob_missing_fs = compare_skills(bob_skills_fs, fs_jd_skills)
    
    # Carol Matching
    carol_score_fs = calculate_match_percentage(cleaned_carol, cleaned_fs_jd)
    carol_skills_fs = extract_skills_from_text(cleaned_carol, compiled_skills)
    carol_matched_fs, carol_missing_fs = compare_skills(carol_skills_fs, fs_jd_skills)

    print(f"Alice (Full-Stack Dev) match score: {alice_score_fs}% | Matched Skills: {alice_matched_fs}")
    print(f"Bob (Data Scientist) match score: {bob_score_fs}% | Matched Skills: {bob_matched_fs}")
    print(f"Carol (UI Designer) match score: {carol_score_fs}% | Matched Skills: {carol_matched_fs}")
    
    # Assertions
    assert alice_score_fs > bob_score_fs, "Alice should match Full-Stack role better than Bob!"
    assert alice_score_fs > carol_score_fs, "Alice should match Full-Stack role better than Carol!"
    print("-> Full-Stack Match assertions passed! Alice ranks #1.")

    # 5. Run Matching Test 2: Data Scientist Job Description
    print("\n[Step 5] Running matches for Data Scientist JD...")
    
    ds_jd_skills = extract_skills_from_text(cleaned_ds_jd, compiled_skills)
    print(f"Skills detected in Job Description: {ds_jd_skills}")
    
    # Alice Matching
    alice_score_ds = calculate_match_percentage(cleaned_alice, cleaned_ds_jd)
    alice_skills_ds = extract_skills_from_text(cleaned_alice, compiled_skills)
    alice_matched_ds, alice_missing_ds = compare_skills(alice_skills_ds, ds_jd_skills)
    
    # Bob Matching
    bob_score_ds = calculate_match_percentage(cleaned_bob, cleaned_ds_jd)
    bob_skills_ds = extract_skills_from_text(cleaned_bob, compiled_skills)
    bob_matched_ds, bob_missing_ds = compare_skills(bob_skills_ds, ds_jd_skills)
    
    # Carol Matching
    carol_score_ds = calculate_match_percentage(cleaned_carol, cleaned_ds_jd)
    carol_skills_ds = extract_skills_from_text(cleaned_carol, compiled_skills)
    carol_matched_ds, carol_missing_ds = compare_skills(carol_skills_ds, ds_jd_skills)

    print(f"Alice (Full-Stack Dev) match score: {alice_score_ds}% | Matched Skills: {alice_matched_ds}")
    print(f"Bob (Data Scientist) match score: {bob_score_ds}% | Matched Skills: {bob_matched_ds}")
    print(f"Carol (UI Designer) match score: {carol_score_ds}% | Matched Skills: {carol_matched_ds}")
    
    # Assertions
    assert bob_score_ds > alice_score_ds, "Bob should match Data Scientist role better than Alice!"
    assert bob_score_ds > carol_score_ds, "Bob should match Data Scientist role better than Carol!"
    print("-> Data Science Match assertions passed! Bob ranks #1.")
    
    # 6. Test Recruiter Recommendations
    print("\n[Step 6] Verifying Recruiter recommendations...")
    rec_alice_fs = generate_recommendation(alice_score_fs, alice_matched_fs, alice_missing_fs)
    print(f"Alice Recruiter Summary: {rec_alice_fs['headline']} (Status: {rec_alice_fs['status_class']})")
    print(f"Recommendation: {rec_alice_fs['recommendation']}")
    
    assert rec_alice_fs['status_class'] in ['success', 'warning', 'info', 'danger']
    print("-> Recommendation verification passed!")
    
    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
