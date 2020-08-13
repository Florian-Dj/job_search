# -*- coding: utf-8 -*-

import time
import main
import database
import requests
from bs4 import BeautifulSoup


def home():
    sql = """SELECT * FROM site GROUP BY web"""
    results = database.select(sql)
    for result in results:
        parse(result)
    time.sleep(2)
    main.main()


def parse(result):
    print(result)
    req = requests.get(result[3])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result")
    for ad in ads:
        link = ad.a['href']
        title = ad.h2.text.replace("\n", "")
        location = ad.find('p', class_="subtext").text.replace("\n", "")
        description = ad.find('p', class_="description").text
        print("Lien : {}\nTitre : {}\nLieu : {}\nDescription : {}".format(link, title, location, description))
        print("\n\n")
