def detect_emergency(symptoms):
    """Detect if symptoms are emergency level"""
    
    emergency_keywords = [
        "chest pain", "heart attack", "cardiac arrest",
        "brain stroke", "unconscious", "not breathing",
        "heavy bleeding", "severe bleeding", "can't breathe",
        "breathing stopped", "fits", "seizure", "poisoning",
        "snake bite", "accident", "major injury", "coma",
        "గుండె నొప్పి", "శ్వాస తీసుకోవడం కష్టం",
        "दिल का दर्द", "सांस नहीं आ रही"
    ]

    symptoms_lower = symptoms.lower()
    
    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return {
                "is_emergency": True,
                "message": "🚨 EMERGENCY DETECTED!",
                "action": "Call 108 immediately!",
                "helplines": {
                    "Ambulance": "108",
                    "Police": "100",
                    "Fire": "101",
                    "Women Helpline": "1091",
                    "Child Helpline": "1098"
                }
            }

    return {
        "is_emergency": False,
        "message": None,
        "action": None,
        "helplines": {
            "Ambulance": "108",
            "Police": "100",
            "Fire": "101",
            "Women Helpline": "1091",
            "Child Helpline": "1098"
        }
    }

def get_first_aid_tips(symptoms):
    """Get basic first aid tips based on symptoms"""
    
    first_aid = {
        "chest pain": [
            "Make patient sit or lie down comfortably",
            "Loosen tight clothing",
            "Call 108 immediately",
            "Do NOT give food or water"
        ],
        "bleeding": [
            "Apply pressure on wound with clean cloth",
            "Keep wound elevated if possible",
            "Call 108 immediately",
            "Do NOT remove cloth even if soaked"
        ],
        "breathing problem": [
            "Help patient sit upright",
            "Loosen tight clothing around neck",
            "Call 108 immediately",
            "Keep patient calm"
        ],
        "fever": [
            "Give paracetamol if available",
            "Apply cold wet cloth on forehead",
            "Give plenty of water",
            "Consult doctor if fever exceeds 103°F"
        ],
        "fracture": [
            "Do NOT move injured part",
            "Apply ice pack if available",
            "Call 108 or go to nearest hospital",
            "Keep patient calm and still"
        ]
    }

    symptoms_lower = symptoms.lower()
    for condition, tips in first_aid.items():
        if condition in symptoms_lower:
            return tips

    return [
        "Stay calm",
        "Consult a doctor immediately",
        "Call 108 if condition is severe"
    ]