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
            run()
        elif choose == 2:
            add_link()
        elif choose == 3:
            delete_link()
        elif choose == 4:
            list_link()
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        main()


def add_link():
    link = input("URL de la recherche : ")
    print("""
    1 - Pole-Emploi
    2 - Linkedin
    3 - Leboncoin
    0 - Retour""")
    web = input("De quel site provient la recherche ? ")
    if web == "1":
        web = "Pole-Emploi"
    elif web == "2":
        web = "Linkedin"
    elif web == "3":
        web = "Leboncoin"
    else:
        print("Ici")
        main()
    subject = input("Quel est le titre de la recherche ? ")
    conn = database.connection()
    sql = """INSERT INTO site (web, subject, link) VALUES ('{}', '{}', '{}')""".format(web, subject, link)
    try:
        data = conn.cursor()
        data.execute(sql)
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)
    time.sleep(3)
    main()


def list_link():
    sql = """SELECT * FROM site"""
    results = database.select(sql)
    for result in results:
        print(result)
    time.sleep(2)
    main()


if __name__ == '__main__':
    database.create_db()
    main()
