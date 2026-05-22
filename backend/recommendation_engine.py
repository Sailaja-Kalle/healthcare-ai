from utils.constants import SYMPTOM_DEPARTMENT_MAP, SEVERITY_LEVELS
from utils.helpers import get_department_from_symptoms, get_severity
from backend.hospital_engine import get_nearby_hospitals, get_hospitals_by_location
from backend.cost_estimator import get_treatment_cost

def analyze_symptoms(symptoms):
    """Analyze symptoms and return department and severity"""
    department = get_department_from_symptoms(symptoms, SYMPTOM_DEPARTMENT_MAP)
    severity = get_severity(symptoms, SEVERITY_LEVELS)
    return {
        "department": department,
        "severity": severity,
        "is_emergency": severity == "high"
    }

def get_recommendations(symptoms, city, hospital_type="All"):
    """Get complete hospital recommendations based on symptoms and location"""
    # Step 1 - Analyze symptoms
    analysis = analyze_symptoms(symptoms)
    department = analysis["department"]
    severity = analysis["severity"]

    # Step 2 - Get nearby hospitals
    nearby_hospitals = get_nearby_hospitals(city, department)

    # Step 3 - Get all hospitals if nearby is empty
    if nearby_hospitals.empty:
        nearby_hospitals = get_hospitals_by_location(
            city=None,
            department=department,
            hospital_type=hospital_type if hospital_type != "All" else None
        )

    # Step 4 - Filter by hospital type
    if hospital_type != "All" and not nearby_hospitals.empty:
        nearby_hospitals = nearby_hospitals[
            nearby_hospitals["type"].str.lower() == hospital_type.lower()
        ]

    # Step 5 - Get cost estimation
    cost_info = get_treatment_cost(symptoms.split()[0], hospital_type)

    return {
        "symptoms": symptoms,
        "department": department,
        "severity": severity,
        "is_emergency": severity == "high",
        "hospitals": nearby_hospitals,
        "cost_info": cost_info,
        "city": city
    }

def get_emergency_advice(symptoms):
    """Get emergency advice for severe symptoms"""
    high_symptoms = [
        "chest pain", "heart attack", "brain stroke",
        "breathing problem", "unconscious", "bleeding"
    ]
    symptoms_lower = symptoms.lower()
    for s in high_symptoms:
        if s in symptoms_lower:
            return {
                "is_emergency": True,
                "advice": "⚠️ This is an emergency! Please call 108 immediately!",
                "helpline": "108"
            }
    return {
        "is_emergency": False,
        "advice": "Please consult a doctor soon.",
        "helpline": None
    }