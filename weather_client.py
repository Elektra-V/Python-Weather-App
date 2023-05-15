import requests

class OpenWeatherClient:
    # initializes the class with an API key
    def __init__(self, api_key:str) -> None :
        self.api_key = api_key

    # fetches weather data for a given city using the OpenWeather API
    def get_weather_data(self, city):
        try:
            # build the URL to access the API
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
            
            # send a GET request to the API and get the response in JSON format
            response = requests.get(url)
            return response.json()
        
        except Exception as e:
            # in case of any error, print a message and return None
            print(f"An error occurred while fetching weather data for {city}: {e}")
            return None