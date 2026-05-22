import folium
from streamlit_folium import st_folium
import streamlit as st

def render_hospital_map(hospitals_df, city):
    if hospitals_df is None or hospitals_df.empty:
        st.warning("No hospitals to show on map.")
        return

    map_df = hospitals_df.dropna(subset=["latitude", "longitude"])
    if map_df.empty:
        st.warning("No location data available for these hospitals.")
        return

    center_lat = map_df["latitude"].mean()
    center_lon = map_df["longitude"].mean()

    # Force India bounds
    center_lat = map_df["latitude"].mean()
    center_lon = map_df["longitude"].mean()

    # Validate coordinates are in India range
    if not (6 <= center_lat <= 37 and 68 <= center_lon <= 97):
        center_lat = 17.3850  # Default Hyderabad
        center_lon = 78.4867

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="OpenStreetMap",
        min_zoom=5,
        max_zoom=18
    )
    # Force fit to India
    m.fit_bounds([[6, 68], [37, 97]])

    type_colors = {
        "Government": "green",
        "Private": "red",
    }

    for _, row in map_df.iterrows():
        color = type_colors.get(row.get("type", "Private"), "blue")

        popup_html = f"""
        <div style="width:200px">
            <b>🏥 {row['hospital_name']}</b><br>
            <b>Type:</b> {row.get('type','N/A')}<br>
            <b>Specialization:</b> {row.get('specialization','N/A')}<br>
            <b>Cost:</b> {row.get('cost_range','N/A')}<br>
            <b>Phone:</b> {row.get('phone','N/A')}<br>
            <b>Address:</b> {row.get('address','N/A')}
        </div>
        """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=row["hospital_name"],
            icon=folium.Icon(color=color, icon="plus-sign", prefix="glyphicon")
        ).add_to(m)

    st.markdown("🟢 **Green** = Government &nbsp;&nbsp; 🔴 **Red** = Private")
    st_folium(m, width=900, height=450, returned_objects=[])