import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Path to the CSV file
CSV_FILE = "dataset/fan_data.csv"

# Load existing data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "ID", "First Name", "Last Name", "Gender", "Area", "City", "Post Code", "Distance (km)", 
            "Age", "Travel Date", "Mode of Transport", "Provider/User", 
            "Offer Vehicle", "Seats Provided/Needed", "Lon", "Lat", "Short Description"
        ])

# Save updated data to the CSV file
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

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

# Display the form for new user registration
def display_registration_form(data):
    st.title("🚗 Fan Registration Page")

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

# Load data from CSV
data = load_data(CSV_FILE)

# Add background image (replace 'path/to/your/image.png' with the actual path to your image)
add_background_image('dataset/cover.png')

# Display the registration form on the screen
display_registration_form(data)