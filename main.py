# -*- coding: utf-8 -*-

import time
import database
import site


def home():
    print("""
    1 - Run
    2 - Site
    3 - Annonces
    0 - Quitter
    """)
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            exit()
        elif choose == 1:
            run()
        elif choose == 2:
            site.home()
        elif choose == 3:
            annonce()
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        home()


if __name__ == '__main__':
    database.create_db()
    home()
