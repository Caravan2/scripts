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

url = "https://jobs.ge/en"

# VIP
# //*[@id="wrapper"]/div[4]/table/tbody
# //*[@id="wrapper"]/div[4]/table/tbody/tr[1]

# //*[@id="job_list_table"]/tbody[1]
# //*[@id="job_list_table"]/tbody[1]/tr[1]
# //*[@id="job_list_table"]/tbody[2]
# //*[@id="job_list_table"]/tbody[2]/tr[1]
# //*[@id="job_list_table"]/tbody[8]

for tr in range (2, 400000):
    page = requests.get(url)        
    try:
        try:
            company = Selector(response=page).xpath(f'//*[@id="job_list_table"]/tr[{tr}]/td[4]/a/text()').get().strip()
        except:
            company = ""
        
        
        try:
            link = Selector(response=page).xpath(f'//*[@id="job_list_table"]/tr[{tr}]/td[2]/a/@href').get().strip()
            link = "https://jobs.ge" + link
        except:
            link = ""

        try:
            position = Selector(response=page).xpath(f'//*[@id="job_list_table"]/tr[{tr}]/td[2]/a/text()').get().strip()
        except:
            position = ""

        try:
            published = Selector(response=page).xpath(f'//*[@id="job_list_table"]/tr[{tr}]/td[5]/text()').get()
            publish_day = int(published.split(" ")[0])
            publish_month = int(months[f"{published.split(' ')[1]}"])
            publish_year = year
        except:
            publish_day = 0
            publish_month = 0
            publish_year = 0
        if yesterday_day != publish_day:
            print("Not published yesterday")
            continue

        try:
            ends = Selector(response=page).xpath(f'//*[@id="job_list_table"]/tr[{tr}]/td[6]/text()').get()
            ends = ends.split(" ")
            deadline_day = int(ends[0])
            deadline_month = int(months[f"{ends[1].strip()}"])
            deadline_year = year
        except Exception as e:
            deadline_day = 0
            deadline_month = 0
            deadline_year = 0

        x = {
            "company" : company,
            "position" : position,
            "publish_day" : publish_day,
            "publish_month" : publish_month,
            "publish_year" : publish_year,
            "deadline_day" : deadline_day,
            "deadline_month" : deadline_month,
            "deadline_year" : deadline_year,
            "vacancy_url" : link
        }

        print("Main info scraped")
       
       
       
        # Check if company already exists in a collection
        check = companydb.find_one({"name" : company})

        # Dunmping into MongoDB - at this point it has unique structure (meaning, fits for every option)
        if check is None:
            bia_data = BiaFunction(company)
            if "No info" not in bia_data:
                new_company_info = {
                    "name" : bia_data["name"],
                    "logo" : bia_data["logo"],
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
            print("Company Already exists")

        try:
            vacancy_returned = Vacancy_info(link)
        except:
            vacancy_returned = {
                "description_ka" : "",
                "description_ru" : "",
                "description_en" : "",
                "email" : ""
                }




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
            "source" : "jobs.ge",
            "status" : "active"
        }
        jobdb.insert(new_job_info)


       
    except Exception as e:
        print(e)

    
    
#     check = userdb.find_one({"email" : email})
#     if check is None:
#         if email == "":
#             user_object_id = 100000000000000000000000
#         else:
#             new_user_info = {
#                 "email" : email,
#                 "company_id" : company_object_id,
#                 "created_at" : datetime.datetime.utcnow()
#             }
#             userdb.insert(new_user_info)
#             user_object_id = userdb.find_one({"email" : email})
#             user_object_id = user_object_id["_id"]
#             print(user_object_id)
#     else:
#         user_object_id = userdb.find_one({"email" : email})
#         user_object_id = user_object_id["_id"]
#         print(user_object_id)

#     new_job_info = {
#         "user_id" : ObjectId(f"{user_object_id}"),
#         'company_id' : ObjectId(f"{company_object_id}"),
#         "job_details" : {
#             "url" : url,
#             "title" : position,
#             "country_id" : "GE",
#             "city" : location_id,
#             "employment_type" : stack,
#             "type" : job_type,
#             "description" : [
#                 {
#                     "language" : "ka",
#                     "description" : description_ka,
#                 },
#                 {
#                     "language" : "en",
#                     "description" : description_en,
#                 },
#                 {
#                     "language" : "ru",
#                     "description" : description_ru,
#                 }
#             ],
#             "required" : {
#                 "education" : education,
#             },
#             "salarycurrency" : "GEL",
#             "salarymin" : 0,
#             "salarymax" : 0,
#             "salaryinterval" : "month",
#             "additional_info" : {
#                 "suitable_for" : education
#             },
#             "numberofpositions" : 1,
#             "publishday" : publish_day,
#             "publishmonth" : publish_month,
#             "publishyear" : publish_year,
#             "deadlineday" : deadline_day,
#             "deadlinemonth" : deadline_month,
#             "deadlineyear" : deadline_year
#         },
#         "created_at" : datetime.datetime.utcnow(),
#         "source" : "hiro.ge"
#     }
#     jobdb.insert(new_job_info)
# except Exception as e:
#     print(f"shut up \n ------------------------------------------------------------------------- \n {e} \n\n")
