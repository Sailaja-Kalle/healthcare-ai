import pandas as pd
import os

def load_hospital_data():
    """Load hospital data from CSV"""
    try:
        path = os.path.join("database", "hospital_data.csv")
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error loading hospital data: {e}")
        return pd.DataFrame()

def load_treatment_costs():
    """Load treatment cost data from CSV"""
    try:
        path = os.path.join("database", "treatment_costs.csv")
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error loading treatment costs: {e}")
        return pd.DataFrame()

def get_department_from_symptoms(symptoms, symptom_map):
    """Match symptoms to medical department"""
    symptoms_lower = symptoms.lower()
    for symptom, department in symptom_map.items():
        if symptom in symptoms_lower:
            return department
    return "General"

def get_severity(symptoms, severity_levels):
    """Determine severity from symptoms"""
    symptoms_lower = symptoms.lower()
    for level, keywords in severity_levels.items():
        for keyword in keywords:
            if keyword in symptoms_lower:
                return level
    return "medium"

def filter_hospitals(df, city=None, department=None, hospital_type=None):
    """Filter hospitals based on criteria"""
    filtered = df.copy()
    if city and city != "All":
        filtered = filtered[
            filtered["city"].str.lower() == city.lower()
        ]
    if department and department != "All":
        filtered = filtered[
            filtered["specialization"].str.contains(department, case=False, na=False)
        ]
    if hospital_type and hospital_type != "All":
        filtered = filtered[
            filtered["type"].str.lower() == hospital_type.lower()
        ]
    return filtered

def format_cost(min_cost, max_cost):
    """Format cost in Indian Rupees"""
    def format_number(n):
        if n >= 100000:
            return f"₹{n/100000:.1f}L"
        elif n >= 1000:
            return f"₹{n/1000:.0f}K"
        else:
            return f"₹{n}"
    return f"{format_number(min_cost)} – {format_number(max_cost)}"

def get_cities_list(df):
    """Get unique cities from hospital data"""
    if df.empty:
        return []
    return ["All"] + sorted(df["city"].unique().tolist())