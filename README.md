# Green Fan Movement - Carpooling Web Application

## Project Overview
The **Green Fan Movement** carpooling web application encourages SPVGG GREUTHER FÜRTH fans to travel sustainably to the stadium by offering a platform for carpool matching. Developed using Streamlit, this app allows fans to register their travel details, find carpool partners, and calculate the environmental impact of their chosen transportation methods. By leveraging real-time data, AI-powered route mapping, and an innovative reward system, this application aims to reduce traffic congestion and CO₂ emissions on game days.

---

## Features

### User Registration
- Fans can register their travel information, including their **name**, **location**, **mode of transport**, and **travel date**.
- Users can specify if they are **offering** or **looking for carpool seats** and provide additional details in a description box.

### Environmental Impact Calculation
- The app calculates estimated **CO₂ emissions** based on transportation mode and distance.
- Displays the potential **CO₂ savings** when fans opt for carpooling over solo travel.

### Interactive Route Mapping
- Integrated with the **OpenRouteService API** for route mapping from user location to the stadium.
- Shows **route distance** on an interactive map using **Folium**, helping fans plan their journey efficiently.

### Reward System
- Fans earn points for choosing **sustainable travel options**, which can be redeemed for discounts and other incentives (planned as a future feature).

### Customizable UI
- Styled with **custom CSS** and includes background images and logos to align with the **Green Fan Movement** branding.

---

## Technologies Used
- **Streamlit**: For creating the web interface.
- **Pandas**: For data handling and storage.
- **Folium**: For interactive map display.
- **OpenRouteService API**: For route mapping and distance calculation.
- **Base64 Encoding**: For background image styling.

---

## Future Enhancements
- **Enhanced Reward System**: Introduce a point-based reward system to incentivize sustainable travel choices.
- **Improved Emission Calculations**: Incorporate more detailed factors for each mode of transport.
- **Email Notifications**: Send confirmation emails upon successful registration.

---

## License
This project is © 2024 by NTT DATA Business Solutions and is intended for demonstration purposes only.