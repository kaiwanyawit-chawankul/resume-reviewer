import re
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources during module initialization
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

def preprocess_text(text, lemmatizer=None, stop_words=None):
    """Clean and preprocess the text data"""
    # Initialize lemmatizer and stop_words if not provided
    if lemmatizer is None:
        lemmatizer = WordNetLemmatizer()

    if stop_words is None:
        stop_words = set(stopwords.words('english'))

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize
    processed_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    return ' '.join(processed_tokens)

class ResumeReviewer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()

        # Common keywords for skills, education, and experience
        self.skill_keywords = ['python', 'java', 'javascript', 'sql', 'react',
                              'angular', 'node', 'aws', 'cloud', 'docker',
                              'kubernetes', 'ml', 'ai', 'data', 'analysis',
                              'frontend', 'backend', 'fullstack', 'development',
                              'programming', 'testing', 'agile', 'scrum']

        self.education_keywords = ['degree', 'bachelor', 'master', 'phd',
                                  'bs', 'ms', 'ba', 'university', 'college',
                                  'certification', 'certified', 'license']

        self.experience_keywords = ['year', 'month', 'experience', 'work',
                                   'project', 'led', 'managed', 'developed',
                                   'implemented', 'created', 'designed', 'team',
                                   'client', 'stakeholder', 'deadline']

    def preprocess_text(self, text):
        """Clean and preprocess the text data using the global function"""
        return preprocess_text(text, self.lemmatizer, self.stop_words)

    def extract_skills(self, text):
        """Extract skills from the text"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()
        skills = [word for word in words if word in self.skill_keywords]
        return list(set(skills))  # Remove duplicates

    def calculate_similarity(self, job_desc, resume):
        """Calculate the similarity between job description and resume"""
        documents = [self.preprocess_text(job_desc), self.preprocess_text(resume)]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return similarity

    def analyze_resume(self, job_description, resume_text):
        """Analyze resume against job description"""
        # Calculate overall similarity
        similarity = self.calculate_similarity(job_description, resume_text)

        # Extract skills from both job description and resume
        job_skills = self.extract_skills(job_description)
        resume_skills = self.extract_skills(resume_text)

        # Calculate skill match percentage
        matching_skills = [skill for skill in resume_skills if skill in job_skills]
        skill_match_percentage = len(matching_skills) / len(job_skills) if job_skills else 0

        # Calculate education and experience match (simple keyword-based approach)
        education_keywords_count = sum(1 for keyword in self.education_keywords if keyword in self.preprocess_text(resume_text).split())
        experience_keywords_count = sum(1 for keyword in self.experience_keywords if keyword in self.preprocess_text(resume_text).split())

        education_score = min(1.0, education_keywords_count / 5)  # Cap at 1.0
        experience_score = min(1.0, experience_keywords_count / 10)  # Cap at 1.0

        # Calculate overall score (weighted average)
        overall_score = 0.5 * similarity + 0.3 * skill_match_percentage + 0.1 * education_score + 0.1 * experience_score

        # Format the results
        result = {
            "overall_match_score": round(overall_score * 100, 2),
            "similarity_score": round(similarity * 100, 2),
            "skill_match": {
                "percentage": round(skill_match_percentage * 100, 2),
                "matching_skills": matching_skills,
                "missing_skills": [skill for skill in job_skills if skill not in resume_skills]
            },
            "education_score": round(education_score * 100, 2),
            "experience_score": round(experience_score * 100, 2)
        }

        return result