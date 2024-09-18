import pandas as pd
import streamlit as st
import base64

# Path to the CSV file
CSV_FILE = "dataset/CO2_fanData.csv"

# Load existing data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to read and encode an image file as base64
def get_base64_image(image_file):
    with open(image_file, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

# Inject custom CSS for background image and white font using base64 encoding
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
        .custom-font {{
            color: white;
            font-size: 18px;
            font-weight: bold;
        }}
        .custom-success {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            background-color: rgba(0, 255, 0, 0.2);
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add background image (replace 'dataset/cover.png' with the actual path to your image)
add_background_image('dataset/cover.png')

# Function to display the information in a structured way with white font and a "Book Now" button
def display_provider_info(person):
    # Display the structured information
    st.markdown(f"<div class='custom-font'>Name: {person['First Name']} {person['Last Name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-font'>Address: {person['Area']}, {person['City']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-font'>Distance: {person['Distance (km)']} km</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-font'>Provided Seats: {person['Provided Seats']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-font'>Needed Seats: {person['Needed Seats']}</div>", unsafe_allow_html=True)

    # Check if 'Price' column exists before displaying it
    if 'Price' in person:
        st.markdown(f"<div class='custom-font'>Price: {person['Price']} EUR</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='custom-font'>Price: Not available</div>", unsafe_allow_html=True)

    # Add a "Book Now" button for each person
    if st.button(f"Book Now - {person['First Name']} {person['Last Name']}"):
        st.markdown(
            f"<div class='custom-success'>Thank you!! Booking confirmed for {person['First Name']} {person['Last Name']} and you have saved 1.2 Kg of CO2 emission!</div>", 
            unsafe_allow_html=True
        )
    
    st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line between each person

# Function to show provider details for the specified users
def show_selected_providers():
    # Load the data from the predefined CSV file
    df = load_data(CSV_FILE)

    # Filter for the specific users (Jonas Müller, Lisa Schmidt, Max Fischer)
    selected_names = ['Michael Hoffmann']
    df['full_name'] = df['First Name'] + ' ' + df['Last Name']
    
    # Filter the DataFrame to include only the selected users
    filtered_df = df[df['full_name'].isin(selected_names)]
    
    # Display the information for the selected users
    for _, person in filtered_df.iterrows():
        display_provider_info(person)

# Call the function to display the selected provider details
show_selected_providers()
