import pytest
from resume_reviewer import preprocess_text, ResumeReviewer

# filepath: /Users/kaiwanyawit/Repositories/homework-llm/claude/tests/test_resume_reviewer.py

@pytest.fixture
def reviewer():
    return ResumeReviewer()

def test_preprocess_text_basic():
    text = "Python Developer with 5+ years EXPERIENCE!"
    processed = preprocess_text(text)
    assert "python" in processed
    assert "developer" in processed
    assert "experience" in processed
    assert "!" not in processed
    assert "with" not in processed  # stopword removed

def test_preprocess_text_empty():
    assert preprocess_text("") == ""

def test_reviewer_skill_extraction():
    reviewer = ResumeReviewer()
    text = """
    Experienced Python developer with expertise in Django and Flask.
    Proficient in JavaScript, React, and Node.js.
    """
    skills = reviewer.extract_skills(text)
    assert "python" in skills
    assert "django" in skills
    assert "flask" in skills
    assert "javascript" in skills
    assert "react" in skills
    assert "node" in skills

def test_reviewer_similarity_calculation():
    reviewer = ResumeReviewer()
    job_desc = "Looking for a Python developer with Django experience"
    resume = "Python developer with 3 years Django experience"
    similarity = reviewer.calculate_similarity(job_desc, resume)
    assert 0 <= similarity <= 1

def test_reviewer_full_analysis():
    reviewer = ResumeReviewer()
    job_desc = "Senior Python Developer needed. Must know Django, React and SQL."
    resume = "Python developer with 5 years experience in Django and SQL."

    result = reviewer.analyze_resume(job_desc, resume)

    assert "overall_match_score" in result
    assert "similarity_score" in result
    assert "skill_match" in result
    assert isinstance(result["overall_match_score"], float)
    assert 0 <= result["overall_match_score"] <= 100
    assert "matching_skills" in result["skill_match"]
    assert "missing_skills" in result["skill_match"]

def test_reviewer_edge_cases():
    reviewer = ResumeReviewer()

    # Empty inputs
    result = reviewer.analyze_resume("", "")
    assert result["overall_match_score"] == 0

    # Non-matching content
    result = reviewer.analyze_resume(
        "Looking for a doctor with medical experience",
        "Software engineer with programming skills"
    )
    assert result["skill_match"]["matching_skills"] == []
    assert result["similarity_score"] < 50

def test_skill_categories():
    reviewer = ResumeReviewer()
    text = "Python developer with React and Node.js experience"
    skills = reviewer.extract_skills(text)
    categories = reviewer.identify_skill_categories(skills)

    assert "technology" in categories
    assert len(categories["technology"]["skills"]) > 0