# -*- coding: utf-8 -*-

import time
import main
import database


def home():
    print("""
    1 - Ajouter Lien
    2 - Supprimer Lien
    3 - Liste Lien
    0 - Retour
    """)
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            main.main()
        elif choose == 1:
            add_link()
        elif choose == 2:
            delete_link()
        elif choose == 3:
            list_link()
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        home()


def add_link():
    link = input("URL de la recherche : ")
    print("""
    1 - Pole-Emploi
    2 - Linkedin
    3 - Leboncoin
    0 - Retour\n""")
    web = input("De quel site provient la recherche ? ")
    if web == "1":
        web = "Pole-Emploi"
    elif web == "2":
        web = "Linkedin"
    elif web == "3":
        web = "Leboncoin"
    else:
        home()
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
    home()


def delete_link():
    sql = """SELECT * FROM site"""
    results = database.select(sql)
    print()
    for result in results:
        print("{} - {}  {}".format(result[0], result[1], result[2]))
    print("0 - Retour\n")
    choose = int(input("Quel cherche voulez-vous supprimer ? "))
    if choose == 0:
        home()
    if 1 <= choose <= len(results):
        print(results[choose-1])
    time.sleep(2)
    home()


def list_link():
    sql = """SELECT * FROM site"""
    results = database.select(sql)
    for result in results:
        print()
        print("Site : {}".format(result[1]))
        print("Poste : {}".format(result[2]))
        print("Lien : {}".format(result[3]))
    time.sleep(2)
    home()
