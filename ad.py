# -*- coding: utf-8 -*-

import main
import database
import time


def home():
    print("""
    1 - Pôle-Emploi
    2 - Linkedin
    3 - Leboncoin
    4 - Monster
    0 - Retour
    """)
    choose = input("Votre action : ")
    try:
        choose = int(choose)
        if choose == 0:
            main.main()
        elif choose == 1:
            list_ad("Pole-Emploi")
        elif choose == 2:
            list_ad("Linkedin")
        elif choose == 3:
            list_ad("Leboncoin")
        elif choose == 4:
            list_ad("Monster")
    except ValueError:
        print("Merci de rentrer une donné valide !")
        time.sleep(2)
        home()


def list_ad(site):
    sql = """SELECT ad.title, ad.description, ad.location, ad.link, search.web FROM ad
            LEFT JOIN search ON ad.site_id = search.id
            WHERE web='{}'""".format(site)
    results = database.select(sql)
    print("\n----- Toutes les annonces de {} ({}) -----\n".format(site, len(results)))
    for result in results:
        time.sleep(5)
        print("\nLien : {}\nTitre : {}\nLieu : {}\nDescription : {}\n".format(result[3], result[0], result[2], result[1]))
    time.sleep(2)
    home()
