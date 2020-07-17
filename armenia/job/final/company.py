import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
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


def Company_Info(link):
    url = link
    page = requests.get(url)

    # Industry
    try:
        address = Selector(response=page).xpath('/html/body/div[3]/div[1]/div/div/div/div[3]/div/div[1]/p/span[2]/text()').get()
    except:
        address = ""


    try:
        phone = Selector(response=page).xpath('/html/body/div[3]/div[1]/div/div/div/div[3]/div/div[3]/p/a/text()').get()
        number = phone.replace("+", "")
        number = number.replace("374", "")
        number = number.replace("tel: ", "")
        phone = [{"country_code" : "374", "number" : number}]
    except:
        phone = []


    try:
        website = Selector(response=page).xpath('/html/body/div[3]/div[1]/div/div/div/div[3]/div/div[2]/p/a/@href').get()
        if "+" in website or "374" in website:
            phone = website
            number = phone.replace("+", "")
            number = number.replace("374", "")
            number = number.replace("tel: ", "")
            phone = [{"country_code" : "374", "number" : number}]
            website = []
        elif website is None:
            website = []
        else:
            website = [website]
    except:
        website = []

    try:
        description = Selector(response=page).xpath('/html/body/div[3]/div[2]/div/div/div/div[2]/div/div/p/text()').get()
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
        description_en = description
        description_am = ""

    data = {
        "address" : address,
        "phone" : phone,
        "website" : website,
        "description_am" : description_am,
        "description_en" : description_en,

    }

    # print(data)
    return data

# Company_Info('https://job.am/en/company/18390/san-holding-spe')