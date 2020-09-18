# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import database as db

title_word = ["stagiaire", "freelance", "stage", "alternance"]
description = ""


def select_search():
    sql = """SELECT * FROM polls_search"""
    results = db.db_select(sql)
    for result in results:
        parse(result)


def parse(result):
    if result[3] == "Pole-Emploi":
        ep(result)
    elif result[3] == "Linkedin":
        lk(result)
    else:
        print("Error - {}".format(result))


def ep(result):
    req = requests.get(result[2])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result")
    conn = db.db_connection()
    for ad in ads:
        link = "{}{}".format("https://candidat.pole-emploi.fr", ad.a['href'])
        title = ad.h2.text.replace("\n", "").capitalize()
        location = ad.find('p', class_="subtext").text.replace("\n", "")
        description = ad.find('p', class_="description").text.replace('"', "")
        check_status(result[0], title, location, link, description, conn)
    db.db_close(conn)


def lk(result):
    req = requests.get(result[2])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result-card")
    conn = db.db_connection()
    for ad in ads:
        link = ad.a['href'].split("?")[0]
        title = ad.h3.text.capitalize()
        location = ad.find('span', class_="job-result-card__location").text
        check_status(result[0], title, location, link, description, conn)
    db.db_close(conn)


def lb(result):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = requests.get(result[2], headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="_3DFQ-")
    conn = db.db_connection()
    for ad in ads:
        link = "{}{}".format("https://www.leboncoin.fr", ad.a['href'])
        title = ad.find("p", class_="_2tubl").text.capitalize()
        location = ad.find('p', class_="_2qeuk").text
        check_status(result[0], title, location, link, description, conn)
    db. db_close(conn)


def check_status(site_id, title, location, link, description, conn):
    if any(ele in title.lower() for ele in title_word):
        status = "other"
    else:
        status = "not-read"
    sql = """INSERT INTO polls_ad (site_id, title, location, description, link, status)
            VALUES ({}, "{}", "{}", "{}", "{}", "{}")""".format(site_id, title, location, description, link, status)
    db.injection_sql(conn, sql)


def data_status():
    sql = """SELECT web FROM polls_search GROUP BY web"""
    results = db.db_select(sql)
    list_web = {}
    for result in results:
        list_web[result[0]] = {}
    list_status = {"not-read": 0, "applied": 0, "inadequate": 0, "expired": 0, "other": 0}
    for web in list_web:
        list_web[web].update(list_status)
    sql = """SELECT status, COUNT(status), polls_search.web FROM polls_ad
        LEFT JOIN polls_search ON polls_ad.site_id = polls_search.id
        GROUP BY status, polls_search.web"""
    results = db.db_select(sql)
    for result in results:
        list_web[result[2]][result[0]] = result[1]
    conn = db.db_connection()
    for data in list_web:
        total = list_web[data]["not-read"] + list_web[data]["applied"] + list_web[data]["inadequate"] + list_web[data]["expired"] + list_web[data]["other"]
        sql = """INSERT INTO polls_stat (web, not_read, applied, inadequate, expired, other, total)
                VALUES ('{}', {}, {}, {}, {}, {}, {})"""\
        .format(data, list_web[data]["not-read"], list_web[data]["applied"], list_web[data]["inadequate"], list_web[data]["expired"], list_web[data]["other"], total)
        insert = db.injection_sql(conn, sql)
        if insert == "update":
            sql = """UPDATE polls_stat SET not_read={}, applied={}, inadequate={}, expired={}, other={}, total={}
                    WHERE web = '{}'"""\
                .format(list_web[data]["not-read"], list_web[data]["applied"], list_web[data]["inadequate"], list_web[data]["expired"], list_web[data]["other"], total, data)
            db.injection_sql(conn, sql)
    db.db_close(conn)


if __name__ == '__main__':
    select_search()
    data_status()
