# -*- coding: utf-8 -*-
import os
import subprocess
import sys

# ---------------------------------------------------------
# 1. FORCE INSTALL MULTIPART (FastAPI se pehle hona chahiye)
# ---------------------------------------------------------
try:
    import multipart
except ImportError:
    print("Installing python-multipart...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-multipart"])

# ---------------------------------------------------------
# 2. STANDARD IMPORTS
# ---------------------------------------------------------
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importing your custom logic modules
from resume_parser import extract_text, extract_skills
from quiz_engine import generate_quiz
from coding import generate_coding_challenges

app = FastAPI(title="Skill Measure AI Backend")

# ---------------------------------------------------------
# 3. CORS CONFIGURATION
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 4. ROUTES
# ---------------------------------------------------------

@app.get("/")
def home():
    return {"msg": "Python AI Server Running 🤖", "status": "online"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    temp_path = None
    skills_found = []
    quiz_data = []
    coding_data = []
    
    try:
        import tempfile
        import traceback
        
        # 1. Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            contents = await file.read()
            temp_file.write(contents)
            temp_file.flush()
        
        print(f"File saved to: {temp_path}")

        # 2. Process the file using your logic
        try:
            full_text = extract_text(temp_path)
            print(f"Extracted text length: {len(full_text) if full_text else 0}")
            
            skills_found = extract_skills(full_text)
            print(f"Skills found: {skills_found}")
            
            if skills_found:
                quiz_data = generate_quiz(skills_found)
                coding_data = generate_coding_challenges(skills_found)
            else:
                print("No skills found, using empty data")
            
        except Exception as process_error:
            print(f"Error processing file: {str(process_error)}")
            traceback.print_exc()
            raise

        # 3. Cleanup: Delete the temp file after processing
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temp file: {cleanup_error}")

        return {
            "status": "success",
            "skills_found": skills_found,
            "quiz": quiz_data,
            "coding_challenges": coding_data
        }

    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Server Error: {error_detail}")
        return {
            "status": "error",
            "message": str(e),
            "skills_found": skills_found,
            "quiz": quiz_data,
            "coding_challenges": coding_data
        }

# ---------------------------------------------------------
# 5. SERVER STARTUP (Render Optimized)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Render automatically assigns a PORT environment variable
    port = int(os.environ.get("PORT", 8003))
    print(f"Starting Python AI Server on port {port}...")
    # host="0.0.0.0" is required for external access on Render
    uvicorn.run(app, host="0.0.0.0", port=port)