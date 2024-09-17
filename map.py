import streamlit as st
from streamlit_folium import st_folium
import folium

# SPVGG GREUTHER FÜRTH stadyumunun koordinatları
stadium_location = [49.493611, 10.988333]  # (Enlem, Boylam)

# Streamlit başlığı
st.title("SPVGG GREUTHER FÜRTH Stadium")

# Folium haritasını oluşturun
m = folium.Map(location=stadium_location, zoom_start=15)

# Stadyum konumuna bir işaretçi (marker) ekleyin
folium.Marker(
    location=stadium_location,
    popup="SPVGG GREUTHER FÜRTH Stadium",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(m)

# Folium haritasını Streamlit ile gösterin
st_folium(m, width=725)
