# -*- coding: utf-8 -*-

import time
import database
import requests
from bs4 import BeautifulSoup
import playsound
import datetime


def home():
    while True:
        sql = """SELECT * FROM search"""
        results = database.select(sql)
        datetime_now = datetime.datetime.now().strftime("%H:%M:%S")
        print("\n---------- {} ----------\n".format(datetime_now))
        for result in results:
            parse(result)
        time.sleep(300)


def parse(result):
    req = requests.get(result[3])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result")
    conn = database.connection()
    for ad in ads:
        link = "{}{}".format(result[4], ad.a['href'])
        title = ad.h2.text.replace("\n", "")
        location = ad.find('p', class_="subtext").text.replace("\n", "")
        description = ad.find('p', class_="description").text
        sql = """INSERT INTO ad (site_id, title, description, location, link) VALUES ({}, "{}", "{}", "{}", "{}")"""\
            .format(result[0], title, description, location, link)
        try:
            data = conn.cursor()
            data.execute(sql)
            playsound.playsound("alert.mp3", False)
            print("\nLien : {}\nTitre : {}\nLieu : {}\nDescription : {}\n".format(link, title, location, description))
            time.sleep(3)
        except conn.IntegrityError:
            pass
        except conn.Error as e:
            print(e)
    try:
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)
