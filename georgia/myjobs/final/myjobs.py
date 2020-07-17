import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_ka import Geonames
from bia import BiaFunction
from translator import Translate
# from vacancy import Vacancy_info
from langdetect import detect
import datetime
from bson import ObjectId

import sys
# sys.path.append("/home/miriani/Desktop/main")


# https://hiro.ge/en/search?publish_up=2

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Test"]
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

for number in range(1, 2):
    try:
        url = f'https://www.myjobs.ge/en/?page={number}&sort=6'
        page = requests.get(url)
        for i in range(1, 2):
            try:
            # /html/body/div[2]/div/div[5]/div[2]/div[2]/div[2]/p/span[1]/span

                try:
                    company = Selector(response=page).xpath('/html/body/div[2]/div').get()
                except Exception as e:
                    company = e

                data = {
                    "company" : company
                }

                print(data)


                
            except Exception as e:
                print("Check: ", e)
    except Exception as e:
        print("Check: ", e)
