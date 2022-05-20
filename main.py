# для интерфейса
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
# для прочих систем
import sys
import os
import json
# импорт других файлов
from Account import Account
from processData import getWeather

# для конвертации файла в exe
app = QApplication([])
account = Account()


def getCity():
    """Получаем список городов"""
    list_city = []
    path = resource_path(os.path.join('files', 'russian-cities.json'))
    with open(path, encoding='utf-8', mode='r') as f:
        templates = json.load(f)
    for i in templates:
        list_city.append(i['name'])
    return list_city


class WeatherDetail(QMainWindow):
    def __init__(self, id):
        super().__init__()
        path = resource_path(os.path.join('design', 'main_detail.ui'))
        uic.loadUi(path, self)

        self.id_user = id
        self.exit.clicked.connect(self.openMain)
        self.user_data = account.getData(self.id_user)
        self.data = getWeather(self.user_data['city'])
        self.setState()

    def openMain(self):
        self.hide()
        self.weather = WeatherWindows(self.id_user)
        self.weather.show()

    def setState(self):
        """Отображение полученных данных"""
        self.time.setText(self.data['time'])
        self.gradus.setText(f"{str(self.data['temp'])}°C")
        self.gorod.setText(self.data['city'])
        self.weather.setText(self.data['descr'])
        self.week.setText(self.data['week'])
        self.day.setText(self.data['month'])
        self.davlenie.setText(f"Давление:\n {self.data['pressure']} гПа")
        self.vlazhnost.setText(f"Влажность:\n {self.data['humidity']}%")
        text = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']
        self.p_vetra.setText(f"Порыв ветра:\n {self.data['gust']} м/с")
        self.v_vetra.setText(f"Скорость:\n {self.data['speed_wind']} м/с")
        self.n_vetra.setText(f"Направление:\n {text[self.data['deg']]}")
        self.oblachnost.setText(f"Облачность:\n {self.data['cloud']}%")


class WeatherWindows(QMainWindow):
    """Окно погоды"""
    def __init__(self, id):
        super().__init__()
        path = resource_path(os.path.join('design', 'main.ui'))
        uic.loadUi(path, self)
        self.id_user = id
        self.user_data = account.getData(id)
        self.data = getWeather(self.user_data['city'])
        self.menuRef.triggered.connect(self.cab)
        self.menuExit.triggered.connect(self.authWindows)
        self.exit.clicked.connect(self.openDetail)
        self.setState()

    def openDetail(self):
        self.hide()
        self.detail = WeatherDetail(self.id_user)
        self.detail.show()

    def setState(self):
        """Отображение полученных данных"""
        self.time.setText(self.data['time'])
        self.gradus.setText(f"{str(self.data['temp'])}°C")
        self.gorod.setText(self.data['city'])
        self.weather.setText(self.data['descr'])
        self.week.setText(self.data['week'])
        self.day.setText(self.data['month'])

    def cab(self):
        self.cabinet = Cabinet(self.id_user)
        self.cabinet.setWindowTitle(self.user_data['name'])
        self.cabinet.show()
        self.hide()

    def authWindows(self):
        self.hide()
        self.login = Authenticate()
        self.login.show()


class Authenticate(QMainWindow):
    def __init__(self):
        super().__init__()
        path = resource_path(os.path.join('design', 'auth.ui'))
        uic.loadUi(path, self)
        self.check.clicked.connect(self.getUser)
        self.reg.clicked.connect(self.register)

    def getUser(self):
        """Получение данных от пользователя"""
        login = self.login.text()
        password = self.password.text()
        if login == password or not login or not password:
            message('Ошибка', 'Некорректные значения, проверьте введенные данные')
        else:
            id_user = account.checkUser(login, password)
            if id_user:
                self.hide()
                self.weather = WeatherWindows(id_user)
                self.weather.show()

    def register(self):
        """Переход на регистрации"""
        self.hide()
        self.register = Register()
        self.register.show()


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        path = resource_path(os.path.join('design', 'register.ui'))
        uic.loadUi(path, self)
        self.interface()

    def interface(self):
        """Работа с элементами"""
        self.city.addItems(getCity())
        self.btnCreate.clicked.connect(self.createUser)
        self.auth.clicked.connect(self.authWindows)

    def createUser(self):
        login = self.login.text()
        password = self.password.text()
        name = self.name.text()
        city = self.city.currentText()
        if not login or not password or not name or not city:
            message('Ошибка', 'Поле не должно быть пустым')
        else:
            if account.createUser(login, password, name, city):
                message('Успех', 'Регистрация завершена')
                self.authWindows()

    def authWindows(self):
        self.hide()
        self.login = Authenticate()
        self.login.show()


class Cabinet(QMainWindow):
    def __init__(self, id):
        super().__init__()
        path = resource_path(os.path.join('design', 'cabinet.ui'))
        uic.loadUi(path, self)
        self.data = account.getData(id)
        self.interface()

    def interface(self):
        self.setData()
        self.exit.clicked.connect(self.backMenu)
        self.save.clicked.connect(self.saveUser)

    def backMenu(self):
        self.weather = WeatherWindows(self.data['id'])
        self.weather.show()
        self.hide()

    def setData(self):
        self.name.setText(self.data['name'])
        self.login.setText(self.data['login'])
        self.password.setText(self.data['password'])
        self.city.addItems(getCity())
        index = self.city.findText(self.data['city'])
        self.city.setCurrentIndex(index)

    def saveUser(self):
        id = self.data['id']
        name = self.name.text()
        login = self.login.text()
        password = self.password.text()
        city = self.city.currentText()
        if account.updateUser(id, name, login, password, city):
            self.backMenu()
            self.setData()
        else:
            message('Ошибка', 'Ошибка обновления данных, повторите попытку')


def message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.exec_()


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


if __name__ == "__main__":
    login = Authenticate()
    login.show()
    sys.exit(app.exec_())
