import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
from translator import Translate
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


for n in range(0, 20):
    try:
        url = f"https://www.worknet.am/en/load/jobs?&start={n*12}&end=12"
        headers = { "x-requested-with" : "XMLHttpRequest" }
        page = requests.get(url, headers=headers)
        for div in range(1, 30):
            try:
                print(div)
                # Company
                try:
                    company = Selector(response=page).xpath(f'/html/body/div[{div}]/div/div[2]/div[1]/div/a/text()').get()
                except:
                    company = ""
                if company is None:
                    continue

                # Company Link
                try:
                    c_link = Selector(response=page).xpath(f'/html/body/div[{div}]/div/div[2]/div[1]/div/a/@href').get()
                    c_link = "https://www.worknet.am" + c_link
                except:
                    c_link = ""

                # Position
                try:
                    position = Selector(response=page).xpath(f'/html/body/div[{div}]/div/div[1]/div[1]/a/text()').get()
                except:
                    position = ""

                # Vacancy link
                try:
                    v_link = Selector(response=page).xpath(f'/html/body/div[{div}]/div/div[1]/div[1]/a/@href').get()
                    v_link = "https://www.worknet.am" + v_link
                except:
                    v_link = ""

                # Logo
                try:
                    logo = Selector(response=page).xpath(f'/html/body/div[{div}]/div/img/@src').get()
                    logo = "https://www.worknet.am" + logo
                except:
                    logo = ""


                data = {
                    "company" : company,
                    "c_link" : c_link,
                    "position" : position,
                    "v_link" : v_link,
                    "logo" : logo
                }

                returned = Vacancy(v_link)

                print(data)

                
                # COMPANY DATA
                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "url" : c_link,
                        "industry" : "1",
                        "logo" : logo,
                        "created_at" : datetime.datetime.utcnow(),
                        "websites" : returned["website"],
                        "emails" : returned["email"],
                        "career_center" : {
                            "description" : "",
                            "custom_button_enabled" : True,
                            "custom_button_title" : "Visit",
                            "custom_button_url" : c_link
                        },
                        "country" : "AM"
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
                        "country_id" : "AM",
                        "city" : returned["location"],
                        "description" : [
                            {
                                "language" : "am",
                                "description" : returned["description_am"],
                            },
                            {
                                "language" : "en",
                                "description" : returned["description_en"],
                            }
                        ],
                        "required" : {
                            "gender" : returned["gender"],
                        },
                        "salarycurrency" : "AMD",
                        "salarymin" : returned["salary"],
                        "salarymax" : returned["salary"],
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : returned["gender"]
                        },
                        "numberofpositions" : 1,
                        "publishday" : int(today.strftime("%d")),
                        "publishmonth" : int(today.strftime("%m")),
                        "publishyear" : int(today.strftime("%Y")),
                        "deadlineday" : 0,
                        "deadlinemonth" : 0,
                        "deadlineyear" : 0
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "worknet.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)



            except Exception as e:
                print("Check div: ", e)
    except Exception as e:
        print("Check n: ", e)