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
# from config import config


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Test"]
check = mydb["armenia_companies"]
unofficial = mydb["arm_unofficial"]
official = mydb["arm_official"]

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

driver.implicitly_wait(5)

def Get_Company(link):
    url = link

    driver.get(url)

    # Contact Person
    try:
        contact_person = driver.find_element_by_xpath('//*[@id="executive"]').text
        contact_person = contact_person.split("\n")[1].split(", ")
        position = contact_person[1]
        contact_person = contact_person[0]
    except:
        contact_person = ""
        position = ""

    # Phones
    try:
        phone = driver.find_element_by_xpath('//*[@id="address"]/li[2]/div/div[contains(., "+")]').text
        phone = phone.replace("• ", "")
    except:
        phone = ""
    
    # Address
    try:
        address = driver.find_element_by_xpath('//*[@id="address"]/li[2]/div').text
        address = address.split('\n•')[0]
        address = address.split("\nMon")[0]
    except:
        address = ""

    # Website
    try:
        website = driver.find_element_by_xpath('//*[@id="otherData"]/li[contains(., "http")]').text
    except:
        website = ""

    data = {
        "phone" : phone,
        "address" : address,
        "website" : website,
        "contact_person" : contact_person,
        "position" : position
    }

    return data

def Get_Vat(name):
    driver.get('https://www.e-register.am/en/search')
    
    driver.find_element_by_xpath('//*[@id="by_comp"]/tbody/tr[1]/td/input[1]').send_keys(name)

    driver.find_element_by_xpath('//*[@id="by_comp"]/tbody/tr[4]/td/input').click()
    
    driver.find_element_by_xpath('//*[@id="by_comp"]/tbody/tr[1]/td/input[2]').click()

    # time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="page"]/div[1]/div/table[2]/tbody/tr[2]/td/a').click()
    except:
        print("No info in government")
        return

    registration_number = driver.find_element_by_xpath('//*[@id="page"]/table[3]/tbody/tr[2]/td[2]').text

    foundation_date = registration_number.split("/")[1].strip()
    
    registration_number = registration_number.split("/")[0].strip()

    tax_id = driver.find_element_by_xpath('//*[@id="page"]/table[3]/tbody/tr[3]/td[2]').text

    data = {
        "foundation_date" : foundation_date,
        "registration_number" : registration_number,
        "tax_id" : tax_id
    }

    return data

info = check.find({})
for each in info:
    if unofficial.find_one( {"name" : each["company"]} ) is None and official.find_one( {"name" : each["company"]} ) is None:
        web_returned = Get_Company(each["c_link"])
        gov_returned = Get_Vat(each["company"])
        if gov_returned is None:
            insertion = {
                "name" : each["company"],
                "source" : each["c_link"],
                "phone" : web_returned["phone"],
                "address" : web_returned["address"],
                "website" : web_returned["website"],
                "contact_person" : web_returned["contact_person"],
                "position" : web_returned["position"],
            }
            unofficial.insert_one(insertion)
            print("Unofficial added")
        else:
            insertion = {
                "name" : each["company"],
                "source" : each["c_link"],
                "phone" : web_returned["phone"],
                "address" : web_returned["address"],
                "website" : web_returned["website"],
                "contact_person" : web_returned["contact_person"],
                "position" : web_returned["position"],
                "foundation_date" : gov_returned["foundation_date"],
                "registration_number" : gov_returned["registration_number"],
                "tax_id" : gov_returned["tax_id"]
            }
            official.insert_one(insertion)
            print("Official added")

        print("ID:", each["_id"], "Finished \n -------------------------------------------------")
    else:
        print(unofficial.find_one( {"name" : each["company"]} ))
        print(official.find_one( {"name" : each["company"]} ))
        print("Already exists")
print("Finished")

# Get_Vat("AACC")

# Check('https://www.spyur.am/en/companies/a--h-friendship/40028')

# https://www.spyur.am/en/companies/armetal/40273
# https://www.spyur.am/en/companies/a--a-souvenir-shop/38615
# https://www.spyur.am/en/companies/print-box-printing-house/36232