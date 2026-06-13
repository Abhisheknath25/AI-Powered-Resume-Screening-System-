from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.nlp_processor import extract_skills
import re

def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    """Computes cosine similarity between resume text and job description using TF-IDF."""
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
        
    try:
        # Create the Vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        # Fit and transform the texts
        tfidf = vectorizer.fit_transform([resume_text, jd_text])
        # Compute cosine similarity
        sim_matrix = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return float(sim_matrix[0][0])
    except Exception as e:
        print(f"Error computing text similarity: {e}")
        return 0.0

def match_resume_to_jd(resume_text: str, jd_text: str) -> dict:
    """Performs deep comparison between resume and job description.
    
    Calculates overall score, matching skills, missing skills, and recommendations.
    """
    # 1. Extract skills from both texts
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))
    
    # 2. Find overlap and missing
    matching_skills = list(resume_skills.intersection(jd_skills))
    missing_skills = list(jd_skills.difference(resume_skills))
    
    # 3. Calculate skill match ratio
    if len(jd_skills) > 0:
        skill_score = len(matching_skills) / len(jd_skills)
    else:
        # If no skills are defined in JD, check if resume has any technical/general skills
        skill_score = 1.0 if len(resume_skills) > 0 else 0.5
        
    # 4. Calculate overall TF-IDF similarity
    text_sim = compute_text_similarity(resume_text, jd_text)
    
    # 5. Composite score: 50% skills match + 50% text similarity
    # Scale both to 0-100. Text similarity is usually lower, so we scale it up slightly for realism.
    scaled_text_sim = min(text_sim * 1.5, 1.0) # Boost text similarity scaling slightly
    overall_score = round(((skill_score * 0.5) + (scaled_text_sim * 0.5)) * 100)
    
    # Clamp score between 0 and 100
    overall_score = max(0, min(100, overall_score))
    
    # 6. Generate Recommendations
    recommendations = []
    if len(missing_skills) > 0:
        recommendations.append(
            f"Add missing skills key to this job role: {', '.join(missing_skills[:4])}."
        )
    if len(resume_text.split()) < 150:
        recommendations.append(
            "The resume appears relatively short. Expand on your professional experience and project accomplishments."
        )
    if "education" not in resume_text.lower() and "degree" not in resume_text.lower():
        recommendations.append(
            "Consider adding an explicit 'Education' section with your degrees, major, and graduation years."
        )
    if "experience" not in resume_text.lower() and "work" not in resume_text.lower() and "history" not in resume_text.lower():
        recommendations.append(
            "Highlight your professional work history with bullet points describing key achievements using action verbs."
        )
        
    if overall_score >= 80:
        recommendations.append("Excellent match! Customize your summary paragraph slightly to align with the core company values in the JD.")
    elif overall_score >= 60:
        recommendations.append("Good match! Incorporate the top 2-3 missing skills into your projects or work experience description to boost your rating.")
    else:
        recommendations.append("Moderate match. Try aligning your resume's vocabulary and phrasing closer to the job description keywords.")
        
    return {
        "overall_score": overall_score,
        "skill_score": round(skill_score * 100),
        "text_similarity": round(text_sim * 100),
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "all_resume_skills": sorted(list(resume_skills)),
        "all_jd_skills": sorted(list(jd_skills)),
        "recommendations": recommendations
    }
