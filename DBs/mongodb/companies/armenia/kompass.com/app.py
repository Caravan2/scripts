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
mycol = mydb["armenia_companies_kompass"]

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

# driver.implicitly_wait(2)


for i in range(1850, 100000):
    try:
        url = f"https://am.kompass.com/en/c/detect-value-ag/am{i}/"

        driver.get(url)

        headers = {"User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}

        page = requests.get(url, headers=headers)


        # Company
        try:
            company = Selector(response=page).css('#productDetailUpdateable > div.container.containerCompany > div.headerCompany.containerWhite > div > div.companyCol1.companyColumn > div.companyRow > div.companyCol1.blockNameCompany > h1').get()
            company = remove_tags(company)
            company = company.strip()
        except:
            company = ""
        if company == "":
            print("No company on ID: ", i)
            continue

        # Address
        try:
            address = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[3]/div[1]/div/div[1]/p[1]/span[2]').text
        except:
            address = ""
        if address == "":
            try:
                address = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/p[1]/span[2]/span').text
            except:
                f = open('log.txt', "a")
                f.write(f"Address: {url}\n")
                address = ""    
        # Logo
        try:
            logo = driver.find_element_by_xpath('//*[@id="companyLogo"]').get_attribute("src")
        except:
            logo = ""

        # Foundation date
        try:
            foundation_date = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[3]/div[2]/div/div/table/tbody/tr[1]/td').text
        except:
            foundation_date = ""
        if foundation_date == "":
            try:
                foundation_date = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/td').text
            except:
                f = open('log.txt', "a")
                f.write(f"Foundation Date: {url}\n")
                foundation_date = ""

        # Legal form
        try:
            legal_form = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[3]/div[2]/div/div/table/tbody/tr[2]/td').text
        except:
            legal_form = 0

        # Number of employers
        try:
            number_of_employers = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[3]/div[2]/div/div/table/tbody/tr[4]/td').text
        except:
            number_of_employers = 0
        if number_of_employers == 0:
            try:
                number_of_employers = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[2]/div[2]/div[2]/div/div/table/tbody/tr[4]/td').text
            except:
                f = open('log.txt', "a")
                f.write(f"Number_of_employer: {url}\n")
                number_of_employers = 0

        # Website
        try:
            website = driver.find_element_by_xpath('//*[@id="webSite_presentation_0"]').get_attribute('href')
        except:
            website = ""

        # Description
        try:
            description = driver.find_element_by_xpath('//*[@id="productDetailUpdateable"]/div[3]/div[1]/div[1]/div/div/div').text
        except:
            description = ""

        # Contact Person
        try:
            contact_person = driver.find_element_by_xpath('//*[@id="executive-info-1"]/div[1]/div[2]').text
        except:
            contact_person = ""

        try:
            position = contact_person.split("\n")[1]
            position = position.replace(")", "")
            position = position.replace("(", "")
            contact_person = contact_person.split("\n")[0]
        except:
            contact_person = ""
            position = ""

        # Phone number
        try:
            driver.find_element_by_xpath(f'//*[@id="switchPhone-contactCompanyForCompany-AM{i}"]/div').click()
            phone_number = driver.find_element_by_xpath(f'//*[@id="contactCompanyHipayModalBody-contactCompanyForCompany-AM{i}"]/div/div/a').get_attribute('href')
            phone_number = phone_number.replace("tel:", "")
        except Exception as e:
            phone_number = e


        # Neglect if log has a default picture
        # if Selector(response=page).xpath('//*[@id="companyLogo"]/@title').get() == 
        


        data = {
            "company" : company,
            "address" : address,
            "logo" : logo,
            "foundation_date" : foundation_date,
            "legal_form" : legal_form,
            "number_of_employers" : number_of_employers,
            "phone_number" : phone_number,
            "website" : website,
            # "description" : description,
            "contact_person" : contact_person,
            "position" : position
        }

        mycol.insert_one(data)

        print(data)
    except:
        f = open('log.txt', "a")
        f.write(f"-------------------------------- Ooops: {url}\n")
        print("Ooops")
        os.system("windscribe connect")