from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import json

# Import the ResumeReviewer from our original code
from resume_reviewer import ResumeReviewer, preprocess_text

app = FastAPI(
    title="Resume Review API",
    description="API for analyzing resumes against job descriptions",
    version="1.0.0"
)

# Initialize the reviewer at startup
reviewer = ResumeReviewer()

class ResumeInput(BaseModel):
    job_description: str
    resume: str

class SkillMatch(BaseModel):
    percentage: float
    matching_skills: List[str]
    missing_skills: List[str]

class ResumeResult(BaseModel):
    overall_match_score: float
    similarity_score: float
    skill_match: SkillMatch
    education_score: float
    experience_score: float
    recommendations: List[str]

@app.get("/")
async def root():
    return {"message": "Welcome to Resume Review API. Use /docs for API documentation."}

@app.post("/analyze", response_model=ResumeResult)
async def analyze_resume(input_data: ResumeInput):
    """
    Analyze a resume against a job description
    """
    if not input_data.job_description or not input_data.resume:
        raise HTTPException(status_code=400, detail="Both job description and resume are required")

    # Analyze the resume using our reviewer
    result = reviewer.analyze_resume(input_data.job_description, input_data.resume)

    # Add recommendations
    recommendations = []
    if result['overall_match_score'] < 60:
        recommendations = [
            "Your resume needs significant improvement to match this job description.",
            "Focus on acquiring the missing skills listed above."
        ]
    elif result['overall_match_score'] < 80:
        recommendations = [
            "Your resume is a moderate match for this position.",
            "Consider highlighting your relevant experience more prominently.",
            "Try to incorporate more keywords from the job description."
        ]
    else:
        recommendations = [
            "Your resume is a strong match for this position!",
            "Make sure your resume is well-formatted and error-free.",
            "Prepare to discuss your experience with the matching skills in interviews."
        ]

    result['recommendations'] = recommendations
    return result

@app.post("/analyze_text")
async def analyze_text(request: Request):
    """
    Analyze resume and job description from plain text with delimiter ---RESUME---
    """
    try:
        body = await request.body()
        text_data = body.decode("utf-8")

        # Parse input data
        parts = text_data.split("---RESUME---")
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="Invalid format. Use ---RESUME--- as delimiter between job description and resume.")

        job_description = parts[0].strip()
        resume_text = parts[1].strip()

        if not job_description or not resume_text:
            raise HTTPException(status_code=400, detail="Both job description and resume are required")

        # Analyze the resume using our reviewer
        result = reviewer.analyze_resume(job_description, resume_text)

        # Add recommendations
        recommendations = []
        if result['overall_match_score'] < 60:
            recommendations = [
                "Your resume needs significant improvement to match this job description.",
                "Focus on acquiring the missing skills listed above."
            ]
        elif result['overall_match_score'] < 80:
            recommendations = [
                "Your resume is a moderate match for this position.",
                "Consider highlighting your relevant experience more prominently.",
                "Try to incorporate more keywords from the job description."
            ]
        else:
            recommendations = [
                "Your resume is a strong match for this position!",
                "Make sure your resume is well-formatted and error-free.",
                "Prepare to discuss your experience with the matching skills in interviews."
            ]

        result['recommendations'] = recommendations
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)