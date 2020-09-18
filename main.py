# -*- coding: utf-8 -*-

import os


def check_db():
    if not os.path.isfile('data.db'):
        f = open('data.db', "w")
        f.close()
        os.system('python manage.py migrate')


if __name__ == '__main__':
    check_db()
    print("Search Jobs V0.4")
    print("By Mucral")
    os.system('python manage.py runserver 80')
    # pyinstaller --onefile --icon=logo.ico main.py     Command Pyinstaller
