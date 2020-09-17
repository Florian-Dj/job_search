# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup

title_word = ["stagiaire", "freelance", "stage", "alternance"]
description = ""


def home():
    sql = """SELECT * FROM polls_search"""
    results = db_select(sql)
    for result in results:
        parse(result)


def parse(result):
    if result[3] == "Pole-Emploi":
        ep(result)
    elif result[3] == "Linkedin":
        lk(result)
    elif result[3] == "Leboncoin":
        lb(result)
    else:
        print("Error")


def ep(result):
    req = requests.get(result[2])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result")
    conn = db_connection()
    for ad in ads:
        link = "{}{}".format("https://candidat.pole-emploi.fr", ad.a['href'])
        title = ad.h2.text.replace("\n", "").capitalize()
        location = ad.find('p', class_="subtext").text.replace("\n", "")
        description = ad.find('p', class_="description").text.replace('"', "")
        check_status(result[0], title, location, link, description, conn)
    db_close(conn)


def lk(result):
    req = requests.get(result[2])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result-card")
    conn = db_connection()
    for ad in ads:
        link = ad.a['href'].split("?")[0]
        title = ad.h3.text.capitalize()
        location = ad.find('span', class_="job-result-card__location").text
        check_status(result[0], title, location, link, description, conn)
    db_close(conn)


def lb(result):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = requests.get(result[2], headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="_3DFQ-")
    conn = db_connection()
    for ad in ads:
        link = "{}{}".format("https://www.leboncoin.fr", ad.a['href'])
        title = ad.find("p", class_="_2tubl").text.capitalize()
        location = ad.find('p', class_="_2qeuk").text
        check_status(result[0], title, location, link, description, conn)
    db_close(conn)


def check_status(site_id, title, location, link, description, conn):
    if any(ele in title.lower() for ele in title_word):
        status = "other"
    else:
        status = "not-read"
    sql = """INSERT INTO polls_ad (site_id, title, location, description, link, status)
            VALUES ({}, "{}", "{}", "{}", "{}", "{}")""".format(site_id, title, location, description, link, status)
    injection_sql(conn, sql)


def injection_sql(conn, sql):
    try:
        data = conn.cursor()
        data.execute(sql)
    except conn.IntegrityError:
        pass
    except conn.Error as e:
        print(e)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("../data.db")
        conn.execute('PRAGMA foreign_keys = 1')
        return conn
    except Error as e:
        print(e)
    return conn


def db_close(conn):
    try:
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)


def db_select(sql):
    try:
        conn = db_connection()
        c = conn.cursor()
        c.execute(sql)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)


if __name__ == '__main__':
    home()
