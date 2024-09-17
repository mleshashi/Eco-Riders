import requests
import json

# Define your API key
api_key = "5b3ce3597851110001cf6248e4066e0c05744247a6e294bfc14e7e4a"

# Define the start and end coordinates (longitude, latitude)
start_coords = [9.999, 53.5511]  # Example: Hamburg, Germany
end_coords = [13.405, 52.52]     # Example: Berlin, Germany

# Define the endpoint and profile
url = f"https://api.openrouteservice.org/v2/directions/driving-car"

# Set up the headers for authentication
headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json'
}

# Build the request data with the coordinates
body = {
    "coordinates": [start_coords, end_coords],
    "instructions": False  # Turn off step-by-step instructions for simplicity
}

# Make the request to the API
response = requests.post(url, headers=headers, json=body)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract the distance (in meters)
    distance = data['routes'][0]['summary']['distance'] / 1000  # Convert to kilometers
    
    print(f"Distance between the two places is: {distance} km")
else:
    print(f"Error: {response.status_code}, {response.text}")
