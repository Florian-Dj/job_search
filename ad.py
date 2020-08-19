# -*- coding: utf-8 -*-

import main
import database
import time
import configparser

config = configparser.ConfigParser()


def home():
    sql = """SELECT status, COUNT(site_id) FROM ad
            GROUP BY status"""
    results = database.select(sql)
    i = 1
    print()
    for result in results:
        print("{} - {} ({})".format(i, result[0].replace("_", " ").title(), result[1]))
        i += 1
    print("0 - Retour")
    choose = input("\nChoisir votre action : ")
    choose = int(choose)
    if choose == 0:
        main.main()
    elif 1 <= choose <= len(results):
        choose_site(results[choose-1][0])
    else:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        home()


def choose_site(status):
    sql_total = """SELECT COUNT(id), status FROM ad WHERE status='{}'""".format(status)
    total = database.select(sql_total)[0]
    sql = """SELECT web, COUNT(site_id) FROM ad 
            INNER JOIN search ON ad.site_id = search.id
            WHERE status='{}'
            GROUP BY web""".format(status)
    results = database.select(sql)
    web = {"Leboncoin": 0, "Linkedin": 0, "Pole-Emploi": 0}
    for result in results:
        web[result[0]] = result[1]
    print("""
    1 - Pôle-Emploi\t({})
    2 - Linkedin\t({})
    3 - Leboncoin\t({})
    0 - Retour
    """.format( web["Pole-Emploi"], web["Linkedin"], web["Leboncoin"]))
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            home()
        elif choose == 1:
            list_search("Pole-Emploi", status, web["Pole-Emploi"])
        elif choose == 2:
            list_search("Linkedin", status, web["Linkedin"])
        elif choose == 3:
            list_search("Leboncoin", status, web["Leboncoin"])
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        home()


def list_search(web, status, nb):
    sql = """SELECT search.*, COUNT(ad.site_id), status FROM ad
            LEFT JOIN search ON ad.site_id = search.id
            WHERE web='{w}' AND status='{s}'
            GROUP BY search.id""".format(w=web, s=status)
    results = database.select(sql)
    print()
    print("1 - Tout {} ({})".format(" "*31, nb))
    i = 2
    for result in results:
        space = 35 - len(result[2])
        print("{} - {} {} ({})".format(i, result[2], " "*space, result[5]))
        i += 1
    print("0 - Retour\n")
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            choose_site(status)
        elif choose == 1:
            list_ad(web, ['*'], status, nb)
        elif 2 <= choose <= len(results):
            list_ad(web, results[choose-1], status, nb)
        else:
            print("Merci de rentrer une donné valide !")
            time.sleep(2)
            list_search(web, status, nb)
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        list_search(web, status, nb)


def list_ad(site, subject, status, nb):
    if subject[0] == '*':
        sql = """SELECT ad.id, ad.title, ad.description, ad.location, ad.link, search.web, status FROM ad
                LEFT JOIN search ON ad.site_id = search.id
                WHERE web='{}' AND status='{}'""".format(site, status)
        subject.extend(["2", "Tout"])
    else:
        sql = """SELECT ad.id, ad.title, ad.description, ad.location, ad.link, search.web, status FROM ad
                LEFT JOIN search ON ad.site_id = search.id
                WHERE site_id={} AND status='{}'""".format(subject[0], status)
    results = database.select(sql)
    if results:
        conn = database.connection()
        print("\n----- ({}) Annonces pour {} / {} -----\n".format(len(results), site, subject[2]))
        for result in results:
            if result[6] != "non_lu":
                config.read("config.ini")
                time.sleep(int(config["DEFAULT"]["cooldown_ad"]))
                print("\nLien : {}\nTitre : {}\nLieu : {}\nDescription : {}\n".format(result[4], result[1], result[3], result[2]))
            else:
                change_status(result, conn)
        conn.close()
    else:
        print("\n----- (0) Annonces pour {} / {} -----\n".format(site, subject[2]))
    time.sleep(2)
    list_search(site, status, nb)


def change_status(result, conn):
    print("\nLien : {}\nTitre : {}\t\tLieu : {}".format(result[4], result[1], result[3]))
    print("1 - Postulée \t 2 - Inadequate \t 3 - Expirée \t 4 - Rien")
    choose = input("Votre choix : ")
    print()
    choose = int(choose)
    text = ["postulée", "inadequate", "expirée"]
    if 1 <= choose <= 3:
        sql = """UPDATE ad SET status='{}' WHERE id={}""".format(text[choose-1], result[0])
        conn.execute(sql)
        conn.commit()
    elif choose == 4:
        pass
    else:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        change_status(result, conn)
