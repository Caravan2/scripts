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
from pprint import pprint as pp
# from config import config

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Companies"]
official = mydb["companyinfo.ge"]


# driver.implicitly_wait(2)

for i in range(1, 200000):
    try:
        en = "en"
        ka = "ka"

        url = f"https://www.companyinfo.ge/{en}/corporations/{i}"
        
        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"}

        page = requests.get(url, headers=headers)
        
        # print(page.content)

        # Name
        try:
            name = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[1]/td[2]/text()').get()
        except:
            name = ""

        if name is None or name == "":
            f = open("check.txt", "a")
            f.write(f"id: {i} was Not captured\n")
            continue


        # ID
        try:
            _id = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[2]/td[2]/text()').get()
        except:
            _id = ""


        # Legal Form
        try:
            legal_form = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[3]/td[2]/text()').get()
        except:
            legal_form = ""


        # Foundation date
        try:
            foundation_date = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[4]/td[2]/text()').get()
        except:
            foundation_date = ""


        # Source
        try:
            source = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[5]/td[2]/a/@href').get()
        except:
            source = ""


        # Address
        try:
            address = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[6]/td[2]/text()').get()
        except:
            address = ""
        

        # Email
        try:
            email = Selector(response=page).xpath('//*[@id="corporation-attributes"]/tbody/tr[7]/td[2]/text()').get()
        except:
            email = ""

        # Get name in georgian
        page2 = requests.get(f"https://www.companyinfo.ge/{ka}/corporations/{i}", headers=headers)

        name_ka = Selector(response=page2).xpath('//*[@id="corporation-attributes"]/tbody/tr[1]/td[2]/text()').get()

        data = {
            "name_en" : name,
            "name_ka" : name_ka,
            "identification_number" : _id,
            "legal_form" : legal_form,
            "foundation_date" : foundation_date,
            "primary_source" : url,
            "secondary_source" : source,
            "address" : address,
            "email" : email
        }

        official.insert_one(data)
        pp(data)
    except Exception as e:
        f = open("log.txt", "a")
        f.write(f"id: {i} was interrupted by Error: {e} \n")