from flask import Flask, render_template, request, jsonify
from weather_cache import WeatherCache
from weather_limit import RequestLimiter
from datetime import datetime
import traceback


app = Flask(__name__)

# Set API key for OpenWeatherMap API and instantiate WeatherCache and RequestLimiter classes
api_key = ''
weather_cache = WeatherCache(api_key)
weather_limit = RequestLimiter(max_requests=10, time_period=5)


@app.route('/')
def index():
    return render_template('weather.html')


@app.route('/weather', methods=['GET'])
def get_weather():
    try:
        # Get city parameter from query string
        city = request.args.get('city')
        if not city:
            # Return error message if city parameter is missing
            return jsonify({'error': 'City parameter is required.'}), 400

        # Get weather data from cache or API
        weather_data = get_weather_data(city)
        if not weather_data:
            # Return error message if weather data could not be retrieved
            traceback.print_exc()
            return jsonify({'error': f'Failed to get weather data for {city}.'}), 500

        # Extract temperature, humidity, sunrise, sunset, and timezone from weather data
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']
        timezone = weather_data['timezone']

        # Convert sunrise and sunset times to local timezone
        sunrise_time = datetime.utcfromtimestamp(sunrise + timezone).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(sunset + timezone).strftime('%H:%M:%S')

        # Return weather data as JSON object
        return jsonify({
            'temp': temperature,
            'humidity': humidity,
            'sunrise': sunrise_time,
            'sunset': sunset_time,
            'timezone': timezone
        })

    except Exception as e:
        traceback.print_exc()
        print(e)
        return jsonify({'error': f'An error occurred while processing the request: {e}.'}), 500


def get_weather_data(city):
    try:
        # Check request limit for client IP address
        ip_address = request.remote_addr
        if weather_limit.check_request_limit(ip_address):
            return {'error': f'Request limit exceeded for {ip_address}.'}

        # Try to get weather data from cache
        data = weather_cache.get_weather_data(city)
        if data is None:
            # If weather data is not in cache, get it from the API and store it in cache
            traceback.print_exc()
            return None

        # Increment request count for client IP address
        weather_limit.increment_request_count(ip_address)
        return data

    except Exception as e:
        traceback.print_exc()
        return None

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)