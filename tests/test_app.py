import pytest
import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_analyze_resume_endpoint():
    # Test data
    test_input = {
        "job_description": "We are looking for a Python developer with experience in Flask, Django, and SQL. Knowledge of AWS and Docker is a plus.",
        "resume": "Experienced software developer with 5 years of Python programming. Built web applications using Flask and Django. Familiar with PostgreSQL and MySQL. Experience with cloud deployment on AWS."
    }

    response = client.post(
        "/analyze_resume",
        json=test_input
    )

    assert response.status_code == 200
    result = response.json()

    # Check response structure and types
    assert "overall_match_score" in result
    assert isinstance(result["overall_match_score"], (int, float))
    assert 0 <= result["overall_match_score"] <= 100

    assert "similarity_score" in result
    assert isinstance(result["similarity_score"], (int, float))
    assert 0 <= result["similarity_score"] <= 100

    assert "skill_match" in result
    assert isinstance(result["skill_match"], dict)

    assert "recommendations" in result
    assert isinstance(result["recommendations"], list)
    assert all(isinstance(item, str) for item in result["recommendations"])

def test_analyze_resume_invalid_json():
    response = client.post(
        "/analyze_resume",
        content="Invalid JSON data"
    )
    assert response.status_code == 422

def test_analyze_resume_missing_fields():
    test_input = {
        "job_description": "Python developer role"
        # Missing resume field
    }
    response = client.post(
        "/analyze_resume",
        json=test_input
    )
    assert response.status_code == 422

def test_analyze_resume_empty_fields():
    test_input = {
        "job_description": "",
        "resume": ""
    }
    response = client.post(
        "/analyze_resume",
        json=test_input
    )
    assert response.status_code == 400
    assert "Both job description and resume are required" in response.json()["detail"]