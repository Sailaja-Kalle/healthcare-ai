import pandas as pd
from utils.helpers import load_hospital_data, filter_hospitals, get_cities_list
from utils.constants import SYMPTOM_DEPARTMENT_MAP

def get_hospitals_by_location(city, department=None, hospital_type=None):
    """Get hospitals based on location and filters"""
    df = load_hospital_data()
    if df.empty:
        return pd.DataFrame()
    filtered = filter_hospitals(df, city, department, hospital_type)
    return filtered

def get_all_hospitals():
    """Get all hospitals"""
    return load_hospital_data()

def get_hospital_details(hospital_name):
    """Get specific hospital details"""
    df = load_hospital_data()
    if df.empty:
        return None
    result = df[df["hospital_name"].str.lower() == hospital_name.lower()]
    if result.empty:
        return None
    return result.iloc[0].to_dict()

def get_nearby_hospitals(city, department=None):
    """Get nearby hospitals for a city"""
    df = load_hospital_data()
    if df.empty:
        return pd.DataFrame()

    # First try exact city match
    nearby = filter_hospitals(df, city, department)

    # If no results, get all hospitals in same state
    if nearby.empty:
        city_data = df[df["city"].str.lower() == city.lower()]
        if not city_data.empty:
            state = city_data.iloc[0]["state"]
            nearby = df[df["state"] == state]

    return nearby

def get_available_cities():
    """Get list of all available cities"""
    df = load_hospital_data()
    return get_cities_list(df)

def search_hospitals_by_specialization(specialization):
    """Search hospitals by specialization"""
    df = load_hospital_data()
    if df.empty:
        return pd.DataFrame()
    return df[
        df["specialization"].str.contains(specialization, case=False, na=False)
    ]