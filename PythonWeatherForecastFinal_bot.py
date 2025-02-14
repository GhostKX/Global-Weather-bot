import os

import telebot
import buttons
import requests
from datetime import datetime
import math
from dotenv import load_dotenv


load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
bot = telebot.TeleBot(API_KEY)

API_1 = str(os.getenv('API1'))
API_2 = str(os.getenv('API2'))

city_details = {}
seven_days = []

condition_to_emoji = {
    "Clear": "☀️",
    "Sunny": "☀️",
    "Partly Cloudy": "⛅",
    "Cloudy": "☁️",
    "Overcast": "🌥️",
    "Mist": "🌫️",
    "Patchy Rain": "🌦️",
    "Patchy Light Rain": "🌦️",
    "Patchy Rain Nearby": "🌦️",
    "Patchy Snow": "🌨️ ❄️",
    "Freezing Drizzle": "🌧️",
    "Thunder": "⛈️",
    "Blowing Snow": "🌬️",
    "Fog": "🌁",
    "Light Rain Shower": "🌦️",
    "Light Rain": "🌦️",
    "Light Drizzle": "🌦️",
    "Light Snow Shower": "🌨️ ❄️",
    "Moderate Rain": "🌧️",
    "Thunderstorm": "⛈️ ⚡️",
    "Blizzard": "🌪️"
}


night_icon_code_to_emoji = {
    1000: "🌙",  # Clear
    1003: "☁️",  # Partly Cloudy
    1006: "☁️",  # Cloudy
    1009: "☁️",  # Overcast
    1030: "🌫️",  # Mist
    1063: "🌧️",  # Patchy Rain
    1066: "🌨️ ❄️",  # Patchy Snow
    1072: "🌧️",  # Freezing Drizzle
    1087: "⛈️",  # Thunder
    1114: "🌬️",  # Blowing Snow
    1135: "🌁",  # Fog
    1150: "🌧️",
    1153: "🌦️",
    1180: "🌧️",
    1183: "🌧️",
    1186: "🌧️",  # Light Rain Shower
    1210: "🌨️ ❄️",  # Light Snow Shower
    1243: "🌧️",  # Moderate Rain
    1273: "⛈️ ⚡️",  # Thunderstorm
    1282: "🌪️"  # Blizzard
}


condition_to_emoji_7_days = {
    "Thunderstorm With Light Rain": "⛈️",  # Thunderstorm
    "Thunderstorm With Rain": "⛈️",  # Thunderstorm
    "Thunderstorm With Heavy Rain": "⛈️",  # Thunderstorm
    "Thunderstorm With Light Drizzle": "⛈️",  # Thunderstorm
    "Thunderstorm With Drizzle": "⛈️",  # Thunderstorm
    "Thunderstorm With Heavy Drizzle": "⛈️",  # Thunderstorm
    "Thunderstorm With Hail": "⛈️",  # Thunderstorm With Hail
    "Light Drizzle": "🌦️",  # Light Drizzle
    "Drizzle": "🌦️",  # Drizzle
    "Heavy Drizzle": "🌧️",  # Heavy Drizzle
    "Light Rain": "🌦️",  # Light Rain
    "Patchy Light Rain": "🌦️",  # Patchy Light Rain
    "Moderate Rain": "🌧️",  # Moderate Rain
    "Heavy Rain": "🌧️",  # Heavy Rain
    "Freezing Rain": "🌧️",  # Freezing Rain
    "Light Freezing Rain": "🌧️",  # Light Freezing Rain
    "Light Shower Rain": "🌦️",  # Light Shower Rain
    "Shower Rain": "🌧️",  # Shower Rain
    "Heavy Shower Rain": "🌧️",  # Heavy Shower Rain
    "Light Snow": "🌨️",  # Light Snow
    "Patchy Light Snow": "🌨️",  # Patchy Light Snow
    "Snow": "🌨️",  # Snow
    "Heavy Snow": "❄️",  # Heavy Snow
    "Mix Snow/Rain": "🌨️",  # Mix Snow/Rain
    "Sleet": "🌨️",  # Sleet
    "Heavy Sleet": "🌨️",  # Heavy Sleet
    "Ice Pellets": "🧊",  # Ice Pellets
    "Snow Shower": "🌨️",  # Snow Shower
    "Heavy Snow Shower": "❄️",  # Heavy Snow Shower
    "Blowing Snow": "🌬️❄️",  # Blowing Snow
    "Hail": "🌨️🧊",  # Hail
    "Flurries": "❄️",  # Flurries
    "Mist": "🌫️",  # Mist
    "Smoke": "🌫️",  # Smoke
    "Haze": "🌫️",  # Haze
    "Sand/Dust": "🌫️",  # Sand/Dust
    "Fog": "🌫️",  # Fog
    "Freezing Fog": "🌫️",  # Freezing Fog
    "Dust Storm": "🌪️",  # Dust Storm
    "Tornado": "🌪️",  # Tornado
    "Clear Sky": "☀️",  # Clear Sky
    "Few Clouds": "⛅",  # Few Clouds
    "Scattered Clouds": "⛅",  # Scattered Clouds
    "Broken Clouds": "☁️",  # Broken Clouds
    "Overcast Clouds": "☁️",  # Overcast Clouds
    "Unknown Precipitation": "🌦️❓"  # Unknown Precipitation
}


