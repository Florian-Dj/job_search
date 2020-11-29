# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import scripts.database as db
from scripts import log

title_word = ["stagiaire", "freelance", "stage", "alternance"]
description = ""


def select_search():
    sql = """SELECT * FROM polls_search"""
    results = db.db_select(sql)
    if results:
        for result in results:
            parse(result)


def parse(result):
    if result[3] == "Pole-Emploi":
        ep(result)
    elif result[3] == "Linkedin":
        lk(result)
    else:
        logging.warning("Scrape parse {}".format(result))


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


def check_status(site_id, title, location, link, description, conn):
    if any(ele in title.lower() for ele in title_word):
        status = "other"
    else:
        status = "not-read"
    sql = """INSERT INTO polls_ad (site_id, title, location, description, link, status)
            VALUES ({}, "{}", "{}", "{}", "{}", "{}")""".format(site_id, title, location, description, link, status)
    db.injection_sql(conn, sql)


if __name__ == '__main__':
    logging = log.log_sql()
    logging.info("Run script scrape")
    select_search()
    logging.info("Finish script scrape")
