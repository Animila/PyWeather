from datetime import datetime
import requests
from PyQt5.QtWidgets import QMessageBox

from files.setting import api_key

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

testBase = {
    "coord": {
        "lon": 129.7331,
        "lat": 62.0339
    },
    "weather": [{
        "id": 800,
        "main": "Clear",
        "description": "ясно",
        "icon": "01d"
    }],
    "base": "stations",
    "main": {
        "temp": 8.98,
        "feels_like": 8,
        "temp_min": 8.98,
        "temp_max": 8.98,
        "pressure": 1008,
        "humidity": 66
    },
    "visibility": 10000,
    "wind": {
        "speed": 2,
        "deg": 100
    },
    "clouds": {"all": 0},
    "dt": 1653097927,
    "sys": {
        "type": 1,
        "id": 8854,
        "country": "RU",
        "sunrise": 1653070370,
        "sunset": 1653135763
    },
    "timezone": 32400,
    "id": 2013159,
    "name": "Якутск",
    "cod": 200
}


def getApi(city):
    """Получение данных погоды"""
    parameters = {'q': city, 'lang': 'ru', 'appid': api_key, 'units': 'metric'}
    url = f'https://api.openweathermap.org/data/2.5/weather'
    try:
        api_result = requests.get(url, params=parameters).json()
    except requests.ConnectionError:
        messages('Ошибка', f"Ошибка подключения к серверу", 'Соединение прервано', 'Проверьте свое интернет соединение')
        return testBase
    else:
        if api_result['cod'] != 200:
            messages('Ошибка', f"Сбой работы программы", 'Ошибка на стороне сервера', api_result['message'])
            return testBase
        else:
            return api_result


def getWeather(city):
    api_result = getApi(city)
    """Парсинг данных"""
    data = {
            'city': api_result["name"],
            'main': api_result['weather'][0]['main'],
            'image': api_result['weather'][0]['icon'],
            'descr': api_result['weather'][0]['description'],
            'temp': round(api_result['main']['temp']),
            'humidity': str(api_result['main']['humidity']),
            'pressure': str(api_result['main']['pressure']),
            'speed_wind': str(api_result['wind']['speed']),
            'deg': round((api_result['wind']['deg'] / 45) % 8),
            'cloud': str(api_result['clouds']['all']),
            'sunrise': datetime.fromtimestamp(api_result['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(api_result['sys']['sunset']),
            'time': datetime.now().strftime("%H:%M"),
            'week': week[datetime.now().weekday()],
            'month': f'{month[datetime.now().strftime("%m")]} {datetime.now().strftime("%d")}',
            }
    if 'gust' in api_result['wind']:
        data['gust'] = str(api_result['wind']['gust'])
    else:
        data['gust'] = 0
    return data


def messages(title, text, info, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.setDetailedText(message)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

