import os
import re

# Get absolute path to skills.txt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_FILE_PATH = os.path.join(BASE_DIR, 'data', 'skills.txt')

def load_skills(file_path=SKILLS_FILE_PATH):
    """
    Loads list of skills from a text file, cleans them,
    and returns a unique list sorted by length in descending order.
    Sorting by length helps match longer multi-word phrases first.
    """
    skills = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    skill = line.strip()
                    if skill:
                        skills.append(skill)
        except Exception as e:
            print(f"Error reading skills file: {e}")
    
    # Fallback list if the file is missing or empty
    if not skills:
        skills = [
            "Python", "Java", "C++", "C#", "Go", "Rust", "JavaScript", "TypeScript", 
            "HTML", "CSS", "SQL", "NoSQL", "MongoDB", "PostgreSQL", "Flask", "Django", 
            "FastAPI", "React", "Angular", "Vue", "Node.js", "Machine Learning", 
            "Deep Learning", "NLP", "Data Science", "Pandas", "NumPy", "Scikit-learn", 
            "TensorFlow", "PyTorch", "AWS", "Azure", "GCP", "Docker", "Kubernetes", 
            "Git", "CI/CD", "Linux", "Bash", "Agile", "Scrum", "Communication", 
            "Leadership", "Teamwork", "Problem Solving"
        ]
    
    # Deduplicate and sort by length descending
    skills = list(set(skills))
    skills.sort(key=len, reverse=True)
    return skills

def compile_skill_patterns(skills):
    """
    Compiles regex patterns for each skill, ensuring correct boundary detection
    for both alphanumeric and special symbol skills (e.g. 'C++', '.NET').
    """
    compiled = []
    for skill in skills:
        escaped = re.escape(skill)
        
        # Determine word boundaries based on character type
        start_boundary = r'\b' if skill[0].isalnum() else ''
        end_boundary = r'\b' if skill[-1].isalnum() else ''
        
        # Compile pattern
        pattern_str = f"{start_boundary}{escaped}{end_boundary}"
        pattern = re.compile(pattern_str, re.IGNORECASE)
        compiled.append((skill, pattern))
    return compiled

def extract_skills_from_text(text, compiled_patterns):
    """
    Scans text for skills using compiled regex patterns and returns a list of found skills.
    """
    found = []
    if not text:
        return found
        
    for skill, pattern in compiled_patterns:
        if pattern.search(text):
            found.append(skill)
            
    # Sort alphabetically for consistent output
    return sorted(found, key=lambda x: x.lower())

def compare_skills(resume_skills, job_desc_skills):
    """
    Compares the skills present in a resume vs the skills mentioned in the job description.
    Returns:
        - matched_skills: Skills found in both
        - missing_skills: Skills in job description but not in the resume
    """
    resume_set = set(resume_skills)
    job_set = set(job_desc_skills)
    
    matched_skills = sorted(list(resume_set.intersection(job_set)), key=lambda x: x.lower())
    missing_skills = sorted(list(job_set.difference(resume_set)), key=lambda x: x.lower())
    
    return matched_skills, missing_skills
