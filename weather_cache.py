from weather_client import OpenWeatherClient
from datetime import datetime, timedelta
from city_locks import CityLocks

class WeatherCache:
    def __init__(self, api_key: str, cache_duration: timedelta = timedelta(minutes=5)):
        self.weather_api = OpenWeatherClient(api_key)
        self.cache_duration = cache_duration
        self.weather_cache = {}
        self.city_locks = CityLocks()

    def get_weather_data(self, city: str) -> dict:
        try:
            self.city_lock = self.city_locks.get_lock(city)
            # check if the requested city is already in the cache
            if city in self.weather_cache:
                with self.city_lock:
                    # retrieve the cached data
                    timestamp, data = self.weather_cache[city]
                    # calculate how long ago the data was cached
                    age = datetime.now() - timestamp
                    # if the data is still fresh, return it
                    if age < self.cache_duration:
                        return data

            with self.city_lock:
                if city not in self.weather_cache:
                    fetched_data = self.fetch_weather_data(city)
                    return fetched_data
                else:
                    return self.weather_cache[city]
        
        except Exception as e:
            print(f"An error occurred while fetching weather data for {city}: {e}")
            return None
    
    def fetch_weather_data(self, city: str):
        try:
            # fetch the weather data from the OpenWeatherMap API
            data = self.weather_api.get_weather_data(city.capitalize())

            # update the cache with the fetched data
            self.weather_cache[city] = (datetime.now(), data)    
            return data

        except Exception as e:
            print(f"An error occurred while fetching weather data for {city}: {e}")