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


def extract_name(text: str) -> str:
    """
    Extract student name from resume text.
    Heuristic: Look for the first line that looks like a name (short, title case).
    """
    lines = text.split('\n')
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if line and 2 <= len(line.split()) <= 5:  # Assume name has 2-5 words
            # Check if mostly title case
            words = line.split()
            if all(word[0].isupper() for word in words if word):
                return line
    return "Unknown Student"
