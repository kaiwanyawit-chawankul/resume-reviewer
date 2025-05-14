# Resume Review API

A FastAPI-based web API for analyzing and scoring resumes against job descriptions.

## Features

- Analyzes resumes against job descriptions
- Calculates overall match score
- Identifies matching and missing skills
- Provides recommendations for improvement
- Supports both JSON and plain text inputs
- Dockerized for easy deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd resume-review-api
```

2. Build and start the Docker container:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

## API Endpoints

### 1. Status Check

- **URL**: `/`
- **Method**: `GET`
- **Response**: Welcome message with link to documentation

### 2. Analyze Resume (JSON)

- **URL**: `/analyze`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "job_description": "Your job description text",
    "resume": "Your resume text"
  }
  ```
- **Response**: Analysis result with scores and recommendations

### 3. Analyze Resume (Plain Text)

- **URL**: `/analyze_text`
- **Method**: `POST`
- **Content-Type**: `text/plain`
- **Request Body**:
  ```
  Your job description text
  ---RESUME---
  Your resume text
  ```
- **Response**: Analysis result with scores and recommendations

## Example Usage

### Using curl with JSON:

```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{
        "job_description": "We are looking for a Python developer with experience in Flask, Django, and SQL. Knowledge of AWS and Docker is a plus.",
        "resume": "Experienced software developer with 5 years of Python programming. Built web applications using Flask and Django. Familiar with PostgreSQL and MySQL. Experience with cloud deployment on AWS."
     }'
```

### Using curl with Plain Text:

```bash
curl -X POST "http://localhost:8000/analyze_text" \
     -H "Content-Type: text/plain" \
     --data-binary @- << EOF
We are looking for a Python developer with experience in Flask, Django, and SQL. Knowledge of AWS and Docker is a plus.
---RESUME---
Experienced software developer with 5 years of Python programming. Built web applications using Flask and Django. Familiar with PostgreSQL and MySQL. Experience with cloud deployment on AWS.
EOF
```

## Using the Interactive API Documentation

Once the API is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These interfaces allow you to:
- Read detailed API documentation
- Try out API endpoints directly from your browser
- View request and response schemas

## License

This project is licensed under the MIT License - see the LICENSE file for details.