@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Welcome to the Global 🌦️ Weather ⛈️️ bot',
                     reply_markup=buttons.start_bot_location_buttons())
    bot.register_next_step_handler(message, handle_location)


@bot.message_handler(content_types=['text'])
def handle_location(message):
    user_id = message.from_user.id
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        bot.send_message(user_id, '🌏 Sharing location...')
        try:
            url = requests.get(f'https://api.weatherapi.com/v1/current.json?'
                               f'key={API_1}&q={latitude},{longitude}&aqi=yes')
            if url.status_code == 200:
                weather_details = url.json()
                city_name = weather_details['location']['name']
                city_details['city_name'] = city_name
                country_name = weather_details['location']['country']
                city_details['country_name'] = country_name
                city_details['latitude'] = latitude
                city_details['longitude'] = longitude
                bot.send_message(user_id, f'✅ {city_name}, {country_name} ✅'
                                          f'\n\n🌦️Weather🌤️ Forecast buttons below 💬',
                                 reply_markup=buttons.weather_data_type_buttons())
                bot.register_next_step_handler(message, weather_choose_data_type)
            else:
                bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                          'Please try to check network connection 💬',
                                 reply_markup=buttons.start_bot_location_buttons())
                bot.register_next_step_handler(message, handle_location)
        except ValueError:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try again later 💬',
                             reply_markup=buttons.start_bot_location_buttons())
            bot.register_next_step_handler(message, handle_location)
    elif message.text == '🌏 Search Location':
        bot.send_message(user_id, '🏙️ Please type in City name', reply_markup=buttons.cancel_button())
        bot.register_next_step_handler(message, location_city_name)
    else:
        bot.send_message(user_id, '❌ ERROR ❌\n\n'
                                  '⬇️ Please use buttons below 💬 ⬇️',
                         reply_markup=buttons.start_bot_location_buttons())
        bot.register_next_step_handler(message, handle_location)


