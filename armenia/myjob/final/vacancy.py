import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
# from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




months_en = {
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

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]


def Vacancy(link):
    print("request sent for Vacancy succesfully")
    url = link
    page = requests.get(url)

    # Category
    try:
        category = Selector(response=page).xpath('//*[@id="MainContentPlaceHolder_jobContainer"]/div[5]/div[1]/text()').get()
    except:
        category = ""

    # Ends
    try:
        ends = Selector(response=page).xpath('//*[@id="MainContentPlaceHolder_jobContainer"]/div[5]/div[3]/text()').get()
        ends = ends.split("/")
        deadline_day = int(ends[0])
        deadline_month = int(ends[1])
        deadline_year = int(ends[2])
    except:
        deadline_day = 0
        deadline_month = 0
        deadline_year = 0

    # Description
    try:
        description = Selector(response=page).xpath('//*[@id="MainContentPlaceHolder_jobContainer"]').get()
        description = remove_tags(description)
    except:
        description = ""


    # Email
    try:
        email = re.findall(r'[\w\.-]+@[\w\.-]+', description)[0]
        email = [email]
    except:
        email = []

    data = {
        "category" : category,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        'description' : description,
        "email" : email
    }


    print("Vacancy data is scraped")
    return data

# Vacancy('https://www.myjob.am/Announcement.aspx?jobId=57479')