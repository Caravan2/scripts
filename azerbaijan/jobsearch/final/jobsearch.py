import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from vacancy import Vacancy
from langdetect import detect
import datetime
from bson import ObjectId

import sys
# sys.path.append("/home/miriani/Desktop/main")


# https://hiro.ge/en/search?publish_up=2

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]

months = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
    }

t = time.localtime()
year = time.strftime("%Y", t)
year = int(year)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))


url = "http://jobsearch.az/"
page = requests.get(url)


for div in range(1, 2):
    try:

        # Position
        try:
            position = Selector(response=page).xpath('/html/body/table/tr[3]/td/table/tr/td[2]/table/tr/td[1]/table/tr[3]/td/table/tr[2]/td[1]/a[1]/text()').get()
            jobdb.insert_one({"miro" : position})
# /html/body/table/tr[3]/td/table/tr/td[2]/table/tr/td[1]/table/tr[3]/td/table/tr[2]/td[1]/a[1]
# /html/body/table/tr[3]/td/table/tr/td[2]/table/tr/td[1]/table/tr[3]/td/table/tr[3]/td[1]/a[1]
        except Exception as e:
            position = e


        data = {
            'position' : position
        }

        print(data)

    except Exception as e:
        print("Check div :", e)