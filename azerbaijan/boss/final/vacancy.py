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
    "Yanvar": "01",
    "Fevral": "02",
    "Mart": "03",
    "Aprel": "04",
    "May": "05",
    "İyun": "06",
    "İyul": "07",
    "Avqust": "08",
    "Sentyabr": "09",
    "Oktyabr": "10",
    "Noyabr": "11",
    "Dekabr": "12"
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
    
    # Age
    try:
        age = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[5]/div/div[1]/ul/li[2]/div[2]/text()').get()
    except:
        age = ""

    # Education
    try:
        education = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[5]/div/div[1]/ul/li[3]/div[2]/text()').get()
    except:
        education = ""

    # Experience
    try:
        experience = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[5]/div/div[1]/ul/li[4]/div[2]/text()').get()
    except:
        experience = ""

    # Published
    try:
        published = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[5]/div/div[1]/ul/li[5]/div[2]/text()').get()
        published = published.split(",")
        publish_day = int(published[0].split(" ")[1])
        publish_month = int(months[published[0].split(" ")[0]])
        publish_year = int(published[1].strip())
    except Exception as e:
        publish_day = e
        publish_month = 0
        publish_year = 0

    # Ends
    try:
        ends = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[5]/div/div[1]/ul/li[6]/div[2]/text()').get()
        ends = ends.split(",")
        deadline_day = int(ends[0].split(" ")[1])
        deadline_month = int(months[ends[0].split(" ")[0]])
        deadline_year = int(ends[1].strip())
    except Exception as e:
        deadline_day = 0
        deadline_month = 0
        deadline_year = 0

    # Phone
    try:
        phone = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[5]/div/div[2]/ul/li[1]/div[2]').get()
        phone = remove_tags(phone)
        phone = phone.split("(")
        if len(phone) == 2:
            phone = phone[1].replace(")", "")
            phone = phone.replace("-", "")
            phone = phone.replace(" ", "")
            phones = [{"country_code" : "994", "number" : phone}]
        elif len(phone) == 3:
            phones = []
            number1 = phone[1].replace(")", "")
            number1 = number1.replace("-", "")
            number1 = number1.replace(" ", "")
            phones.append({"country_code" : "994", "number" : number1})
            number2 = phone[2].replace(")", "")
            number2 = number2.replace("-", "")
            number2 = number2.replace(" ", "")
            phones.append({"country_code" : "994", "number" : number2})
        else:
            phones = []
    except Exception as e:
        phones = []

    # Email
    try:
        driver.get(url)
        email = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[5]/div/div[2]/ul/li[2]/div[2]/a').text
        email = [email]
    except:
        email = []

    # Description
    try:
        description = Selector(response=page).xpath('/html/body/div[3]/div[1]/div[6]').get()
        description = remove_tags(description)
    except:
        description = ""
    try:
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



    data = {
        "age" : age,
        "education" : education,
        "experience" : experience,
        "publish_day" : publish_day,
        "publish_month" : publish_month,
        "publish_year" : publish_year,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        "phone" : phones,
        "email" : email,
        "description_az" : description_az,
        "description_en" : description_en,
    }

    # print(data)
    return data

# Vacancy('https://boss.az/vacancies/161045')