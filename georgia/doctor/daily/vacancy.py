import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_ka import Geonames
from translator import Translate
from langdetect import detect
import datetime
from bson import ObjectId


def Vacancy_info(url):
    print(url)
    page = requests.get(url)


    # Description
    try:
        description = Selector(response=page).xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]').get()
        description = remove_tags(description)
        description = description.rstrip()
        description = description.lstrip()
        description = re.sub(r"\s+", " ", description)
        print(description)
    except:
        description = ""
    if detect(description) == "ru":
        description_ru = description
        description_en = Translate(description)
        description_ka = ""
    elif detect(description) == "et":
        description_ru = ""
        try: 
            description_en = Translate(description)
        except:
            description_en = ""
        description_ka = description
    else:
        description_ru = ""
        description_en = description
        description_ka = ""


    # Email
    try:
        email = Selector(response=page).xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div/a/@href').get()
        email = email.replace("mailto:", "")
    except:
        email = ""


    # Location
    try:
        location = Selector(response=page).xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/span/text()').get()
        location_id = []
        try:
            location_id.append({"city" : f"{location}", "id" : f"{Geonames(location)}"})
        except:
            location_id.append({"city" : f"{location}", "id" : "611717"})
    except:
        location_id = [{"city" : "Tbilisi", "id" : "611717"}]


    # Category
    try:
        category = Selector(response=page).xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/span[1]/text()').get()
    except:
        category = ""

    # Stack
    try:
        stack = Selector(response=page).xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/text()').get()
        if "სრული განაკვეთი" in stack:
            stack = "Full-Stack"
    except:
        stack = ""

    data = {
        "description_en" : description_en,
        "description_ka" : description_ka,
        "description_ru" : description_ru,
        "email" : email,
        "location" : location_id,
        "category" : category,
        "stack" : stack
    }
    
    print("Vacancy Scraped Succesfully")
    return data

