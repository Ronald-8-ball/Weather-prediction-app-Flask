from flask import Flask, render_template, request
import requests 

app = Flask(__name__)

API_KEY = "858c878223acb192e9140a63f989d1f2"

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/getWeather', methods=['POST'])
def get_weather():
    city = request.form.get("city")

    # Validate city input
    if not city or not validate_city_name(city):
        return render_template('index.html', error="Please enter a valid city name.")

    # API request to OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" # For temperature in Celsius
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
        return render_template('index.html', weather=weather)
    elif response.status_code == 404:
        return render_template('index.html', error="City not found. Please check the city name and try again.")
    else:
        return render_template('index.html', error="An error occurred while fetching the weather data.")
    
    # Function to validate city name
def validate_city_name(city):
    """
    Validates the city name input.
    Allows alphabetic characters and spaces.
    """
    return all(char.isalpha() or char.isspace() for char in city)

if __name__ == '__main__':
    app.run(debug=True)