def location_city_name(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        city_details.clear()
        seven_days.clear()
        bot.send_message(user_id, '🔙To Menu', reply_markup=buttons.start_bot_location_buttons())
        bot.register_next_step_handler(message, handle_location)
    else:
        try:
            url = requests.get(f'https://api.weatherapi.com/v1/current.json?key={API_1}&q={message.text}&aqi=yes')
            if url.status_code == 200:
                weather_details = url.json()
                city_name = weather_details['location']['name']
                city_details['city_name'] = city_name
                country_name = weather_details['location']['country']
                city_details['country_name'] = country_name
                latitude = weather_details['location']['lat']
                city_details['latitude'] = latitude
                longitude = weather_details['location']['lon']
                city_details['longitude'] = longitude
                bot.send_message(user_id, f'✅ {city_name}, {country_name} ✅'
                                          f'\n\n🌦️Weather🌤️ Forecast buttons below 💬',
                                 reply_markup=buttons.weather_data_type_buttons())
                bot.register_next_step_handler(message, weather_choose_data_type)
            else:
                bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                          'Please try to check network connection 💬',
                                 reply_markup=buttons.start_bot_location_buttons())
                bot.register_next_step_handler(message, handle_location)
        except ValueError:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try again later 💬',
                             reply_markup=buttons.start_bot_location_buttons())
            bot.register_next_step_handler(message, handle_location)


def weather_choose_data_type(message):
    user_id = message.from_user.id
    if message.text == '⌚️Now':
        try:
            url = requests.get(
                f'https://api.weatherapi.com/v1/current.json?key={API_1}&q={city_details['city_name']}&aqi=yes')
            if url.status_code == 200:
                weather_details = url.json()
                weather_now(message, weather_details)
            else:
                bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                          'Please try to check network connection 💬',
                                 reply_markup=buttons.start_bot_location_buttons())
                bot.register_next_step_handler(message, handle_location)
        except ValueError:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try again later 💬',
                             reply_markup=buttons.start_bot_location_buttons())
            bot.register_next_step_handler(message, handle_location)
    elif message.text == '📆Today':
        try:
            url = requests.get('https://api.weatherapi.com/v1/'
                               f'forecast.json?key={API_1}&q={city_details['city_name']}'
                               f'&days=1&aqi=yes&alerts=no')
            if url.status_code == 200:
                weather_details = url.json()
                weather_today(message, weather_details)
            else:
                bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                          'Please try to check network connection 💬',
                                 reply_markup=buttons.start_bot_location_buttons())
                bot.register_next_step_handler(message, handle_location)
        except ValueError:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try again later 💬',
                             reply_markup=buttons.start_bot_location_buttons())
            bot.register_next_step_handler(message, handle_location)
    elif message.text == '📅Tomorrow':
        try:
            url = requests.get('https://api.weatherapi.com/v1/'
                               f'forecast.json?key={API_1}&q={city_details['city_name']}'
                               f'&days=2&aqi=yes&alerts=no')
            if url.status_code == 200:
                weather_details = url.json()
                weather_tomorrow(message, weather_details)
            else:
                bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                          'Please try to check network connection 💬',
                                 reply_markup=buttons.start_bot_location_buttons())
                bot.register_next_step_handler(message, handle_location)
        except ValueError:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try again later 💬',
                             reply_markup=buttons.start_bot_location_buttons())
            bot.register_next_step_handler(message, handle_location)
    elif message.text == '🗓️For 7 Days':
        try:
            url = requests.get(
                f'https://api.weatherbit.io/v2.0/forecast/daily?city={city_details['city_name']}&key={API_2}')
            if url.status_code == 200:
                weather_details = url.json()
                weather_for_7_days(message, weather_details)
            else:
                bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                          'Please try to check network connection 💬',
                                 reply_markup=buttons.start_bot_location_buttons())
                bot.register_next_step_handler(message, handle_location)
        except ValueError:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try again later 💬',
                             reply_markup=buttons.start_bot_location_buttons())
            bot.register_next_step_handler(message, handle_location)
    elif message.text == '⬅️Back':
        city_details.clear()
        seven_days.clear()
        bot.send_message(user_id, '🔙To Menu', reply_markup=buttons.start_bot_location_buttons())
        bot.register_next_step_handler(message, handle_location)
    else:
        bot.send_message(user_id, '❌ ERROR ❌\n\n'
                                  '⬇️ Please use buttons below 💬 ⬇️',
                         reply_markup=buttons.weather_data_type_buttons())
        bot.register_next_step_handler(message, weather_choose_data_type)


