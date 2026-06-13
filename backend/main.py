import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import tensorflow as tf
from backend.parser import parse_resume
from backend.nlp_processor import extract_contact_info, extract_skills, analyze_experience_and_education
from backend.classifier import classifier, CATEGORIES
from backend.similarity import match_resume_to_jd

app = FastAPI(
    title="AI Resume Screening System",
    description="FastAPI backend for screening resumes using NLP and TensorFlow"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Trains or loads the TensorFlow model on startup."""
    print("FastAPI: Running startup tasks...")
    try:
        classifier.load_or_train()
        print("FastAPI: TensorFlow initialization complete.")
    except Exception as e:
        print(f"FastAPI: Error during TensorFlow initialization: {e}")

@app.post("/api/screen")
async def screen_resume(
    file: UploadFile = File(...),
    jd: str = Form(...)
):
    """Parses a resume, extracts features, classifies it, and matches it against a job description."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Verify file extension
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
        
    # Save the uploaded file temporarily
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Parse resume text
        print(f"FastAPI: Parsing file {file.filename}...")
        resume_text = parse_resume(temp_file_path)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file. Please ensure it is not scanned or empty.")
            
        # 2. NLP Feature Extraction
        print("FastAPI: Running NLP processor...")
        contact_info = extract_contact_info(resume_text)
        resume_skills = extract_skills(resume_text)
        exp_edu = analyze_experience_and_education(resume_text)
        
        # 3. TensorFlow Role Classification
        print("FastAPI: Running TensorFlow classifier...")
        classification_result = classifier.predict(resume_text)
        
        # 4. Job Description Match Analysis
        print("FastAPI: Running match comparison...")
        match_analysis = match_resume_to_jd(resume_text, jd)
        
        # Structure the final report response
        report = {
            "filename": file.filename,
            "parsed_char_count": len(resume_text),
            "contact_info": contact_info,
            "classification": {
                "predicted_role": classification_result["category"],
                "confidence": round(classification_result["confidence"] * 100),
                "probabilities": {k: round(v * 100) for k, v in classification_result["probabilities"].items()}
            },
            "matching": {
                "overall_score": match_analysis["overall_score"],
                "skill_score": match_analysis["skill_score"],
                "text_similarity": match_analysis["text_similarity"],
                "matching_skills": match_analysis["matching_skills"],
                "missing_skills": match_analysis["missing_skills"],
                "recommendations": match_analysis["recommendations"]
            },
            "experience_highlights": exp_edu["experience"],
            "education_highlights": exp_edu["education"]
        }
        
        return JSONResponse(content=report)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal screening error: {str(e)}")
        
    finally:
        # Clean up temp files
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error cleaning up temp directory: {e}")

@app.get("/api/status")
async def get_status():
    """Returns the backend and model initialization status."""
    return {
        "status": "healthy",
        "tensorflow_version": tf.__version__,
        "model_loaded": classifier.model is not None,
        "supported_categories": CATEGORIES
    }

# Serve Frontend static assets from the frontend directory
# Make sure frontend folder exists first
os.makedirs("frontend", exist_ok=True)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
