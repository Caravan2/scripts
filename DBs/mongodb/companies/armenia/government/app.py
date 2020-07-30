import requests, pymongo
import re, os, io
import time
from PIL import Image
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from langdetect import detect
from bson import ObjectId
import datetime
import sys
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from translator import Translate

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Test"]
government = mydb["government"]


for i in range(20296, 2000000):
    url = f"https://www.e-register.am/en/companies/{i}"

    page = requests.get(url)

    name_am = Selector(response=page).xpath('//*[@id="page"]/div[1]/text()').get()
    if name_am is None:
        print("No company on:", i)
        continue

    name_en = Translate(name_am)

    registration_number = Selector(response=page).xpath('//*[@id="page"]/table[3]/tr[2]/td[2]/text()').get()

    foundation_date = registration_number.split("/")[1].strip()

    registration_number = registration_number.split("/")[0].strip()

    tax_id = Selector(response=page).xpath('//*[@id="page"]/table[3]/tr[3]/td[2]/text()').get()

    z_code = Selector(response=page).xpath('//*[@id="page"]/table[3]/tr[4]/td[2]/text()').get()

    data = {
        "name" : name_en,
        "name_am" : name_am,
        "registration_number" : registration_number,
        "foundation_date" : foundation_date,
        "tax_id" : tax_id,
        "z_code" : z_code,
        "url" : url
    }

    government.insert_one(data)
    print(data)