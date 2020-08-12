# -*- coding: utf-8 -*-

import time
import main
import database
# import requests
# from bs4 import BeautifulSoup


def home():
    sql = """SELECT * FROM site GROUP BY web"""
    results = database.select(sql)
    for result in results:
        parse(result[3])
    time.sleep(2)
    main.main()


def parse(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    name = soup.find_all(class_="result")
    print(name)
