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
from pprint import pprint as pp
# from config import config

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["personal"]
people = mydb["1"]


# driver.implicitly_wait(2)

for i in range(161, 200000):
    try:
        en = "en"
        ka = "ka"

        url = f"https://www.companyinfo.ge/{ka}/people/{i}"
        
        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"}

        page = requests.get(url, headers=headers)
        
        # print(page.content)

        # Name
        try:
            name = Selector(response=page).xpath('//*[@id="person-profile"]/div/h2/text()').get()
        except:
            name = ""

        if name is None or name == "":
            f = open("check.txt", "a")
            f.write(f"id: {i} was Not captured\n")
            continue


        # ID
        try:
            _id = Selector(response=page).xpath('//*[@id="person-attributes"]/tbody/tr/td[2]/text()').get()
            _id = _id.strip()
        except:
            _id = ""

        whatsthere = people.find_one({"identification_number" : _id})

        if whatsthere is None:


            

            # Listed Affiliations
            affiliations = []
            num_1 = len(Selector(response=page).xpath('//*[@id="affiliations-list"]/tbody/tr').getall()) + 1
            for tr in range(1, num_1):
                # Company
                try:
                    company = Selector(response=page).xpath(f'//*[@id="affiliations-list"]/tbody/tr[{tr}]/td[1]/a/text()').get()
                    company = company.strip()
                except Exception as e:
                    company = e
                
                # Role
                try:
                    role = Selector(response=page).xpath(f'//*[@id="affiliations-list"]/tbody/tr[{tr}]/td[2]/text()').get()
                    role = role.strip()
                    role = role.replace("\n", "")
                    role = re.sub(' +', ' ', role)
                except:
                    role = ""

                # Date
                try:
                    starting_from = Selector(response=page).xpath(f'//*[@id="affiliations-list"]/tbody/tr[{tr}]/td[3]/text()').get()
                    starting_from = starting_from.strip()
                except:
                    starting_from = ""

                # Documentation
                try:
                    documentation = Selector(response=page).xpath(f'//*[@id="affiliations-list"]/tbody/tr[{tr}]/td[4]/a/@href').get()
                    documentation = "https://www.companyinfo.ge" + documentation
                except:
                    documentation = ""

                
                add = {
                    "company" : company,
                    "role" : role,
                    "starting_from" : starting_from,
                    "documentation" : documentation
                }
                affiliations.append(add)



            # Listed ownership
            ownership = []
            num_2 = len(Selector(response=page).xpath('//*[@id="ownership-list"]/tbody/tr').getall())

            for tr in range(1, num_2+1):
                # Company
                try:
                    company = Selector(response=page).xpath(f'//*[@id="ownership-list"]/tbody/tr[{tr}]/td[1]/a/text()').get()
                    company = company.strip()
                except Exception as e:
                    company = e
                # Share
                try:
                    share = Selector(response=page).xpath(f'//*[@id="ownership-list"]/tbody/tr[{tr}]/td[2]/text()').get()
                    share = share.strip()
                    share = share.replace("\n", "")
                    share = re.sub(' +', ' ', share)
                except:
                    share = ""

                # Date
                try:
                    starting_from = Selector(response=page).xpath(f'//*[@id="ownership-list"]/tbody/tr[{tr}]/td[3]/text()').get()
                    starting_from = starting_from.strip()
                except:
                    starting_from = ""

                # Documentation
                try:
                    documentation = Selector(response=page).xpath(f'//*[@id="ownership-list"]/tbody/tr[{tr}]/td[4]/a/@href').get()
                    documentation = "https://www.companyinfo.ge" + documentation
                except:
                    documentation = ""

                
                add = {
                    "company" : company,
                    "share" : share,
                    "starting_from" : starting_from,
                    "documentation" : documentation
                }
                ownership.append(add)
            



            data = {
                "name" : name,
                "identification_number" : _id,
                "affiliations" : affiliations,
                "ownership" : ownership
            }

            print("Added:", i)
            people.insert_one(data)
        else:
            print(f"Person {i} already exists")
    except Exception as e:
        print("There was an error:", i)
        f = open("log.txt", "a")
        f.write(f"id: {i} was interrupted by Error: {e} \n")