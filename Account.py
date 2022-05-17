import sqlite3

from PyQt5.QtWidgets import QMessageBox


class Account:
    def __init__(self):
        try:
            self.connect = sqlite3.connect("files/pyweather.db")
        except sqlite3.Error as error:
            message('Ошибка', f'Ошибка подключения к SQL\nОшибка: {error}')

    def checkUser(self, user, password):
        """Проверка введенных данных"""
        cmd = f"SELECT id FROM account WHERE user='{user}' AND password='{password}'"
        request = self.connect.cursor()
        request.execute(cmd)
        result = request.fetchall()
        if not result:
            message('Ошибка', 'Пароль или логин не совпадают, повторите снова')
        else:
            return result[0][0]

    def getData(self, id):
        """Полученные данных и парсинг"""
        cmd = f"SELECT * FROM account WHERE id={id}"
        request = self.connect.cursor()
        request.execute(cmd)
        result = request.fetchall()
        if result:
            result = result[0]
            data = {
                    'status': True,
                    'id': result[0],
                    'login': result[1],
                    'name': result[2],
                    'city': result[3],
                    'password': result[4]
                    }
        else:
            data = {'status': False, 'error': 'Неправильный логин или пароль'}
        return data

    def createUser(self, login, password, name, city):
        """Создание нового аккаунта"""
        cmd = f"INSERT INTO account(user, name, city, password) VALUES (?, ?, ?, ?)"
        data = (login, name, city, password)
        try:
            request = self.connect.cursor()
            request.execute(cmd, data)
        except sqlite3.Error as e:
            message('Ошибка', f'Ошибка создания аккаунта\nОшибка: {e}')
        else:
            self.connect.commit()
            return True

    def updateUser(self, id, name, login, password, city):
        cmd = f"UPDATE account SET name = ?, user = ?, password = ?, city = ? WHERE id = {id}"
        data = (name, login, password, city)
        try:
            request = self.connect.cursor()
            request.execute(cmd, data)
        except sqlite3.Error as e:
            message('Ошибка', f'Ошибка обновления данных\nОшибка: {e}')
            return False
        else:
            message('Успех', 'Все изменения сохранены')
            self.connect.commit()
            return True


def message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.exec_()
