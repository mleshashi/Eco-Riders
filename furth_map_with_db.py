import streamlit as st
from streamlit_folium import st_folium
import folium

# Stadium Coordinates
stadium_location = [49.493611, 10.988333]  # Latitude, Longitude


locations_within_1km = [
    {"name": "Konum 1", "coordinates": [49.494111, 10.987833]},  
    {"name": "Konum 2", "coordinates": [49.493111, 10.989333]}, 
    {"name": "Konum 3", "coordinates": [49.492611, 10.987333]}  
]

# Streamlit Titles
st.title("SPVGG GREUTHER FÜRTH Stadium and Other Locations")

# Created folium maps
m = folium.Map(location=stadium_location, zoom_start=16)

# Stick a point for the stadium
folium.Marker(
    location=stadium_location,
    popup="SPVGG GREUTHER FÜRTH Stadium",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Another location point near the 1 km
for loc in locations_within_1km:
    folium.Marker(
        location=loc["coordinates"],
        popup=loc["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Show the map with the Streamlit
st_folium(m, width=725)
