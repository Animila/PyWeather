import requests
from pprint import pprint
from datetime import datetime

week = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье',
}

month = {
    '01': 'январь',
    '02': 'февраль',
    '03': 'март',
    '04': 'апрель',
    '05': 'май',
    '06': 'июнь',
    '07': 'июль',
    '08': 'август',
    '09': 'сентябрь',
    '10': 'октябрь',
    '11': 'ноябрь',
    '12': 'декабрь',
}


def getApi(city, key):
    """Получение данных погоды"""
    parameters = {'q': city, 'lang': 'ru', 'appid': key, 'units': 'metric'}
    url = f'https://api.openweathermap.org/data/2.5/weather'
    try:
        api_result = requests.get(url, params=parameters).json()
    except Exception as message:
        print(f'Ошибка: {message}. Проверьте введенные данные')
    else:
        pprint(getWeather(api_result))
        return getWeather(api_result)


def getWeather(api_result):
    """Парсинг данных"""
    return {
            'city': api_result["name"],
            'descr': api_result['weather'][0]['description'],
            'temp': round(api_result['main']['temp']),
            'humidity': api_result['main']['humidity'],
            'pressure': api_result['main']['pressure'],
            'speed_wind': api_result['wind']['speed'],
            'sunrise': datetime.fromtimestamp(api_result['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(api_result['sys']['sunset']),
            'time': datetime.now().strftime("%H:%M"),
            'week': week[datetime.now().weekday()],
            'month': f'{month[datetime.now().strftime("%m")]} {datetime.now().strftime("%d")}',
            }

