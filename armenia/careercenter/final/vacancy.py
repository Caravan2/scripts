import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geonames_en import Geonames




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
    # headers = {"Accept-Language": "en-US,en;q=0.5"}
    page = requests.get(url) #headers=headers)

    # Location
    try:
        location = Selector(response=page).xpath('/html/body/div[2]/table/tr[contains(., "Location:")]').get()
        location = location.split("<td>")[1].split("</td>")[0].replace("&amp;nbsp", " ")
        location = location.split(",")[0]
        location = [{'city': location, 'id': Geonames(location)}]
    except:
        location = [{'city': 'Yerevan', 'id': '616052'}]

    # Company url
    try:
        c_url = Selector(response=page).xpath('/html/body/div[2]/table/tr[contains(., "Company:")]').get()
        c_url = c_url.split('href="')[1].split('">')[0]
    except:
        c_url = ""

    # Vacancy Description
    try:
        description = Selector(response=page).xpath('/html/body/div[4]').get()
        description = remove_tags(description)
        description = description.strip()
        description = description.replace('&amp;nbsp', " ")
    except:
        description = ""
    try:
        if detect(description) == "et":
            try: 
                description_en = Translate(description)
            except:
                description_en = ""
            description_am = description
        else:
            description_en = description
            description_am = ""
    except:
        description_en = ""
        description_am = ""

    # Email
    try:
        email = Selector(response=page).xpath('//*[@id="job"]/a/@href').get()
        email = email.replace('mailto:', "")
        email = [email]
    except:
        email = []

    data = {
        "location" : location,
        "c_link" : c_url,
        "description_am" : description_am,
        "description_en" : description_en,
        "email" : email
    }

    # print(data)
    return data

# Vacancy('https://careercenter.am/en/get/job?slug=head-of-administration-and-technical-support-division-it-department-3')

