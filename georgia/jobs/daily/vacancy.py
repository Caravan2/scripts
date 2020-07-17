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
    url = url.replace("/en/", "/ge/")
    print(url)
    page = requests.get(url)


    # Description
    try:
        description = Selector(response=page).xpath('//*[@id="job"]/table/tr[1]/td/table[2]').get()
        description = remove_tags(description)
        description = description.rstrip()
        description = description.lstrip()
        description = description.replace('*', "")
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
        email = re.findall(r'[\w\.-]+@[\w\.-]+', description)
        email = email[0]
    except:
        email = ""

    data = {
        "description_ka" : description_ka,
        "description_ru" : description_ru,
        "description_en" : description_en,
        "email" : email
    }
    return data

# Vacancy_info("https://jobs.ge/en/?view=jobs&id=268715")