def weather_now(message, weather_details):
    user_id = message.from_user.id

    date_time = weather_details['location']['localtime']
    dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
    formatted_time = dt.strftime("%H:%M")  # %H for 24-hour format
    formatted_date = dt.strftime("🗓️ %d of %B, %Y")

    is_day = weather_details['current']['is_day']
    text = weather_details['current']['condition']['text'].title().strip()
    temp_c = math.floor(weather_details['current']['temp_c'])
    humidity = weather_details['current']['humidity']
    icon_code = weather_details['current']['condition']['code']

    print(weather_details)

    if is_day == 1:
        bot.send_message(user_id,
                         f'{'*' * 45}'
                         f'\n                  🌏 {city_details["city_name"]}, {city_details["country_name"]}'
                         f'\n                  ({formatted_date})'
                         f'\n\n\n⌚️ Time: {formatted_time}'
                         f'\n\n🌡️ Temperature: {temp_c}°C {condition_to_emoji[text]}'
                         f'\n\n🌆 Condition: {text}'
                         f'\n\n💧 Humidity: {humidity}%'
                         f'\n{'*' * 45}', reply_markup=buttons.weather_data_type_buttons())
        bot.register_next_step_handler(message, weather_choose_data_type)

    else:
        bot.send_message(user_id,
                         f'{'*' * 45}'
                         f'\n                  🌏 {city_details["city_name"]}, {city_details["country_name"]}'
                         f'\n                   ({formatted_date})'
                         f'\n\n\n⌚️Time: {formatted_time}'
                         f'\n\n🌡️Temperature: {temp_c}°C {night_icon_code_to_emoji[icon_code]}'
                         f'\n\n🌃 Condition: {text}'
                         f'\n\n💧 Humidity: {humidity}%'
                         f'\n{'*' * 45}', reply_markup=buttons.weather_data_type_buttons())
        bot.register_next_step_handler(message, weather_choose_data_type)


def weather_today(message, weather_details):
    user_id = message.from_user.id

    message_to_user = f'{'⌚️Time':<15}{'🌡️°C':<15}{'✨Sky':<15}{'Icon':<15}'
    message_to_user += f'\n{'_' * 38}'
    forecast_day = weather_details['forecast']['forecastday'][0]
    sunrise = forecast_day['astro']['sunrise']
    sunset = forecast_day['astro']['sunset']
    for hour_data in forecast_day['hour']:

        time = hour_data['time']
        dt = datetime.strptime(time, '%Y-%m-%d %H:%M')
        formatted_time = dt.strftime("%H:%M")  # %H for 24-hour format
        formatted_date = dt.strftime("🗓️ %d of %B %Y")

        temp_c = hour_data['temp_c']
        temp_c = math.floor(temp_c)

        is_day = hour_data['is_day']
        text = hour_data['condition']['text'].title().strip()
        night_icon = hour_data['condition']['code']
        humidity = weather_details['current']['humidity']
        city_details['today_date'] = formatted_date
        city_details['today_humidity'] = humidity

        if is_day == 1:
            day_icon = condition_to_emoji[text]
            message_to_user += f'\n\n{formatted_time:<17}{f'{temp_c}°C':<17}{text:<17}{day_icon:<15}'
        else:
            night_icon = night_icon_code_to_emoji[night_icon]
            message_to_user += f'\n\n{formatted_time:<17}{f'{temp_c}°C':<17}{text:<17}{night_icon:<15}'

    bot.send_message(user_id, f'{'*' * 45}'
                              f'\n                  🌏 {city_details["city_name"]}, {city_details["country_name"]}'
                              f'\n                   ({city_details["today_date"]})'
                              f'\n\n\n{message_to_user}'
                              f'\n{'_' * 38}'
                              f'\n\n🌅 Sunrise: {sunrise}'
                              f'\n\n🌃 Sunset: {sunset}'
                              f'\n\n💧 Humidity: {city_details['today_humidity']}%'
                              f'\n{'*' * 45}',
                     reply_markup=buttons.weather_data_type_buttons())
    bot.register_next_step_handler(message, weather_choose_data_type)


