# -*- coding: utf-8 -*-

import main
import database
import time
import configparser

config = configparser.ConfigParser()


def home():
    print("""
    1 - Pôle-Emploi
    2 - Linkedin
    3 - Leboncoin
    0 - Retour
    """)
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            main.main()
        elif choose == 1:
            list_search("Pole-Emploi")
        elif choose == 2:
            list_search("Linkedin")
        elif choose == 3:
            list_search("Leboncoin")
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        home()


def list_search(web):
    sql = """SELECT * FROM search WHERE web='{}'""".format(web)
    results = database.select(sql)
    i = 1
    print()
    for result in results:
        print("{} - {}".format(i, result[2]))
        i += 1
    print("0 - Retour\n")
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            home()
        elif 1 <= choose <= len(results):
            list_ad(web, results[choose-1])
        else:
            print("Merci de rentrer une donné valide !")
            time.sleep(2)
            list_search(web)
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        list_search(web)


def list_ad(site, subject):
    config.read("config.ini")
    sql = """SELECT ad.title, ad.description, ad.location, ad.link, search.web FROM ad
            LEFT JOIN search ON ad.site_id = search.id
            WHERE site_id={}""".format(subject[0])
    results = database.select(sql)
    if results:
        print("\n----- ({}) annonces pour {} / {} -----\n".format(len(results), site, subject[2]))
        for result in results:
            time.sleep(int(config["DEFAULT"]["cooldown_ad"]))
            print("\nLien : {}\nTitre : {}\nLieu : {}\nDescription : {}\n".format(result[3], result[0], result[2], result[1]))
    else:
        print("\n----- (0) annonces pour {} / {} -----\n".format(site, subject[2]))
    time.sleep(2)
    home()
