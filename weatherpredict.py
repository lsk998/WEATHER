import streamlit as st
import requests

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import webbrowser

# Title of the app
st.title("🌍 Earth Heat App with Disaster prediction")

# Input field for location
location = st.text_input("Enter a location:")

# Function to fetch weather data
def get_weather_data(location):
    """Fetches weather data from OpenWeatherMap API."""
    api_key = "d0d8d26e14950d5578e76d6a4c369529"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={location}&appid={api_key}"
    response = requests.get(complete_url)
    return response.json()

# Function to display temperature alert
def temperature_alert(temp):
    """Displays alert based on temperature."""
    if temp > 300:
        st.error(" Temperature is quite high! Stay hydrated!")
    elif temp < 273.15:
        st.warning("❄️ It's freezing! Keep warm!")
    else:
        st.success(" Temperature is moderate. Enjoy your day!")

# Function to plot temperature trend
def plot_temperature(temp, feels_like):
    """Plots temperature and feels-like temperature."""
    labels = ["Temperature", "Feels Like"]
    values = [temp, feels_like]

    fig = go.Figure(data=[go.Bar(x=labels, y=values, text=values, textposition='auto')])
    fig.update_layout(title="Temperature vs Feels Like", yaxis=dict(title="Temperature (K)"))

    st.plotly_chart(fig)

# Function to plot map
def plot_map(lat, lon):
    """Displays the location on a map."""
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))



# Button to get weather data

if location:
    weather_data = get_weather_data(location)
    if weather_data["cod"] != "404":
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        description = weather_data['weather'][0]['description']
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']

        st.write(f"## Weather in {location.title()}:")
        st.write(f"**Temperature**: {temp} K")
        st.write(f"**Feels like**: {feels_like} K")
        st.write(f"**Description**: {description.capitalize()}")

        temperature_alert(temp)
        plot_temperature(temp, feels_like)
        plot_map(lat, lon)
        

    else:
        st.write("City not found. Please check your input.")
else:
    st.write("Please enter a location.")



API_KEY = "d0d8d26e14950d5578e76d6a4c369529"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"



def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_recommendations(temp_celsius):
    if temp_celsius < 25:
        return "😊The temperature is comfortable. No special precautions needed for heat stroke prevention."
    elif 25 <= temp_celsius < 30:
        return """
        - Stay hydrated by drinking plenty of water
        - Wear light, loose-fitting clothing
        - Limit outdoor activities during the hottest part of the day
        """
    elif 30 <= temp_celsius < 35:
        return """
        - Drink plenty of water and electrolyte-rich fluids
        - Wear light, loose-fitting, and breathable clothing
        - Avoid outdoor activities between 10 AM and 4 PM
        - Use sunscreen and wear a wide-brimmed hat when outside
        - Take frequent breaks in shaded or air-conditioned areas
        """
    elif temp_celsius<0:
        return "❄️ It's freezing! Keep warm!"

    else:
        return """
        - 🔥Drink plenty of water and electrolyte-rich fluids, even if you don't feel thirsty
        - Wear light, loose-fitting, and breathable clothing
        - Stay indoors in air-conditioned areas as much as possible
        - If you must go outside, limit activity to early morning or evening hours
        - Take cool showers or baths to lower your body temperature
        - Check on elderly neighbors and those with health conditions
        - Never leave children or pets in parked cars
        - If you feel dizzy, weak, or overheated, seek medical attention immediately
        """

st.write("Heat Stroke Prevention Recommendations")

city =location

if city:
    weather_data = get_weather_data(city)
    
    if weather_data:
        temp_kelvin = weather_data["main"]["temp"]
        temp_celsius = kelvin_to_celsius(temp_kelvin)
        
        st.write(f"Current temperature in {city}: {temp_celsius:.1f}°C")
        
        recommendations = get_recommendations(temp_celsius)
        st.subheader("Recommendations:")
        st.write(recommendations)
        
        # Display additional weather information
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        st.subheader("Additional Weather Information:")
        weather_df = pd.DataFrame({
            "Metric": ["Humidity", "Wind Speed"],
            "Value": [f"{humidity}%", f"{wind_speed} m/s"]
        })
        st.table(weather_df)
        
    else:
        st.error("Unable to fetch weather data. Please check the city name and try again.")













st.title("Welcome! Choose the information you'd like to access:")

option = st.radio(
    "Select an option:",
    ("Flood Forecast", "Landslide Information","Earthquake running history")
)

if st.button("Access Information"):
    if option == "Flood Forecast":
        webbrowser.open_new_tab("https://ndem.nrsc.gov.in/hydrological_fivedaycwc.php")
        st.success("Opening flood forecast information.")
    elif option =="Landslide Information":
        webbrowser.open_new_tab("https://ndem.nrsc.gov.in/geological_lshz.php")
        st.success("Opening landslide information.")
    elif option == "Earthquake running history":
        webbrowser.open_new_tab("https://ndem.nrsc.gov.in/geological_eq.php")
        st.success("Opening earthquakes running history with active events.")

st.write("Note: The data visible is just a prediction.")









