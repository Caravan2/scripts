import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from langdetect import detect
from bson import ObjectId
import datetime
import sys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Companies"]
companydb = mydb["bia"]

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

for i in range(139500, 150000):
    print(i)
    try:
        url = f"https://www.bia.ge/En/company/{i}"
        page = requests.get(url)
        
        status = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[1]/span[2]/text()').get()
        
        if status == "Operating":
            # Company name
            name = Selector(response=page).xpath('//*[@id="TrademarksListBox"]/li/text()').get()
            
            
            # Vat number
            vat_number = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[2]/span[2]/text()').get()
            

            # Address
            try:
                address = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[2]/span[2]/text()').get()
                raw = address.split(",")
                postal_code = raw[0]
                location = raw[1]
                region = raw[2]
                appartment = raw[3]
                address = {"location" : location, "postal_code" : postal_code, "appartament" : appartment, "region" : region}
            except:
                address = []
            
            # Working hours
            try:
                working_hours = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[2]/ul/li/text()').get()
                raw = working_hours.split(":", 1)
                days = raw[0].split("-")
                till = days[1].lstrip().lower()
                days = []
                for day in weekdays:
                    if day != till:
                        days.append(day)
                    else:
                        days.append(day)
                        break

                hourfrom = raw[1].split("-")[0]
                hourfrom = hourfrom.lstrip()
                hourfrom = hourfrom.rstrip()

                hourto = raw[1].split("-")[1]
                hourto = hourto.lstrip()
                hourto = hourto.rstrip()
                business_hours = {"week_days" : days, "hour_from" : hourfrom, "hour_to" : hourto}
            except:
                business_hours = []

            # Foundation Date
            foundation_date = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[3]/td[2]/span[2]/text()').get()

            # Phone
            try:
                phone = Selector(response=page).xpath('//*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span').get()
                phone = remove_tags(phone)
                if "," in phone:
                    array = phone.split(",")
                    phone = []
                    for each in array:
                        each = each.lstrip()
                        each = each.rstrip()
                        each = each.split(" ", 1)
                        code = each[0]
                        code = code.replace("+", "")
                        number = each[1]
                        phone.append({"country_code" : code, "number" : number})
                else:
                    phone = phone.lstrip()
                    add = phone.rstrip()
                    add = add.split(" ", 1)
                    code = add[0]
                    code = code.replace("+", "")
                    number = add[1]
                    phone = [{"country_code" : code, "number" : number}]
            except:
                phone = []


            # Web   
            try:
                web = Selector(response=page).xpath('//*[@id="ContactsBox"]/table/tbody/tr[3]/td[2]/span').get()
                web = remove_tags(web)
                if "," in web:
                    array = web.split(",")
                    web = []
                    for each in array:
                        each = each.lstrip()
                        each = each.rstrip()
                        web.append(each)
                else:
                    web = web.lstrip()
                    add = web.rstrip()
                    web = [add]
            except:
                web = []


            # Email
            try:
                email = Selector(response=page).xpath('//*[@id="TabPanelBox"]').get()
                email = email.replace("sales@bia.ge", "")
                email = re.findall(r'[\w\.-]+@[\w\.-]+', email)
            except:
                email = []

            # Logo
            try:
                logo = Selector(response=page).xpath('//*[@id="LogoImageUploaderBox"]').get()
                logo = logo.split("url(\'")
                logo = logo[1].split("')")
                logo = logo[0]
            except:
                logo = ""



            info = {
                "name" : name,
                "vat" : vat_number,
                "addresses" : address,
                "business_hours" : business_hours,
                "phones" : phone,
                "websites" : web,
                "emails" : email,
                "foundation_date" : foundation_date
            }
            print(i, "Scraped. Boo Yeah")
            companydb.insert(info)
    except Exception as e:
        print(e)
# //*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span
# //*[@id="ContactsBox"]/table/tbody/tr[3]/td[2]/span
