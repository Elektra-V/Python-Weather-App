# Python-Weather-App
This is a web application that displays weather data for a given city. The app retrieves weather data from the OpenWeatherMap API and caches it to improve performance. The app also limits the number of requests a client can make to the API within a given time period.

Requirements
Python 3.6 or higher
Flask 2.0.1
Requests 2.25.1

Installation
Clone the repository:
$ git clone https://github.com/yourusername/weather-app.git

Install the required packages:
$ pip install -r requirements.txt

Set your OpenWeatherMap API key in the app.py file:
api_key = 'your_api_key'

Usage
Run the app:
$ python app.py

Open a web browser and navigate to http://localhost:8000.

Enter a city name and click the "Get Weather" button.

The app will display the temperature, humidity, sunrise time, sunset time, and timezone for the specified city.

Acknowledgements
This app was created by Vedika Chauhan as a personal project. The app is based on the OpenWeatherMap API and uses code from the Flask documentation. This project is licensed under the MIT License. See the LICENSE file for more information.
