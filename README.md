# ResumeIQ - AI-Powered Resume Screening & Ranking System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)

An intelligent, modular **Resume Screening and Ranking System** built with **Python**, **NLP (Natural Language Processing)**, **Scikit-learn**, and **Flask**. 

ResumeIQ parses multiple resumes (PDF or TXT), compares them against a target job description using semantic text representations (TF-IDF) and geometric distance metrics (Cosine Similarity), extracts core technical/soft skills via a boundary-safe lookup lexicon, and renders a real-time recruiting leaderboard dashboard.

* **Live Demo:** [Click here to view the live demo](https://your-demo-link.com) *(Placeholder)*
* **GitHub Repository:** [https://github.com/yourusername/resume-screening-system](https://github.com/yourusername/resume-screening-system) *(Placeholder)*

---

## ✨ Features
* **Multi-Resume Leaderboard**: Upload one or multiple resumes concurrently. The system automatically screens and ranks them in descending order of compatibility.
* **TF-IDF Vectorization & Cosine Similarity**: Uses advanced vector space representations to measure semantic match percentages, rather than basic keyword counts.
* **Boundary-Aware Skill Extraction**: Accurately scans for technical terms, handling multi-word skills ("Machine Learning") and special symbol technologies ("C++", ".NET") without false positives (e.g., matches "Go" but ignores "good" or "Django").
* **SaaS-Style UX (Notion/Linear Inspired)**: Designed with glassmorphic panels, vertical height alignment sync, interactive split-pane leadership tables, and a real-time SaaS character counter pill.
* **Recruiter Action Reviews**: Generates custom feedback headlines, compatibility badges (Highly Compatible, Good Fit, etc.), and clear action directives (e.g., "Strongly recommend proceeding to technical interview").

---

## 🛠️ Technology Stack
* **Backend**: Python, Flask
* **Document Parsing**: `pdfplumber` (for robust text extraction)
* **NLP & Vectorization**: Scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
* **Text Processing**: Custom Regex pipelines (punctuation stripping, tokenization, custom English stopword filter)
* **Frontend**: HTML5, CSS3 (Vanilla Glassmorphic Dark Theme), Vanilla JavaScript

---

## 📂 Project Structure

```
resume-screening-system/
├── app.py                   # Flask server entry point & HTTP router
├── requirements.txt         # Python package dependencies
├── .gitignore               # Excludes virtual environments, logs, and OS caches
├── README.md                # Project documentation & portfolio guide
├── data/
│   └── skills.txt           # Predefined lexicon of 650+ tech & soft skills
├── samples/                 # Sample candidate resumes for evaluation
│   ├── alice_dev.txt        # High-match Full-Stack Engineer resume
│   ├── bob_ds.txt           # High-match Data Scientist resume
│   └── carol_design.txt     # UI/UX Designer resume (baseline low match)
├── static/
│   └── style.css            # Notion-inspired glassmorphism styles
├── templates/
│   ├── index.html           # Homepage (Drag-and-drop file upload & JD inputs)
│   └── result.html          # Interactive split-screen recruitment dashboard
├── utils/
│   ├── __init__.py
│   ├── matching.py          # TF-IDF calculations & recruiter summaries
│   ├── skill_extraction.py  # Regex boundary skill parser & overlap analysis
│   └── text_processing.py   # PDF/TXT document parsers & cleaning pipelines
└── test_screening.py        # Programmatic integration tests
```

---

## ⚙️ Local Installation & Running

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/resume-screening-system.git
cd resume-screening-system
```

### 2. Set Up a Virtual Environment
Ensure Python 3.9+ is installed, then create and activate a virtual environment:
```bash
# Create venv
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows (CMD)
venv\Scripts\activate

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Web App
Launch the local development server:
```bash
python app.py
```
Open **`http://127.0.0.1:5001`** in your web browser.

### 5. Run Integration Tests
To test the pipeline math, token extraction, and scoring thresholds programmatically:
```bash
python test_screening.py
```

---

## ☁️ Deployment Instructions

### Deploying to Render (Recommended & Free)
1. **Create a Render Account**: Sign up at [render.com](https://render.com/).
2. **Create a Web Service**: Link your GitHub repository.
3. **Configure Settings**:
   * **Runtime**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app` *(Note: Add `gunicorn` to requirements.txt if deploying to Render, or use python command)*
     * *Alternative Start Command*: `python -m gunicorn app:app` or set start command to `python app.py` (making sure to bind the host port dynamically).
   * **Port**: Render automatically binds to the `$PORT` environment variable. In `app.py`, change `app.run(port=5001)` to read the port from env:
     ```python
     port = int(os.environ.get("PORT", 5001))
     app.run(host="0.0.0.0", port=port)
     ```
     *(This is already handled cleanly inside the app.py start command!)*

---

## 🧠 Portfolio talking points (Prep for Recruiters)

Be prepared to explain the technical design choices behind ResumeIQ in interviews:

### 1. Term Frequency-Inverse Document Frequency (TF-IDF)
* **What is it?** A statistical measure used to evaluate how relevant a word is to a document in a collection or corpus.
* **Why did you use it?** Simple word counts are heavily biased towards frequently repeated generic words ("experience", "work", "responsibilities"). TF-IDF balances this out:
  * **TF (Term Frequency)**: Rewards words that appear frequently in a resume.
  * **IDF (Inverse Document Frequency)**: Penalizes words that are common across *all* job postings and resumes, elevating technical terms ("PyTorch", "Kubernetes", "Flask") which occur more uniquely.

### 2. Cosine Similarity vs. Jaccard Index
* **Why Cosine Similarity?** Cosine similarity measures the cosine of the angle between two multi-dimensional document vectors. It evaluates *directional alignment* rather than vector magnitude.
* **Why does this matter?** If a resume is short (e.g. 1 page) and the job description is very long (e.g. 3 pages), Jaccard similarity (which checks simple set intersection divided by union) would penalize the candidate heavily for the length difference. Cosine similarity looks at the overlap of features regardless of document length, giving a fairer score.

### 3. Edge-Case Regex Bounds for Skills
* **The challenge**: How do you match a skill like `C++` or `.NET` using standard regex without throwing errors or matching partially?
* **Our solution**:
  * We escape characters with `re.escape()`.
  * We dynamically check boundaries: we only prepend `\b` (word boundary) if the skill starts with an alphanumeric character, and only append it if it ends with one.
  * For `C++`, this compiles to `\bc\+\+` (front boundary only), successfully matching it while avoiding partial matches (like matching `go` inside `django` because `\bgo\b` is used).

---

## 📄 License
Distributed under the MIT License. See [LICENSE](LICENSE) for more details.
