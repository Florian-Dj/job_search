# -*- coding: utf-8 -*-

import time
import sqlite3
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup
import playsound
import configparser

config = configparser.ConfigParser()
web = ""
data_name = "data.db"


def home():
    config.read("config.ini")
    sql = """SELECT * FROM polls_search"""
    results = db_select(sql)
    for result in results:
        parse(result)


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
    conn = db_connection()
    for ad in ads:
        link = "{}{}".format(result[4], ad.a['href'])
        title = ad.h2.text.replace("\n", "")
        location = ad.find('p', class_="subtext").text.replace("\n", "")
        description = ad.find('p', class_="description").text.replace('"', "")
        sql = """INSERT INTO polls_ad (site_id, title, description, location, link, status) VALUES ({}, "{}", "{}", "{}", "{}", "{}")"""\
            .format(result[0], title, description, location, link, "not-read")
        injection_sql(conn, sql, result)
    db_close(conn)


def lk(result):
    req = requests.get(result[3])
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="result-card")
    conn = db_connection()
    for ad in ads:
        link = ad.a['href'].split("?")[0]
        title = ad.h3.text
        location = ad.find('span', class_="job-result-card__location").text
        sql = """INSERT INTO polls_ad (site_id, title, location, link, status) VALUES ({}, "{}", "{}", "{}", "{}")"""\
            .format(result[0], title, location, link, "not-read")
        injection_sql(conn, sql, result)
    db_close(conn)


def lb(result):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = requests.get(result[3], headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find_all('li', class_="_3DFQ-")
    conn = db_connection()
    for ad in ads:
        link = "{}{}".format(result[4], ad.a['href'])
        title = ad.find("p", class_="_2tubl").text
        location = ad.find('p', class_="_2qeuk").text
        sql = """INSERT INTO polls_ad (site_id, title, location, link, status) VALUES ({}, "{}", "{}", "{}", "{}")"""\
            .format(result[0], title, location, link, "not-read")
        injection_sql(conn, sql, result)
    db_close(conn)


def injection_sql(conn, sql, result):
    try:
        data = conn.cursor()
        data.execute(sql)
        global web
        if "{} / {}".format(result[1], result[2]) != web:
            web = "{} / {}".format(result[1], result[2])
    except conn.IntegrityError as u:
        pass
    except conn.Error as e:
        print(e)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect(data_name)
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
