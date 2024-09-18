import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
import folium
import openrouteservice

# Initialize the OpenRouteService client with your API key
client = openrouteservice.Client(key='5b3ce3597851110001cf6248e1346f2a8cea4749bc4a86ac03b441ec')  # Replace with your actual ORS API key

# Path to the CSV file
CSV_FILE = "dataset/fan_data2.csv"

# Load existing data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "ID", "First Name", "Last Name", "Gender", "Area", "City", "Distance (km)", 
            "Age", "Travel Date", "Mode of Transport", "Provider/User", 
            "Offer Vehicle", "Seats Provided/Needed", "Lon", "Lat", "Short Description"
        ])

# Save updated data to the CSV file
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# Display the form for new user registration
def display_registration_form(data):
    st.title("Fan Registration Page")

    # Collect user input
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    area = st.text_input("Street")
    city = st.text_input("City")
    age = st.number_input("Age", min_value=18)
    travel_date = st.date_input("Travel Date", value=datetime.now())
    mode_of_transport = st.selectbox("Mode of Transport", ["Car", "Bus"])
    if mode_of_transport == 'Car':
        provider_user = st.selectbox("Provider/User", ["Provider", "User"])
        if provider_user == 'Provider':
            needed_seats = [0]
            provided_seats = st.number_input("Seats Provided", min_value=0)
        else:
            provided_seats = [0]
            needed_seats = st.number_input("Seats Needed", min_value=0)
    else:
        provider_user = [0]
        provided_seats = [0]
        needed_seats = st.number_input("Seats Needed", min_value=0)
    short_description = st.text_area("Short Description")

    # Button to submit the form
    if st.button("Register"):
        # Create a new entry as a DataFrame
        new_entry = pd.DataFrame({
            "ID": [len(data) + 1],
            "First Name": [first_name],
            "Last Name": [last_name],
            "Gender": [gender],
            "Area": [area],
            "City": [city],
            "Distance (km)": [0],  # Default value since it's not used in form
            "Age": [age],
            "Travel Date": [travel_date],
            "Mode of Transport": [mode_of_transport],
            "Provider/User": [provider_user],
            "Offer Vehicle": [0],
            "Provided Seats": [provided_seats],
            "Needed Seats": [needed_seats],
            "Lon": [0],  # Default value since it's not used in form
            "Lat": [0],  # Default value since it's not used in form
            "Short Description": [short_description]
        })

        # Append the new entry to the existing data using pd.concat
        updated_data = pd.concat([data, new_entry], ignore_index=True)

        # Save the updated data
        save_data(updated_data, CSV_FILE)

        st.success(f"{first_name} {last_name} has been registered successfully!")

        # Set session state to indicate that the user has registered
        st.session_state['registered'] = True
        st.session_state['area'] = area
        st.session_state['city'] = city

    # If registration is successful, show the "Open Route Map" button
    if st.session_state.get('registered'):
        if st.button("Open Route Map"):
            # Set session state to show the map
            st.session_state['show_map'] = True

# Function to display the route map
def display_route_map(area, city):
    # Geocode the user's address to get coordinates
    user_location = f"{area}, {city}"
    try:
        geocode_result = client.pelias_search(text=user_location)
        if geocode_result and geocode_result['features']:
            start_coords = geocode_result['features'][0]['geometry']['coordinates']  # [lon, lat]
            end_coords = [10.9881, 49.4772]  # SPVGG GREUTHER FÜRTH stadium coordinates [lon, lat]

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
        else:
            st.error("Could not find coordinates for the address. Please enter a valid address.")
    except Exception as e:
        st.error(f"Geocoding error: {e}")

# Load data from CSV
data = load_data(CSV_FILE)

# Display the registration form on the screen
display_registration_form(data)

# If the map should be shown, call the function to display the route map
if st.session_state.get('show_map'):
    display_route_map(st.session_state['area'], st.session_state['city'])
