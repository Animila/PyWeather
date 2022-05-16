from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import sys

from setting import api_key
from processData import getApi


class WeatherWindows(QMainWindow):
    """Окно погоды"""
    def __init__(self):
        super().__init__()
        uic.loadUi('5.ui', self)

        self.data = getApi('Якутск', api_key)
        self.setState()

    def setState(self):
        """Установка данных"""
        self.time.setText(self.data['time'])
        self.gradus.setText(f"{str(self.data['temp'])}°C")
        self.gorod.setText(self.data['city'])
        self.weather.setText(self.data['descr'])
        self.week.setText(self.data['week'])
        self.day.setText(self.data['month'])


def application():
    """Метод самого приложения"""
    app = QApplication(sys.argv)
    windows = WeatherWindows()
    windows.setFixedSize(333, 491)
    windows.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
