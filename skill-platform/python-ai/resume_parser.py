# -*- coding: utf-8 -*-
# ============================================
# RESUME PARSER (Render Safe Version)
# OCR + PyMuPDF DISABLED for cloud deployment
# ============================================

import re
import os

# ⚠️ Disabled libraries (NOT supported on Render Free tier)
# import fitz
# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_path
# os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR'

# --------------------------------------------
# SIMPLE TEXT EXTRACTION (NO OCR)
# --------------------------------------------
import pdfplumber

def extract_text(pdf_path: str) -> str:
    try:
        print(f"📂 Extracting via pdfplumber: {pdf_path}")

        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

        print(f"✅ Extracted {len(full_text)} characters")
        return full_text

    except Exception as e:
        print("❌ PDF extraction failed:", e)
        return ""




# --------------------------------------------
# SMART SKILL EXTRACTOR
# --------------------------------------------

SKILLS_DB = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "rust", "kotlin", "swift",
    "php", "ruby", "scala", "r", "matlab", "perl", "shell", "bash",

    # Web Technologies
    "html", "css", "sass", "less", "bootstrap", "tailwind",
    "react", "vue", "angular", "next.js", "nuxt", "svelte",
    "node", "node.js", "express", "nestjs", "fastapi", "django", "flask", "spring", "laravel",
    "rest api", "graphql", "websocket",

    # Databases
    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "cassandra", "elasticsearch",
    "oracle", "sqlite", "firebase", "dynamodb", "neo4j",

    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "jenkins", "gitlab ci",
    "github actions", "terraform", "ansible", "git", "github", "gitlab",

    # Mobile
    "android", "ios", "react native", "flutter", "xamarin", "ionic",

    # Data Science & AI
    "machine learning", "ml", "deep learning", "artificial intelligence", "ai", "data science",
    "data analysis", "pandas", "numpy", "tensorflow", "pytorch", "keras", "scikit-learn",
    "opencv", "nlp", "natural language processing", "computer vision",

    # Other Technologies
    "linux", "unix", "windows", "networking", "cybersecurity", "blockchain",
    "microservices", "agile", "scrum", "devops", "ci/cd", "api", "json", "xml"
]

# Mapping for skill normalization
SKILL_MAPPING = {
    "python": "Python",
    "java": "Java",
    "c": "C",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Machine Learning",
    "artificial intelligence": "Machine Learning",
    "ai": "Machine Learning",
    "data science": "Machine Learning",
    "javascript": "JavaScript",
    "react": "React",
    "node": "Node.js",
    "node.js": "Node.js",
    "express": "Express",
    "django": "Django",
    "flask": "Flask",
    "sql": "SQL",
    "mongodb": "MongoDB",
    "aws": "AWS",
    "docker": "Docker",
    "git": "Git",
    "android": "Android",
    "flutter": "Flutter",
    "linux": "Linux",
    "networking": "Networking"
}


def extract_skills(text: str):
    """
    Scan resume text and detect known skills.
    """
    if not text or len(text.strip()) < 10:
        print("⚠️ Text too short for skill extraction")
        return []

    text_lower = text.lower()

    # Normalize text (remove punctuation)
    text_normalized = re.sub(r"[^\w\s]", " ", text_lower)
    text_normalized = re.sub(r"\s+", " ", text_normalized)

    print(f"🔍 Searching skills in {len(text)} characters")

    found = set()

    # Direct skill scan
    for skill in SKILLS_DB:
        raw = skill.lower()
        norm = re.sub(r"[^\w\s]", " ", raw)
        norm = re.sub(r"\s+", " ", norm).strip()

        if not norm:
            continue

        if norm in text_normalized:
            normalized_name = SKILL_MAPPING.get(raw, skill.title())
            found.add(normalized_name)

    # Common variations
    variations = {
        "js": "JavaScript",
        "reactjs": "React",
        "nodejs": "Node.js",
        "postgres": "PostgreSQL",
        "ml": "Machine Learning",
        "ai": "Machine Learning",
        "amazon web services": "AWS",
        "gcp": "GCP",
        "rest": "REST API",
        "html5": "HTML",
        "css3": "CSS",
    }

    for key, value in variations.items():
        var_norm = re.sub(r"[^\w\s]", " ", key.lower())
        var_norm = re.sub(r"\s+", " ", var_norm).strip()
        if var_norm and var_norm in text_normalized:
            found.add(value)

    result = sorted(found)
    print(f"✅ Skills detected ({len(result)}): {result}")

    return result
