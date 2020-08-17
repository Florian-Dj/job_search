# -*- coding: utf-8 -*-

import time
import database
import requests
from bs4 import BeautifulSoup
import playsound
import datetime
import configparser

config = configparser.ConfigParser()
web = ""


def home():
    while True:
        config.read("config.ini")
        sql = """SELECT * FROM search"""
        results = database.select(sql)
        datetime_now = datetime.datetime.now().strftime("%H:%M:%S")
        print("\n======== {} ========\n".format(datetime_now))
        for result in results:
            parse(result)
        time.sleep(int(config["DEFAULT"]["cooldown_scraping"]))


def parse(result):
    if result[1] == "Pole-Emploi":
        ep(result)
    elif result[1] == "Linkedin":
        lk(result)
    elif result[1] == "Leboncoin":
        lb(result)
    else:
        print("Error")


def ep(result):
    req = requests.get(result[3])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result")
    conn = database.connection()
    for ad in ads:
        link = "{}{}".format(result[4], ad.a['href'])
        title = ad.h2.text.replace("\n", "")
        location = ad.find('p', class_="subtext").text.replace("\n", "")
        description = ad.find('p', class_="description").text.replace('"', "")
        sql = """INSERT INTO ad (site_id, title, description, location, link) VALUES ({}, "{}", "{}", "{}", "{}")"""\
            .format(result[0], title, description, location, link)
        injection_sql(conn, sql, link, title, result)
    close(conn)


def lk(result):
    req = requests.get(result[3])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result-card")
    conn = database.connection()
    for ad in ads:
        link = ad.a['href'].split("?")[0]
        title = ad.h3.text
        location = ad.find('span', class_="job-result-card__location").text
        sql = """INSERT INTO ad (site_id, title, location, link) VALUES ({}, "{}", "{}", "{}")"""\
            .format(result[0], title, location, link)
        injection_sql(conn, sql, link, title, result)
    close(conn)


def lb(result):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = requests.get(result[3], headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="_3DFQ-")
    conn = database.connection()
    for ad in ads:
        link = "{}{}".format(result[4], ad.a['href'])
        title = ad.find("p", class_="_2tubl").text
        location = ad.find('p', class_="_2qeuk").text
        sql = """INSERT INTO ad (site_id, title, location, link) VALUES ({}, "{}", "{}", "{}")"""\
            .format(result[0], title, location, link)
        injection_sql(conn, sql, link, title, result)
    close(conn)


def injection_sql(conn, sql, link, title, result):
    try:
        data = conn.cursor()
        data.execute(sql)
        playsound.playsound("sound/alert.mp3", False)
        global web
        if "{} / {}".format(result[1], result[2]) != web:
            web = "{} / {}".format(result[1], result[2])
            print("\n----- {} -----\n".format(web))
        print("Lien : {}\nTitre : {}".format(link, title))
        print()
        time.sleep(int(config["DEFAULT"]["cooldown_new_ad"]))
    except conn.IntegrityError:
        pass
    except conn.Error as e:
        print(sql)
        print(e)


def close(conn):
    try:
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)
