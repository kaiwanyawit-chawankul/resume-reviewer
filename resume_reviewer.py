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

        # Comprehensive skill keywords organized by category
        self.skill_categories = {
            # Technology and Software Development
            "technology": [
                # Programming Languages
                "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust", "swift", "kotlin",
                "scala", "perl", "r", "matlab", "fortran", "assembly", "shell", "bash", "powershell", "vba", "dart",
                # Web Development
                "html", "css", "react", "angular", "vue", "svelte", "jquery", "bootstrap", "tailwind", "sass", "less",
                "node", "express", "django", "flask", "spring", "laravel", "symfony", "rails", "asp.net", "jsp", "php",
                # Mobile Development
                "android", "ios", "react native", "flutter", "xamarin", "cordova", "ionic", "swift", "objective-c",
                # Databases
                "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "dynamodb", "cassandra", "redis", "firebase",
                "nosql", "neo4j", "graphql", "mariadb", "elasticsearch", "couchdb", "cosmosdb",
                # Cloud and Infrastructure
                "aws", "azure", "gcp", "cloud", "docker", "kubernetes", "terraform", "ansible", "jenkins", "cicd",
                "devops", "serverless", "microservices", "iaas", "paas", "saas", "cloudformation", "openshift", "openstack",
                # Data Science and AI
                "ml", "ai", "machine learning", "deep learning", "data science", "tensorflow", "pytorch", "keras", "scikit-learn",
                "pandas", "numpy", "scipy", "matplotlib", "seaborn", "tableau", "power bi", "data visualization", "statistics",
                "regression", "clustering", "classification", "nlp", "computer vision", "neural networks",
                # General Tech Skills
                "git", "github", "gitlab", "bitbucket", "agile", "scrum", "kanban", "jira", "confluence", "testing", "debugging",
                "cybersecurity", "encryption", "blockchain", "api", "rest", "soap", "json", "xml", "virtualization", "vm",
                "networking", "tcp/ip", "dns", "http", "https", "ssl", "tls", "algorithms", "data structures"
            ],

            # Healthcare and Medical
            "healthcare": [
                # Clinical Skills
                "diagnosis", "treatment", "patient care", "medication", "prescription", "clinical", "assessment", "therapy",
                "rehabilitation", "triage", "emergency", "icu", "anesthesia", "surgery", "suturing", "injection", "vaccination",
                "phlebotomy", "vital signs", "ecg", "ekg", "ultrasound", "imaging", "mri", "ct scan", "xray", "biopsy",
                "specimen collection", "lab testing", "pathology", "oncology", "neurology", "cardiology", "pediatrics",
                "geriatrics", "obstetrics", "gynecology", "orthopedics", "dermatology", "ophthalmology", "psychiatry",
                "psychology", "pharmacy", "pharmacology", "dosage calculation",
                # Medical Documentation
                "medical records", "ehr", "emr", "epic", "cerner", "meditech", "allscripts", "charting", "documentation",
                "coding", "icd", "cpt", "hipaa", "patient confidentiality", "medical terminology",
                # Healthcare Administration
                "healthcare management", "medical billing", "medical coding", "insurance", "scheduling", "patient registration",
                "medical office", "healthcare compliance", "quality improvement", "infection control", "sterilization",
                "sanitization", "bls", "acls", "pals", "first aid", "cpr", "rn", "lpn", "cna", "md", "do", "pa", "np"
            ],

            # Education and Teaching
            "education": [
                # Teaching Skills
                "curriculum development", "lesson planning", "instruction", "classroom management", "assessment", "grading",
                "student evaluation", "differentiated instruction", "special education", "iep", "504 plan", "behavior management",
                "pedagogy", "teaching methodology", "student engagement", "learning styles", "educational technology",
                "distance learning", "online teaching", "hybrid learning", "blended learning", "early childhood education",
                "elementary education", "secondary education", "higher education", "adult education", "esl", "tesol", "tefl",
                # Subject Expertise
                "mathematics", "algebra", "geometry", "calculus", "statistics", "science", "biology", "chemistry", "physics",
                "literature", "english", "writing", "grammar", "reading comprehension", "social studies", "history", "geography",
                "civics", "economics", "foreign language", "art", "music", "physical education", "computer science", "stem",
                "steam", "research methods",
                # Educational Administration
                "education administration", "school counseling", "academic advising", "educational leadership", "curriculum design",
                "instructional design", "professional development", "student affairs", "admissions", "enrollment management",
                "educational policy", "accreditation", "student assessment", "standardized testing", "data analysis",
                "educational research", "program evaluation", "grant writing", "educational technology", "lms", "canvas",
                "blackboard", "moodle", "google classroom", "student information systems", "pbis", "mtss", "rti"
            ],

            # Finance and Accounting
            "finance": [
                "accounting", "bookkeeping", "auditing", "financial analysis", "financial reporting", "budgeting", "forecasting",
                "financial planning", "investment", "portfolio management", "risk assessment", "taxation", "tax preparation",
                "tax law", "gaap", "ifrs", "financial statements", "balance sheet", "income statement", "cash flow", "accounts payable",
                "accounts receivable", "general ledger", "payroll", "cost accounting", "managerial accounting", "cpa", "cfa", "cfp",
                "banking", "lending", "credit analysis", "underwriting", "mortgage", "loan processing", "financial compliance",
                "anti-money laundering", "know your customer", "financial regulations", "quickbooks", "sap", "oracle financials",
                "excel", "vlookup", "pivot tables", "financial modeling", "valuation", "mergers and acquisitions"
            ],

            # Business and Management
            "business": [
                "management", "leadership", "supervision", "strategic planning", "business development", "business analysis",
                "project management", "pmp", "prince2", "agile", "waterfall", "operations management", "supply chain",
                "inventory management", "procurement", "vendor management", "contract negotiation", "quality management",
                "six sigma", "lean", "kaizen", "continuous improvement", "customer service", "client relations", "sales",
                "business-to-business", "business-to-consumer", "account management", "marketing", "digital marketing",
                "social media marketing", "seo", "sem", "content creation", "brand management", "market research",
                "competitive analysis", "product management", "product development", "entrepreneurship", "startups",
                "business strategy", "change management", "organizational development", "human resources", "recruitment",
                "talent acquisition", "onboarding", "performance management", "compensation", "benefits", "training",
                "employee development", "conflict resolution", "negotiations", "decision making", "problem solving"
            ],

            # Legal
            "legal": [
                "law", "legal research", "legal writing", "contract law", "contract drafting", "contract review", "litigation",
                "mediation", "arbitration", "compliance", "regulatory compliance", "corporate law", "business law", "intellectual property",
                "patent", "trademark", "copyright", "licensing", "criminal law", "civil law", "family law", "immigration law",
                "labor law", "employment law", "real estate law", "tax law", "international law", "constitutional law",
                "legal ethics", "case management", "legal documentation", "discovery", "deposition", "trial preparation",
                "legal advocacy", "legal consultation", "legal analysis", "legal advising", "jd", "esq", "paralegal",
                "legal assistance", "legal secretary", "legal billing", "legal translations", "legal services"
            ],

            # Creative and Design
            "creative": [
                "graphic design", "web design", "ui design", "ux design", "user experience", "user interface",
                "illustration", "animation", "motion graphics", "video editing", "video production", "photography",
                "photoshop", "illustrator", "indesign", "figma", "sketch", "adobe creative suite", "after effects",
                "premiere pro", "lightroom", "3d modeling", "cad", "art direction", "creative direction", "brand identity",
                "typography", "layout design", "visual design", "print design", "digital design", "responsive design",
                "content creation", "copywriting", "content writing", "technical writing", "editing", "proofreading",
                "storytelling", "scriptwriting", "storyboarding", "content strategy", "social media content", "blogging"
            ],

            # Communication and Media
            "communication": [
                "communication", "public speaking", "presentation", "public relations", "media relations", "press releases",
                "crisis communication", "corporate communication", "internal communication", "external communication",
                "interpersonal communication", "oral communication", "written communication", "active listening",
                "journalism", "reporting", "interviewing", "broadcast", "podcasting", "social media management",
                "community management", "audience engagement", "stakeholder communication", "cross-cultural communication",
                "multilingual", "translation", "interpretation", "negotiation", "persuasion", "facilitation",
                "conflict resolution", "mediation", "networking", "relationship building", "speech writing"
            ],

            # Administrative and Office
            "administrative": [
                "office management", "administrative", "clerical", "data entry", "word processing", "typing", "transcription",
                "filing", "record keeping", "document management", "calendar management", "scheduling", "appointment setting",
                "microsoft office", "word", "excel", "powerpoint", "outlook", "access", "g suite", "google docs", "google sheets",
                "google slides", "receptionist", "front desk", "customer service", "phone etiquette", "email management",
                "mail processing", "shipping", "procurement", "office supplies", "inventory control", "event planning",
                "meeting coordination", "travel arrangement", "expense reporting", "executive assistance", "virtual assistance"
            ],

            # Research and Analysis
            "research": [
                "research", "data analysis", "quantitative research", "qualitative research", "market research", "competitive analysis",
                "literature review", "systematic review", "meta-analysis", "experimental design", "hypothesis testing",
                "statistical analysis", "data collection", "survey design", "interviewing", "focus groups", "ethnography",
                "field research", "laboratory research", "clinical trials", "research ethics", "irb", "grant writing",
                "research proposal", "dissertation", "thesis", "academic writing", "peer review", "publication", "citation",
                "spss", "r", "stata", "nvivo", "atlas.ti", "research methodology", "research protocols", "longitudinal studies",
                "cross-sectional studies", "case studies", "content analysis", "discourse analysis", "thematic analysis",
                "usability testing", "user research", "research coordination", "research administration"
            ],

            # Customer Service and Retail
            "customer_service": [
                "customer service", "customer support", "client relations", "customer experience", "retail sales",
                "cashiering", "point of sale", "pos", "register", "merchandising", "inventory management", "stock control",
                "sales floor", "upselling", "cross-selling", "product knowledge", "cash handling", "banking", "opening procedures",
                "closing procedures", "customer complaints", "conflict resolution", "returns processing", "refunds",
                "store operations", "visual merchandising", "display setup", "loss prevention", "theft deterrence",
                "customer loyalty", "rewards programs", "crm", "customer relationship management", "salesforce", "zendesk",
                "helpdesk", "call center", "phone support", "email support", "live chat", "troubleshooting", "problem resolution"
            ],

            # Manufacturing and Production
            "manufacturing": [
                "manufacturing", "production", "assembly", "fabrication", "machining", "cnc", "welding", "soldering",
                "quality control", "quality assurance", "inspection", "testing", "lean manufacturing", "six sigma",
                "5s", "kaizen", "continuous improvement", "process improvement", "process control", "spc", "production planning",
                "inventory control", "supply chain", "logistics", "material handling", "warehousing", "shipping", "receiving",
                "packaging", "hazmat", "safety protocols", "osha", "preventive maintenance", "equipment maintenance",
                "machine operation", "forklift", "blueprint reading", "cad", "cam", "automation", "robotics", "plc",
                "scada", "industrial control systems"
            ],

            # General Professional Skills
            "general": [
                "teamwork", "collaboration", "team building", "team leadership", "time management", "organization",
                "multitasking", "prioritization", "decision making", "problem solving", "critical thinking", "analytical thinking",
                "attention to detail", "adaptability", "flexibility", "resilience", "work ethic", "initiative", "self-motivation",
                "reliability", "dependability", "integrity", "ethics", "confidentiality", "professionalism", "cultural sensitivity",
                "diversity awareness", "emotional intelligence", "stress management", "creative thinking", "innovation",
                "growth mindset", "continuous learning", "mentoring", "coaching", "training", "development", "budgeting",
                "goal setting", "performance metrics", "kpis", "reporting", "documentation", "cross-functional coordination",
                "stakeholder management", "resource allocation", "delegating", "workflow management", "process optimization"
            ]
        }

        # Flatten skill categories for easier searching
        self.skill_keywords = []
        for category in self.skill_categories.values():
            self.skill_keywords.extend(category)
        self.skill_keywords = list(set(self.skill_keywords))  # Remove duplicates

        # Education and experience keywords
        self.education_keywords = ['degree', 'bachelor', 'master', 'phd', 'doctorate', 'diploma', 'certificate',
                                  'bs', 'ms', 'ba', 'ma', 'mba', 'university', 'college', 'school', 'institute',
                                  'certification', 'certified', 'license', 'licensed', 'credential', 'accredited',
                                  'education', 'graduate', 'undergraduate', 'postgraduate', 'academic', 'study',
                                  'major', 'minor', 'concentration', 'specialization', 'coursework', 'gpa',
                                  'honors', 'cum laude', 'magna cum laude', 'summa cum laude', 'thesis', 'dissertation']

        self.experience_keywords = ['year', 'month', 'experience', 'work', 'employment', 'job', 'career', 'profession',
                                   'position', 'role', 'responsibility', 'duty', 'task', 'function', 'project', 'campaign',
                                   'initiative', 'achievement', 'accomplishment', 'success', 'led', 'lead', 'manage', 'managed',
                                   'supervise', 'supervised', 'direct', 'directed', 'oversee', 'oversaw', 'coordinate',
                                   'coordinated', 'develop', 'developed', 'implement', 'implemented', 'create', 'created',
                                   'design', 'designed', 'establish', 'established', 'launch', 'launched', 'build', 'built',
                                   'team', 'group', 'department', 'division', 'unit', 'organization', 'company', 'client',
                                   'customer', 'stakeholder', 'partner', 'vendor', 'contractor', 'consultation', 'collaboration',
                                   'deadline', 'target', 'goal', 'objective', 'benchmark', 'metric', 'performance', 'outcome',
                                   'result', 'impact', 'improvement', 'growth', 'increase', 'decrease', 'reduction', 'expansion']

    def preprocess_text(self, text):
        """Clean and preprocess the text data using the global function"""
        return preprocess_text(text, self.lemmatizer, self.stop_words)

    def extract_skills(self, text):
        """Extract skills from the text"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()

        # Extract individual words
        single_word_skills = [word for word in words if word in self.skill_keywords]

        # Extract multi-word skills
        multi_word_skills = []
        for skill in self.skill_keywords:
            if ' ' in skill and skill in processed_text:
                multi_word_skills.append(skill)

        # Combine all skills
        all_skills = single_word_skills + multi_word_skills

        # Remove duplicates and sort
        return sorted(list(set(all_skills)))

    def identify_skill_categories(self, skills):
        """Identify which skill categories are present in the skills list"""
        categories = {}
        for category_name, category_skills in self.skill_categories.items():
            matching_skills = [skill for skill in skills if skill in category_skills]
            if matching_skills:
                categories[category_name] = {
                    "count": len(matching_skills),
                    "skills": matching_skills
                }
        return categories

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

        # Identify skill categories
        job_categories = self.identify_skill_categories(job_skills)
        resume_categories = self.identify_skill_categories(resume_skills)
        matching_categories = self.identify_skill_categories(matching_skills)

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
            "skill_categories": {
                "job_categories": job_categories,
                "resume_categories": resume_categories,
                "matching_categories": matching_categories
            },
            "education_score": round(education_score * 100, 2),
            "experience_score": round(experience_score * 100, 2)
        }

        return result