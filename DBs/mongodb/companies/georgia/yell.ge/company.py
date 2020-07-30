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
# from config import config

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Companies"]
mycol = mydb["yell.ge"]


# driver.implicitly_wait(2)

def Company_Info(link):
    print("Trying to get Identification Number")
    url = link
    page = requests.get(url)

    vat = Selector(response=page).xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/div[contains(., "Identification")]/span[2]/text()').get()
    try:
        vat = vat.strip()
    except:
        vat = None
    data = {
        "vat" : vat
    }

    # print(data)
    return data

# Company_Info("https://www.yell.ge/company.php?lan=eng&id=139568")
# print(main)