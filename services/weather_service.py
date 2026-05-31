import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_weather_forecast(location):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return "Weather service is currently unavailable."

    try:
        # OpenWeatherMap Forecast API (5 day / 3 hour)
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location},ZW&appid={api_key}&units=metric"
        
        response = requests.get(url)
        data = response.json()

        if data.get('cod') != "200":
            return f"Could not find weather for {location}. Please check the city name."

        city_name = data['city']['name']
        forecast_list = data['list']
        
        # We want 3 days, so we pick roughly 24h intervals (every 8th item since it's 3-hourly)
        days = [forecast_list[0], forecast_list[8], forecast_list[16]]
        
        response_text = f"⛅ WEATHER FORECAST - {city_name.upper()}\n\n"
        
        day_labels = ["Today", "Tomorrow", "Wednesday"] # Simplified, could be dynamic
        # Dynamic labels
        for i, day in enumerate(days):
            dt = datetime.fromtimestamp(day['dt'])
            label = dt.strftime('%A') if i > 0 else "Today"
            temp = round(day['main']['temp'])
            desc = day['weather'][0]['description'].capitalize()
            humidity = day['main']['humidity']
            
            response_text += f"{label}: {temp}°C, {desc}, {humidity}% humidity\n"
            
        # Add farming tip based on weather
        first_day_weather = days[0]['weather'][0]['main'].lower()
        tip = "Good planting conditions today."
        if 'rain' in first_day_weather:
            tip = "Expect rain, good for moisture but avoid heavy spraying."
        elif 'clear' in first_day_weather:
            tip = "Clear skies, good for drying produce or harvesting."
            
        response_text += f"\nFarming tip: {tip}\n"
        response_text += "\n🌾 Want crop advice for this weather? Reply 'crop advice maize'"
        
        return response_text
    except Exception as e:
        print(f"Error in Weather API: {e}")
        return "Sorry, I couldn't fetch the weather forecast right now."
