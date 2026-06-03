from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_match_percentage(resume_text, job_desc_text):
    """
    Computes cosine similarity between the TF-IDF vectors of the resume and job description.
    Returns the similarity as a percentage rounded to 2 decimal places.
    """
    if not resume_text.strip() or not job_desc_text.strip():
        return 0.0

    try:
        # Initialize TfidfVectorizer
        vectorizer = TfidfVectorizer()
        
        # Fit and transform the texts
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])
        
        # Calculate Cosine Similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert similarity to percentage
        match_percentage = float(similarity * 100)
        return round(match_percentage, 2)
    except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        return 0.0

def generate_recommendation(score, matched_skills, missing_skills):
    """
    Generates a structured, professional recruiter-style summary and recommendation 
    based on the similarity score and skill overlap.
    """
    matched_str = ", ".join(matched_skills[:4]) if matched_skills else "None"
    missing_str = ", ".join(missing_skills[:4]) if missing_skills else "None"
    
    if score >= 80:
        headline = "Highly Compatible Candidate"
        explanation = (
            f"The candidate's resume shows an excellent <strong>{score}%</strong> match with the job description. "
            f"They possess critical overlapping skills, including <strong>{matched_str}</strong>. "
        )
        if missing_skills:
            explanation += f"To achieve absolute alignment, the candidate could highlight or acquire experience in <strong>{missing_str}</strong>."
        else:
            explanation += "They meet all major technical requirements identified."
        recommendation = "Strongly recommend proceeding to technical interview."
        status_class = "success"
        
    elif score >= 60:
        headline = "Good Fit with Gaps"
        explanation = (
            f"The candidate is a solid match (<strong>{score}%</strong>). They demonstrate strength in core skills like <strong>{matched_str}</strong>. "
        )
        if missing_skills:
            explanation += f"However, they are missing critical requirements: <strong>{missing_str}</strong>. Adding these or highlighting similar experiences would strengthen their profile."
        else:
            explanation += "There are minor differences in domain-specific terminology."
        recommendation = "Recommend for screening call to assess depth in missing core areas."
        status_class = "warning"
        
    elif score >= 35:
        headline = "Potential Fit (Minor Overlap)"
        explanation = (
            f"The candidate has a moderate alignment of <strong>{score}%</strong>. "
            f"While they show exposure to <strong>{matched_str}</strong>, they are missing several major requirements such as <strong>{missing_str}</strong>."
        )
        recommendation = "Consider only if they have transferable experience or for junior/support roles."
        status_class = "info"
        
    else:
        headline = "Low Alignment"
        explanation = (
            f"The candidate has a low compatibility rating of <strong>{score}%</strong>. "
            f"They lack key competencies requested in the job description (missing: <strong>{missing_str}</strong>) and only share minimal overlap (matched: <strong>{matched_str}</strong>)."
        )
        recommendation = "Keep on file for other positions; not recommended for this role."
        status_class = "danger"
        
    return {
        "headline": headline,
        "explanation": explanation,
        "recommendation": recommendation,
        "status_class": status_class
    }
