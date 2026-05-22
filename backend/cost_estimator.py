import pandas as pd
from utils.helpers import load_treatment_costs, format_cost

def get_treatment_cost(disease, hospital_type="All"):
    """Get treatment cost estimation for a disease"""
    df = load_treatment_costs()
    if df.empty:
        return None

    # Search for disease in database
    result = df[df["disease"].str.lower().str.contains(disease.lower(), na=False)]

    if result.empty:
        return None

    row = result.iloc[0]

    if hospital_type == "Government":
        min_cost = row["government_min"]
        max_cost = row["government_max"]
    elif hospital_type == "Private":
        min_cost = row["min_cost"]
        max_cost = row["max_cost"]
    else:
        # Show both
        min_cost = row["government_min"]
        max_cost = row["max_cost"]

    return {
        "disease": row["disease"],
        "department": row["department"],
        "min_cost": min_cost,
        "max_cost": max_cost,
        "formatted_cost": format_cost(min_cost, max_cost),
        "government_cost": format_cost(row["government_min"], row["government_max"]),
        "private_cost": format_cost(row["min_cost"], row["max_cost"]),
        "duration_days": row["duration_days"]
    }

def get_cost_by_department(department):
    """Get all treatment costs for a department"""
    df = load_treatment_costs()
    if df.empty:
        return pd.DataFrame()
    return df[df["department"].str.lower() == department.lower()]

def estimate_total_cost(disease, hospital_type, include_tests=True):
    """Estimate total cost including tests"""
    base_cost = get_treatment_cost(disease, hospital_type)
    if not base_cost:
        return None

    # Add approximate test costs
    test_costs = {
        "Government": {"min": 500, "max": 3000},
        "Private": {"min": 2000, "max": 15000},
        "All": {"min": 500, "max": 15000}
    }

    test = test_costs.get(hospital_type, test_costs["All"])

    total_min = base_cost["min_cost"] + (test["min"] if include_tests else 0)
    total_max = base_cost["max_cost"] + (test["max"] if include_tests else 0)

    return {
        "disease": base_cost["disease"],
        "department": base_cost["department"],
        "base_cost": base_cost["formatted_cost"],
        "test_cost": format_cost(test["min"], test["max"]),
        "total_cost": format_cost(total_min, total_max),
        "government_cost": base_cost["government_cost"],
        "private_cost": base_cost["private_cost"],
        "duration_days": base_cost["duration_days"]
    }