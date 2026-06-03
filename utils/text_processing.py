import re
import os
import pdfplumber

# Set of standard English stopwords to keep the installation lean and reliable
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't",
    'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
    "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
    'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
    'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_txt(txt_path):
    """
    Extracts text from a plain text file, trying multiple encodings.
    """
    encodings = ['utf-8', 'latin-1', 'utf-16']
    for enc in encodings:
        try:
            with open(txt_path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading text file {txt_path}: {e}")
            break
    return ""

def extract_text(file_path):
    """
    Helper function to dispatch to appropriate parser based on file extension.
    """
    _, ext = os.path.splitext(file_path.lower())
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        # Fallback to plain text read if extension is unrecognized but it's readable
        return extract_text_from_txt(file_path)

def clean_text(text):
    """
    Normalizes the text by:
    - Converting to lowercase
    - Replacing punctuation and special symbols with spaces
    - Collapsing multiple whitespaces into a single space
    - Removing custom list of common stopwords
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Replace non-alphabetic/non-numeric characters with spaces
    text = re.sub(r'[^a-z0-9\s+-]', ' ', text)
    
    # Tokenize by spaces
    words = text.split()
    
    # Filter out stopwords
    filtered_words = [word for word in words if word not in STOPWORDS]
    
    # Reassemble text
    return " ".join(filtered_words)
