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
from company import Company_Info
from test import Check_Company
# from config import config

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Companies"]
official = mydb["yell.ge_o"]
official_not_exists = mydb["yell.ge_o_not_psql"]
unofficial = mydb["yell.ge_uno"]


# driver.implicitly_wait(2)

for i in range(116, 1000):

    url = f"https://www.yell.ge/companies.php?lan=eng&rub={i}&SR_pg=1"
    
    page = requests.get(url)
    
    try:
        count = Selector(response=page).xpath('//*[@id="result_count_2020"]/div[2]/div[2]/text()').get()
        count = int(count)
        if count == None:
            count = 0
            print("No company on ID", i)
            continue
    except:
        count = 0
        print("No company on ID", i)
        continue

    print("id:", i, "  page: 1", " companies:", count)

    pages = 0
    remainder = 0
    check = count < 0

    while check is False:
        if count >= 25:
            pages += 1
            count -= 25
            remainder = count % 25
        else:
            check = True
            pages += 1
            remainder = count % 25
    
    print("pages:", pages, " on_the_last_page:", remainder)

    for p_num in range(1, pages+1):
        url = f"https://www.yell.ge/companies.php?lan=eng&rub={i}&SR_pg={p_num}"

        page = requests.get(url)

        for d_num in range (9, 35):
            # Company
            try:
                company = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[2]/div[2]/div[1]/a/text()').get()
                company = company.strip()
            except Exception as e:
                company = ""
            if company == "" or company == None:
                continue

            # Company link
            try:
                c_link = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[2]/div[2]/div[1]/a/@href').get()
                c_link = "https://www.yell.ge/" + c_link
            except Exception as e:
                c_link = ""

            # Address
            try:
                address = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[2]/div[2]/div[4]/div/a/span/text()').get()
                address = address.strip()
            except:
                address = ""
            

            # Phones
            try:
                phone = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[2]/div[2]/div[5]').get()
                phone = remove_tags(phone)
                phone = phone.strip()
                phone = phone.split('\n')
                phone = phone[1].split(",")
                phones = []
                for each in phone:
                    each = each.replace(" ", "")
                    each = each.replace(")", "")
                    each = each.replace("(", "")
                    each = each.replace("\xa0", "")
                    phones.append(each)
            except Exception as e:
                phones = [e]


            # Website
            try:
                website = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[2]/div[2]/div[6]/div[contains(., "website")]/a/@href').get()
                if website is None:
                    website = ""
            except Exception as e:
                website = None


            # Email
            try:
                email = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[2]/div[2]/div[6]/div[contains(., "email")]/a/@href').get()
                email = email.replace("mailto:", "")
                email = [email]
            except:
                email = []

            try:
                check = Selector(response=page).xpath(f'/html/body/div[4]/div/div[2]/div[{d_num}]/div[1]/div[1]/a/img/@src')
                if check == "img/logo_default.png":
                    logo = ""
                else:
                    logo = "https://www.yell.ge/" + check
            except:
                logo = ""

            returned = Company_Info(c_link)
            
            data = {
                "company" : company,
                "address" : address,
                "phones" : phones,
                "websites" : website,
                "emails" : email,
                "logo" : logo,
                "link" : url,
                "company_link" : c_link,
                "vat" : returned["vat"]
            }

                
            print(data)
            if returned["vat"] is None:
                print("Unofficial")
                unofficial.insert_one(data)
            else:
                checking = Check_Company(returned["vat"])
                if checking == 1:
                    print("Official - Exists")
                    official.insert_one(data)
                else:
                    print("Official - Does not exist")
                    official_not_exists.insert_one(data)

# print(main)