# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import polls.scrape
import polls.database as db


def select_ads():
    sql = """SELECT * FROM polls_ad
        LEFT JOIN polls_search ON polls_ad.site_id = polls_search.id
        WHERE status='not-read'"""
    results = db.db_select(sql)
    conn = db.db_connection()
    for result in results:
        print(result[4])
        if result[8] == "Linkedin":
            analysis_lk(result[4], result[0], conn)
        elif result[8] == "Pole-Emploi":
            analysis_pe(result[4], result[0], conn)
    db.db_close(conn)
    polls.scrape.data_status()


def analysis_lk(url, id_ad, conn):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('figcaption', class_="closed-job__flavor--closed")
    if ads:
        sql = """UPDATE polls_ad SET status='expired' WHERE id={}""".format(id_ad)
        db.injection_sql(conn, sql)


def analysis_pe(url, id_ad, conn):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('meta', content='Offre non disponible')
    if ads:
        sql = """UPDATE polls_ad SET status='expired' WHERE id={}""".format(id_ad)
        db.injection_sql(conn, sql)


if __name__ == '__main__':
    select_ads()
