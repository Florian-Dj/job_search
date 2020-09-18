# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup
import polls.scrape


def home():
    sql = """SELECT * FROM polls_ad
        LEFT JOIN polls_search ON polls_ad.site_id = polls_search.id
        WHERE status='not-read'"""
    results = db_select(sql)
    conn = db_connection()
    print("Analyse de {} annonces non lues".format(len(results)))
    for result in results:
        if result[8] == "Linkedin":
            analysis_lk(result[4], result[0], conn)
        elif result[8] == "Pole-Emploi":
            analysis_pe(result[4], result[0], conn)
    db_close(conn)
    polls.scrape.data_status()


def analysis_lk(url, id_ad, conn):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('figcaption', class_="closed-job__flavor--closed")
    if ads:
        sql = """UPDATE polls_ad SET status='expired' WHERE id={}""".format(id_ad)
        injection_sql(conn, sql)


def analysis_pe(url, id_ad, conn):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('meta', content='Offre non disponible')
    if ads:
        sql = """UPDATE polls_ad SET status='expired' WHERE id={}""".format(id_ad)
        injection_sql(conn, sql)


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


def injection_sql(conn, sql):
    try:
        data = conn.cursor()
        data.execute(sql)
    except conn.Error as e:
        print(e)


def db_close(conn):
    try:
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)


if __name__ == '__main__':
    home()
