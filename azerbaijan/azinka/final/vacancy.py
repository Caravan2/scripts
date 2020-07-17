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


url = "https://azinka.az/job-type/contract/"
page = requests.get(url)

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")


def Vacancy(link):
    url = link
    page = requests.get(url)

    # Description
    try:
        description = Selector(response=page).xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[1]').get()
        description = remove_tags(description)
        if detect(description) == "et":
            try: 
                description_en = Translate(description)
            except:
                description_en = ""
            description_az = description
        else:
            description_en = description
            description_az = ""
    except:
        description_en = ""
        description_az = ""


    # email
    try:
        driver.get(url)
        email = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[1]').text
        email = re.findall(r'[\w\.-]+@[\w\.-]+', email)
    except:
        email = []

    data = {
        "description_az" : description_az,
        "description_en" : description_en,
        "email" : email
    }

    # print(data)
    return data

# Vacancy("https://azinka.az/jobs/3710/")