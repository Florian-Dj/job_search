# -*- coding: utf-8 -*-

import time
import main
import database


def home():
    print("""
    1 - Ajouter Recherche
    2 - Supprimer Recherche
    3 - Liste Recherche
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
    link_ad = ""
    link = input("URL de la recherche : ")
    print("""
    1 - Pole-Emploi
    2 - Linkedin
    3 - Leboncoin
    0 - Retour\n""")
    web = input("De quel site provient la recherche ? ")
    if web == "1":
        web = "Pole-Emploi"
        link_ad = "https://candidat.pole-emploi.fr"
    elif web == "2":
        web = "Linkedin"
    elif web == "3":
        web = "Leboncoin"
        link_ad = "https://www.leboncoin.fr"
    else:
        home()
    subject = input("Quel est le titre de la recherche ? ")
    conn = database.connection()
    sql = """INSERT INTO search (web, subject, link_search, link_ad) VALUES ('{}', '{}', '{}', '{}')"""\
        .format(web, subject, link, link_ad)
    try:
        data = conn.cursor()
        data.execute(sql)
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)
    home()


def delete_link():
    conn = None
    sql = """SELECT * FROM search"""
    results = database.select(sql)
    print()
    i = 1
    for result in results:
        print("{} - {}  {}".format(i, result[1], result[2]))
        i += 1
    print("0 - Retour\n")
    choose = int(input("Quel cherche voulez-vous supprimer ? "))
    if choose == 0:
        home()
    if 1 <= choose <= len(results):
        print("{}  {} Supprimé".format(results[choose-1][2], results[choose-1][1]))
        conn = database.connection()
        sql = """DELETE FROM search WHERE id={}""".format(results[choose-1][0])
    try:
        data = conn.cursor()
        data.execute(sql)
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)
    time.sleep(2)
    home()


def list_link():
    sql = """SELECT * FROM search"""
    results = database.select(sql)
    for result in results:
        print()
        print("Site : {}".format(result[1]))
        print("Poste : {}".format(result[2]))
        print("Lien : {}".format(result[3]))
    time.sleep(2)
    home()
