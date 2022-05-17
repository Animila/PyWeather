import sqlite3


class Account:
    def __init__(self):
        try:
            self.connect = sqlite3.connect("pyweather.db")
        except sqlite3.Error as error:
            print(f'Ошибка работы с SQL\nОшибка: {error}')

    def checkUser(self, user, password):
        """Проверка введенных данных"""
        cmd = f"SELECT * FROM account WHERE user='{user}' AND password='{password}'"
        request = self.connect.cursor()
        request.execute(cmd)
        return request.fetchall()

    def getData(self, login, password):
        """Полученные данных и обработка"""
        result = self.checkUser(login, password)
        if result:
            result = result[0]
            data = {
                    'status': True,
                    'id': result[0],
                    'login': result[1],
                    'name': result[2],
                    'city': result[3]
                    }
        else:
            data = {
                'status': False,
                'error': 'Неправильный логин или пароль'
            }

        return data

    def create(self, login, password, name, city):
        cmd = f"INSERT INTO account(user, name, city, password) VALUES (?, ?, ?, ?)"
        data = (login, name, city, password)
        try:
            request = self.connect.cursor()
            request.execute(cmd, data)
        except sqlite3.Error as e:
            print(f'{e}')
        else:
            self.connect.commit()
            return True
