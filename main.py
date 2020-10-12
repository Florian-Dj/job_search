# -*- coding: utf-8 -*-

import os
import sys


def check_db():
    if not os.path.isfile('data.db'):
        if sys.platform == "win32":
            print("Il manque le fichier data.db")


if __name__ == '__main__':
    check_db()
    print("Search Jobs V0.5")
    print("By Mucral")
    os.system('python manage.py runserver --insecure 80')
