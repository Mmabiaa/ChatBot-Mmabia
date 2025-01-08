import requests
import logging

def get_weather(city):
    try:
        api_key = "YOUR_API_KEY"  
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        logging.debug(f"Fetching weather for {city} from URL: {complete_url}")
        response = requests.get(complete_url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]
            return f"The weather in {city} is {weather['description']} with a temperature of {main['temp']}°K."
        else:
            logging.error(f"Failed to retrieve weather information. Status code: {response.status_code}")
            return "I couldn't retrieve the weather information."
    except Exception as e:
        logging.error(f'Error retrieving weather data: {e}')
        return "I'm sorry, I couldn't retrieve the weather information."