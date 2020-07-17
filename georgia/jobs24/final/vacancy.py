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
# /html/body/table[2]/tbody/tr/td[2]/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div[7]
    # Description
    try:
        description = Selector(response=page).xpath('/html/body/table[2]/tr/td[2]/div/table/tr[2]/td[2]/table/tr/td/div[6]').get()
        description = remove_tags(description)
        description = description.rstrip()
        description = description.lstrip()
        # description = re.sub(r"\s+", " ", description)
    except:
        description = ""
    if description is None:
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
    print("Info Scraped Successfully")
    return data
# //*[@id="CenterBody1"]/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div[7]
# //*[@id="CenterBody1"]/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div[7]

# Vacancy_info('https://jobs24.ge/?act=obj&id=173982&PHPSESSID=tf04s8ucsd5trehbc1qouk90f25tnqma')