from telebot import types


def start_bot_location_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    share_location = types.KeyboardButton('📍Share Location', request_location=True)
    search_location = types.KeyboardButton('🌏 Search Location')
    markup.row(share_location, search_location)
    return markup


def cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = types.KeyboardButton('❌ Cancel')
    markup.add(cancel)
    return markup


def weather_data_type_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    now = types.KeyboardButton('⌚️Now')
    today = types.KeyboardButton('📆Today')
    tomorrow = types.KeyboardButton('📅Tomorrow')
    seven_days = types.KeyboardButton('🗓️For 7 Days')
    back = types.KeyboardButton('⬅️Back')
    markup.row(now, today)
    markup.row(tomorrow, seven_days)
    markup.add(back)
    return markup


