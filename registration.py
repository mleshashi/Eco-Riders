import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
import folium
import openrouteservice
import base64

# Initialize the OpenRouteService client with your API key
client = openrouteservice.Client(key='5b3ce3597851110001cf6248e1346f2a8cea4749bc4a86ac03b441ec')  # Replace with your actual ORS API key

# Path to the CSV file
CSV_FILE = "dataset/fan_data2.csv"

# Load existing data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to read and encode an image file as base64
def get_base64_image(image_file):
    with open(image_file, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Inject custom CSS for background image using base64 encoding
def add_background_image(image_file):
    base64_image = get_base64_image(image_file)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            padding-top: 100px; /* Adds space at the top */
        }}
        .main {{
            background-color: rgba(255, 255, 255, 0.2); /* Adds a white overlay with opacity */
            padding: 20px;
            border-radius: 10px;
        }}
        h1 {{
            color: white;
            font-weight: bold;
            font-size: 2rem; /* Adjust font size */
            line-height: 1.2; /* Adjust line height */
            display: flex;
            justify-content: center; /* Centers the text horizontally */
            width: 100%; /* Ensures the title spans the full width */
        }}
        .stTextInput > label, .stNumberInput > label, .stSelectbox > label, 
        .stDateInput > label, .stTextArea > label {{
            color: white !important;
            font-weight: bold !important;
        }}
        .stTextInput, .stNumberInput, .stSelectbox, .stDateInput, .stTextArea {{
            margin-bottom: 1px; /* Reduce space between elements */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add background image (replace 'path/to/your/image.png' with the actual path to your image)
add_background_image('dataset/cover.png')

# Save updated data to the CSV file
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# Display the form for new user registration
def display_registration_form(data):
    # Title with Logo
    col1, col2 = st.columns([1, 4])  # Use two columns, one for the logo and one for the text
    with col1:
        st.image('dataset/logo.png', width=100)  # Add your logo file path and adjust width if necessary
    with col2:
        st.markdown("<h2 style='color:white; text-align:left; font-weight: bold;'>Herzlichen Glückwunsch! Bist du bereit für den Spieltag?</h2>", unsafe_allow_html=True)

    # Second Title
    st.title("🚗 Fahr mit uns, um den Planeten 🌍 zu retten.")

    # Create a centered layout using columns
    col1, col2 = st.columns(2)
    
    # Line 1: First Name and Last Name
    with col1:
        first_name = st.text_input("First Name", help="Enter your first name")
    with col2:
        last_name = st.text_input("Last Name", help="Enter your last name")

    # Line 2: Gender, Age, and Travel Date
    col3, col4, col5 = st.columns(3)
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], help="Select your gender")
    with col4:
        age = st.number_input("Age", min_value=0, help="Enter your age")
    with col5:
        travel_date = st.date_input("Travel Date", value=datetime.now(), help="Select your travel date")

    # Line 3: City, Street, and Post Code
    col6, col7, col8 = st.columns(3)
    with col6:
        city = st.text_input("City", help="Enter your city")
    with col7:
        area = st.text_input("Street", help="Enter your street or area")
    with col8:
        post_code = st.text_input("Post Code", help="Enter your post code")

    # Line 4: Mode of Transport, Provider/User, Offer Vehicle
    col9, col10, col11 = st.columns(3)
    with col9:
        mode_of_transport = st.selectbox("Mode of Transport", ["Car", "Train", "Bus"], help="Select your mode of transport")
    with col10:
        provider_user = st.selectbox("Provider/User", ["Provider", "User", "-"], help="Are you offering or looking for transport?")
    with col11:
        offer_vehicle = st.selectbox("Offer Vehicle", ["Yes", "No", "-"], help="Do you offer a vehicle?")

    # Row for seats, short description, and submit button
    col12, col13 = st.columns([2, 5])  # Seats column is shorter, Description column is wider
    with col12:
        seats = st.number_input("Seats Provided/Needed", min_value=0, help="Specify the number of seats available or needed", max_value=50)
        
        # Place the submit button below the seats input
        submit_button = st.button("🚀 Submit Registration")  # This button will now appear below the "Seats Provided/Needed" field

    with col13:
        short_description = st.text_area("Short Description", help="Provide any additional details", height=50, max_chars=500)

    # Handle form submission after rendering
    if submit_button:
        # Create a new entry as a DataFrame
        new_entry = pd.DataFrame({
            "ID": [len(data) + 1],
            "First Name": [first_name],
            "Last Name": [last_name],
            "Gender": [gender],
            "Area": [area],
            "City": [city],
            "Post Code": [post_code],
            "Distance (km)": [0],  # Default value since it's not used in form
            "Age": [age],
            "Travel Date": [travel_date],
            "Mode of Transport": [mode_of_transport],
            "Provider/User": [provider_user],
            "Offer Vehicle": [offer_vehicle],
            "Seats Provided/Needed": [seats],
            "Lon": [0],  # Default value since it's not used in form
            "Lat": [0],  # Default value since it's not used in form
            "Short Description": [short_description]
        })

        # Append the new entry to the existing data using pd.concat
        updated_data = pd.concat([data, new_entry], ignore_index=True)

        # Save the updated data
        save_data(updated_data, CSV_FILE)

        st.success(f"🎉 {first_name} {last_name} has been registered successfully!")

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

            # Display the route distance above the map in white font
            st.markdown(f"<p style='color:white; font-size:18px; font-weight:bold;'>The total length of the route along the road is {route_distance_km:.2f} Kms.</p>", unsafe_allow_html=True)

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
            st_folium(m, width=725, height=500)  # height parametresi ile haritanın yüksekliğini sınırlayın
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
