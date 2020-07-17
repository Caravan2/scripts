import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from vacancy import Vacancy
from langdetect import detect
import datetime
from bson import ObjectId

import sys
# sys.path.append("/home/miriani/Desktop/main")


# https://hiro.ge/en/search?publish_up=2

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
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

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))


url = "https://azinka.az/job-type/contract/"
page = requests.get(url)


for div in range(1, 30):
    try:
        # Position
        try:
            position = Selector(response=page).xpath(f'/html/body/div[3]/div[1]/div/div/div[1]/div/div[2]/div/article[{div}]/div/div[2]/h2/a/text()').get()
        except:
            position = ""


        # Company
        try:
            company = Selector(response=page).xpath(f'/html/body/div[3]/div[1]/div/div/div[1]/div/div[2]/div/article[{div}]/div/div[2]/p/span[1]/a/text()').get()
        except:
            company = ""

        # Published
        try:
            published = Selector(response=page).xpath(f'/html/body/div[3]/div[1]/div/div/div[1]/div/div[2]/div/article[{div}]/div/div[2]/p/span[4]/time/span[1]/text()').get()
            published = published.strip().split(",")
            publish_year = int(published[1].strip())
            publish_day = int(published[0].split(" ")[1])
            publish_month = int(months[published[0].split(" ")[0]])
        except:
            publish_year = 0
            publish_day = 0
            publish_month = 0

        # Ends
        try:
            ends = Selector(response=page).xpath(f'/html/body/div[3]/div[1]/div/div/div[1]/div/div[2]/div/article[{div}]/div/div[2]/p/span[4]/time/span[2]/text()').get()
            ends = ends.replace("-", "").strip()
            ends = ends.strip().split(",")
            deadline_year = int(ends[1].strip())
            deadline_day = int(ends[0].split(" ")[1])
            deadline_month = int(months[ends[0].split(" ")[0]])
        except:
            deadline_year = 0
            deadline_day = 0
            deadline_month = 0

        # Logo
        try:
            logo = Selector(response=page).xpath(f'/html/body/div[3]/div[1]/div/div/div[1]/div/div[2]/div/article[{div}]/div/div[1]/a/img/@src').get()
        except:
            logo = ""

        # Vacancy link
        try:
            v_link = Selector(response=page).xpath(f'/html/body/div[3]/div[1]/div/div/div[1]/div/div[2]/div/article[{div}]/div/div[1]/a/@href').get()
        except:
            v_link = ""


        returned = Vacancy(v_link)


        data = {
            "position" : position,
            "company" : company,
            "publish_day" : publish_day,
            "publish_month" : publish_month,
            'publish_year' : publish_year,
            "deadline_day" : deadline_day,
            "deadline_month" : deadline_month,
            "deadline_year" : deadline_year,
            "logo" : logo,
            "v_link" : v_link,
        }

        print(data)


        # Check if company already exists in a collection
        check = companydb.find_one({"name" : company})
        if check is None:
            new_company_info = {
                "name" : company,
                "industry" : "1",
                "logo" : logo,
                "created_at" : datetime.datetime.utcnow(),
                "emails" : returned["email"],
                "career_center" : {
                    "description" : "",
                    "custom_button_enabled" : True,
                    "custom_button_title" : "Visit",
                    "custom_button_url" : ""
                },
                "country" : "AZ"
            }
            print("Company details emerged")
            company_object_id = companydb.insert(new_company_info)
            nm = companydb.find_one({"name" : company})
            print(nm)
        else:
            company_object_id = companydb.find_one({"name" : company})
            company_object_id = company_object_id["_id"]
            print("Company already exists: ", company_object_id)



        # Users
        # Vacany User
        if returned["email"] == []:
            user_object_id = 100000000000000000000000
        else:
            check = userdb.find_one({"email" : returned["email"][0]})
            if check is None:
                new_user_info = {
                    "email" : returned["email"][0],
                    "company_id" : ObjectId(f"{company_object_id}"),
                    "created_at" : datetime.datetime.utcnow()
                }
                userdb.insert(new_user_info)
                user_object_id = userdb.find_one({"email" : returned["email"][0]})
                user_object_id = user_object_id["_id"]
                print(user_object_id)
            else:
                user_object_id = userdb.find_one({"email" : returned["email"][0]})
                user_object_id = user_object_id["_id"]
                print(user_object_id)


        # Job Itself
        new_job_info = {
            "user_id" : ObjectId(f"{user_object_id}"),
            'company_id' : ObjectId(f"{company_object_id}"),
            "job_details" : {
                "url" : v_link,
                "title" : position,
                "country_id" : "AZ",
                "city" : [{"city" : "Baku", "id" : "587084"}],
                "employment_type" : "Full Time",
                "description" : [
                    {
                        "language" : "az",
                        "description" : returned["description_az"],
                    },
                    {
                        "language" : "en",
                        "description" : returned["description_en"],
                    }
                ],
                "required" : {
                    "experience" : "",
                },
                "salarycurrency" : "AZN",
                "salarymin" : 0,
                "salarymax" : 0,
                "salaryinterval" : "month",
                "additional_info" : {
                    "suitable_for" : ""
                },
                "numberofpositions" : 1,
                "publishday" : publish_day,
                "publishmonth" : publish_month,
                "publishyear" : publish_year,
                "deadlineday" : deadline_day,
                "deadlinemonth" : deadline_month,
                "deadlineyear" : deadline_year
            },
            "created_at" : datetime.datetime.utcnow(),
            "source" : "azinka.az",
            "status" : "active"
        }
        jobdb.insert(new_job_info)




    except Exception as e:
        print(e)

print("Done")