# -*- coding: utf-8 -*-

import time
import database
import search
import run


def main():
    print("""
    1 - Run
    2 - Sites
    3 - Annonces
    0 - Quitter""")
    choose = input("\nVotre action : ")
    if choose == "0":
        exit()
    elif choose == "1":
        run.home()
    elif choose == "2":
        search.home()
    elif choose == "3":
        print("Annonces")
    else:
        print("\nMerci de rentrer un choix valide !")
        time.sleep(2)
        main()


if __name__ == '__main__':
    database.create_db()
    print("Recherche d'emplois Scrape")
    print("By Florian DJERBI\tV0.1")
    main()
