# App Constants
APP_NAME = "AI Healthcare Assistant"
APP_VERSION = "1.0.0"

# Language Options
LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi"
}

# Department to Symptoms Mapping
SYMPTOM_DEPARTMENT_MAP = {
    "chest pain": "Cardiology",
    "heart pain": "Cardiology",
    "breathing problem": "Pulmonology",
    "shortness of breath": "Pulmonology",
    "asthma": "Pulmonology",
    "kidney stone": "Urology",
    "kidney pain": "Nephrology",
    "kidney failure": "Nephrology",
    "brain stroke": "Neurology",
    "headache": "Neurology",
    "brain tumor": "Neurology",
    "fracture": "Orthopedics",
    "bone pain": "Orthopedics",
    "joint pain": "Orthopedics",
    "pregnancy": "Gynecology",
    "cancer": "Oncology",
    "fever": "General",
    "typhoid": "General",
    "dengue": "General",
    "eye problem": "Ophthalmology",
    "skin disease": "Dermatology",
    "diabetes": "Endocrinology",
    "stomach pain": "Gastroenterology",
    "liver problem": "Gastroenterology",
}

# Severity Levels
SEVERITY_LEVELS = {
    "low": ["fever", "skin disease", "eye problem", "cold"],
    "medium": ["diabetes", "kidney stone", "fracture", "asthma"],
    "high": ["chest pain", "brain stroke", "heart attack", "kidney failure", "cancer"]
}

# Hospital Types
HOSPITAL_TYPES = ["All", "Government", "Private"]

# Cost Ranges
COST_RANGES = ["All", "Low", "Medium", "High"]