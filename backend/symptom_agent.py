from backend.groq_client import get_ai_response
import json
import re

def analyze_symptoms(name, age, gender, symptoms, duration, severity, existing_conditions, language="English"):
    """Analyze symptoms and return structured diagnosis"""

    prompt = f"""
You are an expert AI doctor assistant for India. Analyze the following patient information and provide a detailed health assessment.

Patient Information:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Symptoms: {symptoms}
- Duration: {duration}
- Severity: {severity}/10
- Existing Conditions: {existing_conditions if existing_conditions else "None"}

Respond ONLY in this exact JSON format, nothing else:
{{
    "possible_diseases": [
        {{"name": "Disease 1", "probability": "High/Medium/Low", "description": "brief description"}},
        {{"name": "Disease 2", "probability": "High/Medium/Low", "description": "brief description"}},
        {{"name": "Disease 3", "probability": "High/Medium/Low", "description": "brief description"}}
    ],
    "urgency_level": "Emergency/Visit Soon/Home Care",
    "urgency_reason": "reason in one sentence",
    "doctor_to_visit": "Specialist type e.g. General Physician, Cardiologist",
    "home_remedies": [
        "remedy 1",
        "remedy 2",
        "remedy 3",
        "remedy 4"
    ],
    "warning_signs": [
        "sign 1 that needs immediate attention",
        "sign 2 that needs immediate attention"
    ],
    "general_advice": "2-3 sentences of general health advice"
}}

Important:
- Be accurate and helpful
- Consider Indian healthcare context
- If severity is 8+ or symptoms are critical, set urgency to Emergency
- Respond in {language} language for text fields
"""

    try:
        response = get_ai_response(prompt, max_tokens=1500)
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return True, result
        else:
            return False, "Could not parse AI response. Please try again."
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_urgency_color(urgency):
    colors = {
        "Emergency": "🔴",
        "Visit Soon": "🟡",
        "Home Care": "🟢"
    }
    return colors.get(urgency, "🟡")


def get_probability_color(probability):
    colors = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢"
    }
    return colors.get(probability, "🟡")