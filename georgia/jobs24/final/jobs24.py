import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_ka import Geonames
from bia import BiaFunction
# from translator import Translate
from vacancy import Vacancy_info
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
    "იან": "01",
    "თებ": "02",
    "მარ": "03",
    "აპრ": "04",
    "მაი": "05",
    "ივნ": "06",
    "ივლ": "07",
    "აგვ": "08",
    "სექ": "09",
    "ოქტ": "10",
    "ნოე": "11",
    "დეკ": "12"
    }

t = time.localtime()
year = time.strftime("%Y", t)
year = int(year)

url = "https://jobs24.ge/"

for i in range (2, 1001):
    try:
        page = requests.get(url)
        try:
            company = Selector(response=page).xpath(f'/html/body/table[2]/tr/td[2]/div/div[6]/div/div[3]/table/tr[{i}]/td[2]/text()').get()
        except:
            comapny = ""
        if company is None:
            continue

        try:
            position = Selector(response=page).xpath(f'/html/body/table[2]/tr/td[2]/div/div[6]/div/div[3]/table/tr[{i}]/td[1]/a[1]/text()').get()
        except:
            position = ""

        try:
            link = Selector(response=page).xpath(f'/html/body/table[2]/tr/td[2]/div/div[6]/div/div[3]/table/tr[{i}]/td[1]/a[1]/@href').get()
            link = "https://jobs24.ge/" + link
        except:
            link = ""

        try:
            published = Selector(response=page).xpath(f'/html/body/table[2]/tr/td[2]/div/div[6]/div/div[3]/table/tr[{i}]/td[3]/text()').get()
            publish_day = int(published.split(" ")[0])
            publish_month = int(months[f"{published.split(' ')[1]}"])
            publish_year = year
        except:
            publish_day = 0
            publish_month = 0
            publish_year = 0

        try:
            ends = Selector(response=page).xpath(f'/html/body/table[2]/tr/td[2]/div/div[6]/div/div[3]/table/tr[{i}]/td[4]/text()').get()
            ends = ends.split(" ")
            deadline_day = int(ends[0])
            deadline_month = int(months[f"{ends[1].strip()}"])
            deadline_year = year
        except:
            deadline_day = 0
            deadline_month = 0
            deadline_year = 0

        print(company, position, link, publish_day, publish_month, publish_year, deadline_day, deadline_month, deadline_year)

        # Check if company already exists in a collection
        bia_data = BiaFunction(company)
        if "No info" not in bia_data:
            check = companydb.find_one({"name" : bia_data["name"]})
            if check is None:
                new_company_info = {
                    "name" : bia_data["name"],
                    "industry" : "1",
                    "websites" : bia_data["websites"],
                    "emails" : bia_data["emails"],
                    "phones" : bia_data["phones"],
                    "foundation_date" : bia_data["foundation_date"],
                    "vat" : bia_data["vat"],
                    "addressed" : bia_data["addresses"],
                    "business_hours" : bia_data["business_hours"],
                    "created_at" : datetime.datetime.utcnow(),
                    "country" : "GE"
                }
                companydb.insert(new_company_info)
                company_object_id = companydb.find_one({"name" : company})
                company_object_id = company_object_id["_id"]
                print(company_object_id)
                print("Company added succesfully")
            else:
                company_object_id = companydb.find_one({"name" : bia_data["name"]})
                company_object_id = company_object_id["_id"]
                print(company_object_id)
                print("Company already exists")
        else:
            check = companydb.find_one({"name" : company})
            if check is None:
                new_company_info = {
                    "name" : company,
                    "industry" : "1",
                    "created_at" : datetime.datetime.utcnow(),
                    "country" : "GE"
                }
                companydb.insert(new_company_info)
                company_object_id = companydb.find_one({"name" : company})
                company_object_id = company_object_id["_id"]
                print(company_object_id)
                print("Company added succesfully")
            else:
                company_object_id = companydb.find_one({"name" : company})
                company_object_id = company_object_id["_id"]
                print(company_object_id)
                print("Company already exists")


        vacancy_returned = Vacancy_info(link)



        check = userdb.find_one({"email" : vacancy_returned["email"]})
        if check is None:
            if vacancy_returned["email"] == "":
                user_object_id = 100000000000000000000000
            else:
                new_user_info = {
                    "email" : vacancy_returned["email"],
                    "company_id" : company_object_id,
                    "created_at" : datetime.datetime.utcnow()
                }
                userdb.insert(new_user_info)
                user_object_id = userdb.find_one({"email" : vacancy_returned["email"]})
                user_object_id = user_object_id["_id"]
                print(user_object_id)
        else:
            user_object_id = userdb.find_one({"email" : vacancy_returned["email"]})
            user_object_id = user_object_id["_id"]
            print(user_object_id)


        new_job_info = {
            "user_id" : ObjectId(f"{user_object_id}"),
            'company_id' : ObjectId(f"{company_object_id}"),
            "job_details" : {
                "url" : link,
                "title" : position,
                "country_id" : "GE",
                "city" : [{"city" : "Tbilisi", "id" : "611717"}],
                "description" : [
                    {
                        "language" : "ka",
                        "description" : vacancy_returned["description_ka"],
                    },
                    {
                        "language" : "en",
                        "description" : vacancy_returned["description_en"],
                    },
                    {
                        "language" : "ru",
                        "description" : vacancy_returned["description_ru"],
                    }
                ],
                "salarycurrency" : "GEL",
                "salarymin" : 0,
                "salarymax" : 0,
                "salaryinterval" : "month",
                "numberofpositions" : 1,
                "publishday" : publish_day,
                "publishmonth" : publish_month,
                "publishyear" : publish_year,
                "deadlineday" : deadline_day,
                "deadlinemonth" : deadline_month,
                "deadlineyear" : deadline_year
            },
            "created_at" : datetime.datetime.utcnow(),
            "source" : "jobs24.ge",
            "status" : "active"
        }
        jobdb.insert(new_job_info)
        print("Done", i)

    except Exception as e:
        print("Check: ", e)