# -*- coding: utf-8 -*-

import time
import database


def main():
    print("""
    1 - Run
    2 - Ajouter Lien
    3 - Supprimer Lien
    4 - Liste Lien
    0 - Quitter""")
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            exit()
        elif choose == 1:
            add_link()
        elif choose == 2:
            delete_link()
        elif choose == 3:
            list_link()
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        main()


# def list_link():


if __name__ == '__main__':
    database.create_db()
    main()
