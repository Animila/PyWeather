from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
import json

from Account import Account
from processData import getWeather

account = Account()


def getCity():
    """Получаем список городов"""
    list_city = []
    with open('russian-cities.json', encoding='utf-8', mode='r') as f:
        templates = json.load(f)
    for i in templates:
        list_city.append(i['name'])
    return list_city


class WeatherWindows(QMainWindow):
    """Окно погоды"""
    def __init__(self, data):
        super().__init__()
        uic.loadUi('5.ui', self)

        self.data = getWeather(data['city'])
        self.setState()

    def setState(self):
        """Отображение полученных данных"""
        self.time.setText(self.data['time'])
        self.gradus.setText(f"{str(self.data['temp'])}°C")
        self.gorod.setText(self.data['city'])
        self.weather.setText(self.data['descr'])
        self.week.setText(self.data['week'])
        self.day.setText(self.data['month'])


class Authenticate(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('auth.ui', self)
        self.check.clicked.connect(self.getUser)
        self.auth.clicked.connect(self.register)

    def getUser(self):
        login = self.login.toPlainText()
        password = self.password.toPlainText()
        if login == password or not login or not password:
            print('Ошибка')
        else:
            data = account.getData(login, password)
            if data['status']:
                self.hide()
                self.weather = WeatherWindows(data)
                self.weather.setFixedSize(333, 506)
                self.weather.show()
            else:
                print(data['error'])



    def register(self):
        """окно регистрации"""
        self.hide()
        self.register = Register()
        self.register.setFixedSize(382, 349)
        self.register.show()


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('register.ui', self)
        self.comboBox.addItems(getCity())
        self.check.clicked.connect(self.createUser)

    def createUser(self):
        login = self.login.toPlainText()
        password = self.password.toPlainText()
        name = self.name.toPlainText()
        # city = self.comboBox.activated[str].connect()

        if account.create(login, password, name, 'Якутск'):
            self.auth()

    def auth(self):
        self.hide()
        self.login = Authenticate()
        self.login.setFixedSize(382, 274)
        self.login.show()


def application():
    """Само приложение"""
    app = QApplication(sys.argv)
    login = Authenticate()
    login.setFixedSize(382, 274)
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
