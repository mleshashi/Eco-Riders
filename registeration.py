import streamlit as st
import pandas as pd
from datetime import datetime

# Path to the CSV file
CSV_FILE = "dataset/fan_data.csv"

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
    # distance = st.number_input("Distance (km)", min_value=0)
    age = st.number_input("Age", min_value=0)
    travel_date = st.date_input("Travel Date", value=datetime.now())
    mode_of_transport = st.selectbox("Mode of Transport", ["Car", "Train", "Bus"])
    provider_user = st.selectbox("Provider/User", ["Provider", "User", "-"])
    offer_vehicle = st.selectbox("Offer Vehicle", ["Yes", "No", "-"])
    seats = st.number_input("Seats Provided/Needed", min_value=0)
    #lon = st.number_input("Longitude")
    #lat = st.number_input("Latitude")
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

        st.success(f"{first_name} {last_name} has been registered successfully!")

# Load data from CSV
data = load_data(CSV_FILE)

# Display the registration form on the screen
display_registration_form(data)
