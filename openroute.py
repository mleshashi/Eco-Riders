import streamlit as st
from streamlit_folium import st_folium
import folium
import openrouteservice

# Initialize the OpenRouteService client with your API key
client = openrouteservice.Client(key='5b3ce3597851110001cf6248e1346f2a8cea4749bc4a86ac03b441ec')  # Replace with your actual ORS API key

# Corrected coordinate order: [longitude, latitude]
start_coords = [9.9730, 53.5825]  # Hamburg
end_coords = [13.4053, 52.5281]   # Berlin

# Get directions from OpenRouteService
routes = client.directions(
    coordinates=[start_coords, end_coords],
    profile='driving-car',
    format='geojson'
)

# Extract the route geometry and distance from the response
route_geom = routes['features'][0]['geometry']
route_distance = routes['features'][0]['properties']['segments'][0]['distance']

# Convert distance to kilometers
route_distance_km = route_distance / 1000  # Convert meters to kilometers

# Initialize a Folium map centered at the midpoint of start and end coordinates
m = folium.Map(location=[(start_coords[1] + end_coords[1]) / 2, (start_coords[0] + end_coords[0]) / 2], zoom_start=6)

# Add the route to the map using GeoJSON coordinates directly
folium.PolyLine(
    locations=[[coord[1], coord[0]] for coord in route_geom['coordinates']],  # Swap back to [latitude, longitude]
    tooltip='Route',
    color='blue',
    weight=5
).add_to(m)

# Display the map in Streamlit
st_folium(m, width=725)

# Ensure the text is shown after the map is displayed
st.write(f"The total length of the route along the road is {route_distance_km:.2f} Kms.")
