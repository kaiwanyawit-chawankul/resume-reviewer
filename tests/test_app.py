import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_analyze_text_endpoint():
    # Test data
    test_input = """We are looking for a Python developer with experience in Flask, Django, and SQL.
---RESUME---
Experienced software developer with 5 years of Python programming. Built web applications using Flask."""

    response = client.post(
        "/analyze_text",
        content=test_input
    )

    assert response.status_code == 200
    result = response.json()

    # Check response structure
    assert "overall_match_score" in result
    assert "similarity_score" in result
    assert "skill_match" in result
    assert "recommendations" in result
    assert isinstance(result["recommendations"], list)

def test_analyze_text_invalid_format():
    # Test with invalid format (missing delimiter)
    test_input = "This is an invalid input without delimiter"

    response = client.post(
        "/analyze_text",
        content=test_input
    )

    assert response.status_code == 400
    assert "Invalid format" in response.json()["detail"]