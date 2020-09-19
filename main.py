# -*- coding: utf-8 -*-

import os
import sys


def check_db():
    if not os.path.isfile('data.db'):
        if sys.platform != "win32":
            os.system('cp data_default.db data.db')
        else:
            print("Il manque le fichier data.db")


if __name__ == '__main__':
    check_db()
    print("Search Jobs V0.4")
    print("By Mucral")
    os.system('python manage.py runserver 80')
    # pyinstaller --onefile --icon=logo.ico main.py     Command Pyinstaller
