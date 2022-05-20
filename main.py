# для интерфейса
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
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
    """Окно детального отчета о погоде"""
    def __init__(self, id):
        super().__init__()
        # загрузка дизайна
        path = resource_path(os.path.join('design', 'main_detail.ui'))
        uic.loadUi(path, self)
        # установка кнопки закрыть
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.id_user = id

        self.setState()
        self.setColor()

        self.exit.clicked.connect(self.openMain)

    def setColor(self):
        """Установка цветовой гаммы"""
        if self.data["main"] in ['scattered clouds', 'rain', 'snow', 'mist']:
            self.setStyleSheet(
                'background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(80, 147, 185, 255), stop:1 rgba(108, 175, 209, 255));')
        elif self.data['main'] in ['broken clouds', 'shower rain', 'thunderstorm']:
            self.setStyleSheet(
                'background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 127, 146, 255), stop:0.715909 rgba(97, 152, 183, 255));')
        else:
            self.setStyleSheet(
                'background-color: qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(0, 131, 214, 255), stop:0.0397727 rgba(54, 156, 228, 255), stop:0.965909 rgba(173, 255, 207, 255), stop:0.971591 rgba(149, 255, 200, 255), stop:1 rgba(255, 255, 255, 255));')

    def openMain(self):
        """Открытие главного окна"""
        self.hide()
        self.weather = WeatherWindows(self.id_user)
        self.weather.show()

    def setState(self):
        """Отображение полученных данных"""
        # получение данных
        self.user_data = account.getData(self.id_user)
        self.data = getWeather(self.user_data['city'])
        # отображение изображения
        path = resource_path(os.path.join('image', f'{self.data["image"]}.png'))
        pixmap = QPixmap(path)
        self.photo.setPixmap(pixmap)
        # отображение прочей информации
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
    """Окно отчета о погоде"""
    def __init__(self, id):
        super().__init__()
        # загрузка дизайна
        path = resource_path(os.path.join('design', 'main.ui'))
        uic.loadUi(path, self)
        # установка только закрытия
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # установка цветовой гаммы
        self.id_user = id

        self.setState()
        self.setColor()
        self.interface()

    def setColor(self):
        """Установка цветовой гаммы"""
        if self.data["main"] in ['scattered clouds', 'rain', 'snow', 'mist']:
            self.setStyleSheet('background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(80, 147, 185, 255), stop:1 rgba(108, 175, 209, 255));')
        elif self.data['main'] in ['broken clouds', 'shower rain', 'thunderstorm']:
            self.setStyleSheet('background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 127, 146, 255), stop:0.715909 rgba(97, 152, 183, 255));')
        else:
            self.setStyleSheet('background-color: qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(0, 131, 214, 255), stop:0.0397727 rgba(54, 156, 228, 255), stop:0.965909 rgba(173, 255, 207, 255), stop:0.971591 rgba(149, 255, 200, 255), stop:1 rgba(255, 255, 255, 255));')

    def interface(self):
        """Кнопки"""
        self.exit.clicked.connect(self.openDetail)
        # меню
        self.menuRef.triggered.connect(self.cab)
        self.menuExit.triggered.connect(self.authWindows)

    def openDetail(self):
        """Открытие детального отчета"""
        self.hide()
        self.detail = WeatherDetail(self.id_user)
        self.detail.show()

    def setState(self):
        """Отображение полученных данных"""
        # получение данных
        self.user_data = account.getData(self.id_user)
        self.data = getWeather(self.user_data['city'])
        # установка изображения
        path = resource_path(os.path.join('image', f'{self.data["image"]}.png'))
        pixmap = QPixmap(path)
        self.photo.setPixmap(pixmap)
        # установка данных
        self.time.setText(self.data['time'])
        self.gradus.setText(f"{str(self.data['temp'])}°C")
        self.gorod.setText(self.data['city'])
        self.weather.setText(self.data['descr'])
        self.week.setText(self.data['week'])
        self.day.setText(self.data['month'])

    def cab(self):
        """Переход в личный кабинет"""
        self.cabinet = Cabinet(self.id_user)
        self.cabinet.show()
        self.hide()

    def authWindows(self):
        """Переход в окно авторизации"""
        self.close()
        self.login = Authenticate()
        self.login.show()


class Authenticate(QMainWindow):
    """Окно авторизации"""
    def __init__(self):
        super().__init__()
        # установка дизайна
        path = resource_path(os.path.join('design', 'auth.ui'))
        uic.loadUi(path, self)
        # установка кнопки закрыть
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.interface()

    def interface(self):
        """Кнопки"""
        self.check.clicked.connect(self.checkUser)
        self.reg.clicked.connect(self.register)

    def register(self):
        """Переход на регистрации"""
        self.hide()
        self.register = Register()
        self.register.show()

    def checkUser(self):
        """Авторизация"""
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


class Register(QMainWindow):
    """Окно регистрации"""
    def __init__(self):
        super().__init__()
        # установка дизайна
        path = resource_path(os.path.join('design', 'register.ui'))
        uic.loadUi(path, self)
        # установка кнопки закрытия
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.interface()

    def interface(self):
        """Кнопки"""
        self.city.addItems(getCity())
        self.btnCreate.clicked.connect(self.createUser)
        self.auth.clicked.connect(self.authWindows)

    def createUser(self):
        """Создание пользователя"""
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
        """Окно авторизации"""
        self.hide()
        self.login = Authenticate()
        self.login.show()


class Cabinet(QMainWindow):
    """Окно личного кабинета"""
    def __init__(self, id):
        super().__init__()
        # установка дизайна
        path = resource_path(os.path.join('design', 'cabinet.ui'))
        uic.loadUi(path, self)
        # установка кнопки закрытия
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.data = account.getData(id)
        self.setWindowTitle(self.data['name'])

        self.interface()

    def interface(self):
        """Кнопки"""
        self.setData()
        self.exit.clicked.connect(self.backMenu)
        self.save.clicked.connect(self.saveUser)

    def backMenu(self):
        """окно погоды"""
        self.weather = WeatherWindows(self.data['id'])
        self.weather.show()
        self.hide()

    def setData(self):
        """Загрузка данных в форму"""
        self.name.setText(self.data['name'])
        self.login.setText(self.data['login'])
        self.password.setText(self.data['password'])
        self.city.addItems(getCity())
        index = self.city.findText(self.data['city'])
        self.city.setCurrentIndex(index)

    def saveUser(self):
        """Сохранение изменений"""
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
    """Окно сообщения"""
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.exec_()


def resource_path(relative):
    """Для работы pyinstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


if __name__ == "__main__":
    login = Authenticate()
    login.show()
    sys.exit(app.exec_())
