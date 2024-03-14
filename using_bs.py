import streamlit as st
import requests
from bs4 import BeautifulSoup

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #DBAC38;
        padding: 20px 0;
        text-align: center;
    }
    .weather-info {
        font-size: 18px;
        color: #FFFFFF;
        padding: 10px 0;
    }
    .input-box {
        background-color: #49873E;
        color: #FFFFFF;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def scrape_weather(latitude, longitude):
    """
    Scrape weather data from the specified latitude and longitude.

    Parameters:
        latitude (str): Latitude of the location.
        longitude (str): Longitude of the location.

    Returns:
        tuple: A tuple containing location, temperature, condition, humidity, rainfall, and current time.
    """
    url = f"https://www.timeanddate.com/weather/@{latitude},{longitude}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing weather information
        weather_element = soup.find('div', class_='bk-focus__qlook')
        if weather_element:
            # Extracting Temperature
            temp_element = weather_element.find('div', class_='h2')
            temperature = temp_element.text.strip() if temp_element else "N/A"

            # Extracting Weather Condition
            condition_element = weather_element.find('p')
            condition = condition_element.text.strip() if condition_element else "N/A"

        else:
            temperature, condition = "N/A", "N/A"

        # Find the element containing location information
        location_element = soup.find('div', class_='bk-focus__info')
        if location_element:
            # Extracting Location
            location_info = location_element.find('table', class_='table--left')
            if location_info:
                location_rows = location_info.find_all('tr')
                for row in location_rows:
                    if 'Location' in row.text:
                        location = row.find('td').text.strip()
                        break
                else:
                    location = "N/A"
            else:
                location = "N/A"
        else:
            location = "N/A"
        
        # Extracting Humidity
        humidity_element = soup.find('th', text='Humidity:')
        if not humidity_element:
            humidity_element = soup.find('th', text='Humidity')
        if humidity_element:
            humidity = humidity_element.find_next('td').text.strip()
        else:
            humidity = "N/A"
        
        # Extracting Rainfall
        rainfall_element = soup.find('th', text='Probability of Precipitation')
        if not rainfall_element:
            rainfall_element = soup.find('th', text='Probability of Precipitation:')
        if not rainfall_element:
            rainfall_element = soup.find('th', text='Precipitation:')
        if rainfall_element:
            rainfall = rainfall_element.find_next('td').text.strip()
        else:
            rainfall = "N/A"
        
        # Extracting Current Time
        current_time_element = soup.find('td', id='wtct')
        current_time = current_time_element.text.strip() if current_time_element else "N/A"

        return location, temperature, condition, humidity, rainfall, current_time
    
    else:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Streamlit UI
st.markdown("<h1 class='main-title'>Real-Time Weather App</h1>", unsafe_allow_html=True)

# Input for latitude and longitude
latitude = st.text_input('Enter latitude:')
longitude = st.text_input('Enter longitude:')

# Function to convert input to decimal format
def convert_input(coord):
    # Remove all non-numeric characters except for the decimal point
    coord = ''.join(c for c in coord if c.isdigit() or c == '.')
    return coord

# Convert input to decimal format
latitude = convert_input(latitude)
longitude = convert_input(longitude)

if st.button('Get Weather'):
    if latitude and longitude:
        # Call the scrape_weather function
        location, temperature, condition, humidity, rainfall, current_time = scrape_weather(latitude, longitude)
        
        # Display the weather information
        st.markdown("<h2 class='weather-info'>Weather Information:</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown(f"<p class='weather-info'><b>Location:</b> {location}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='weather-info'><b>Latitude:</b> {latitude}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='weather-info'><b>Longitude:</b> {longitude}</p>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p class='weather-info'><b>Temperature:</b> {temperature}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='weather-info'><b>Weather Condition:</b> {condition}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='weather-info'><b>Humidity:</b> {humidity}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='weather-info'><b>Rainfall:</b> {rainfall}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='weather-info'><b>Current Time:</b> {current_time}</p>", unsafe_allow_html=True)
    else:
        st.warning("Please enter latitude and longitude.")