def weather_tomorrow(message, weather_details):
    user_id = message.from_user.id

    message_to_user = f'{'⌚️Time':<15}{'🌡️°C':<15}{'✨Sky':<15}{'Icon':<15}'
    message_to_user += f'\n{'_' * 38}'
    forecast_day = weather_details['forecast']['forecastday'][1]
    sunrise = forecast_day['astro']['sunrise']
    sunset = forecast_day['astro']['sunset']
    for hour_data in forecast_day['hour']:

        time = hour_data['time']
        dt = datetime.strptime(time, '%Y-%m-%d %H:%M')
        formatted_time = dt.strftime("%H:%M")  # %H for 24-hour format
        formatted_date = dt.strftime("🗓️ %d of %B, %Y")

        temp_c = hour_data['temp_c']
        temp_c = math.floor(temp_c)

        is_day = hour_data['is_day']
        text = hour_data['condition']['text'].title().strip()
        night_icon = hour_data['condition']['code']
        humidity = weather_details['current']['humidity']
        city_details['today_date'] = formatted_date
        city_details['today_humidity'] = humidity

        if is_day == 1:
            day_icon = condition_to_emoji[text]
            message_to_user += f'\n\n{formatted_time:<17}{f'{temp_c}°C':<17}{text:<17}{day_icon:<15}'
        else:
            night_icon = night_icon_code_to_emoji[night_icon]
            message_to_user += f'\n\n{formatted_time:<17}{f'{temp_c}°C':<17}{text:<17}{night_icon:<15}'

    bot.send_message(user_id, f'{'*' * 45}'
                              f'\n                  🌏 {city_details["city_name"]}, {city_details["country_name"]}'
                              f'\n                   ({city_details["today_date"]})'
                              f'\n\n\n{message_to_user}'
                              f'\n{'_' * 38}'
                              f'\n\n🌅 Sunrise: {sunrise}'
                              f'\n\n🌃 Sunset: {sunset}'
                              f'\n\n💧 Humidity: {city_details['today_humidity']}%'
                              f'\n{'*' * 45}',
                     reply_markup=buttons.weather_data_type_buttons())
    bot.register_next_step_handler(message, weather_choose_data_type)


def weather_for_7_days(message, weather_details):
    user_id = message.from_user.id

    message_to_user = f'{'🗓️Day':<15}{'🌡️°C':<15}{'✨Sky':<15}{'Icon':<15}'
    message_to_user += f'\n{'_' * 38}'

    for day in weather_details['data']:

        date = day['datetime']
        dt = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = dt.strftime("%a")
        any_day = dt.strftime('%d of %B')
        seven_days.append(any_day)

        high_temp = math.floor(day['high_temp'])
        low_temp = math.floor(day['low_temp'])
        text = day['weather']['description'].title().strip()
        icon = condition_to_emoji_7_days[text]

        message_to_user += f'\n\n{formatted_date:<17}{f'{high_temp}-{low_temp}°C':<17}{text:<17}{icon:<15}'

    bot.send_message(user_id, f'{'*' * 45}'
                              f'\n                  🌏 {city_details["city_name"]}, {city_details["country_name"]}'
                              f'\n          (🗓️ {seven_days[0]} - {seven_days[-1]})'
                              f'\n\n\n{message_to_user}'
                              f'\n\n{'*' * 45}',
                     reply_markup=buttons.weather_data_type_buttons())
    bot.register_next_step_handler(message, weather_choose_data_type)


bot.polling(non_stop=True)
