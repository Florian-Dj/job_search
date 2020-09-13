# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup


def home():
    sql = """SELECT * FROM polls_ad
        LEFT JOIN polls_search ON polls_ad.site_id = polls_search.id
        WHERE status='not-read'"""
    results = db_select(sql)
    for result in results:
        if result[10] == "Linkedin":
            analysis_lk(result[4])


def analysis_lk(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('figcaption', class_="closed-job__flavor--closed")
    if ads:
        print("Annonce Expiré !", url)
    else:
        print("Annonce Bonne", url)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("../data.db")
        conn.execute('PRAGMA foreign_keys = 1')
        return conn
    except Error as e:
        print(e)
    return conn


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
