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



for page in range(1, 20):
    try:
        url = f"https://staff.am/en/jobs?page={page}&per-page=50"
        headers = {"Accept-Language": "en-US,en;q=0.5"}

        page = requests.get(url, headers=headers)
        for div in range (1, 51):
            try:
                # Company
                try:
                    company = Selector(response=page).xpath(f'//*[@id="w0"]/div[{div}]/div/div/a[1]/div[2]/p[2]/text()').get()
                except:
                    company = ""
                # //*[@id="w0"]/div[1]/div/div/a[1]/div[2]/p[2]
                # //*[@id="w0"]/div[2]/div/div/a[1]/div[2]/p[2]
                # //*[@id="w0"]/div[11]/div/div[2]/a[1]/div[2]/p[2]


                # Position
                try:
                    position = Selector(response=page).xpath(f'//*[@id="w0"]/div[{div}]/div/div/a[1]/div[2]/p[1]/text()').get()
                except:
                    position = ""


                # Location
                try:
                    location = Selector(response=page).xpath(f'//*[@id="w0"]/div[{div}]/div/div/a[2]/div/p[2]').get()
                    location = remove_tags(location)
                    location = location.strip()
                    location_id = []
                    location = {"city" : f"{location}", "id" : f"{Geonames(location)}"}
                    location_id.append(location)
                except:
                    location = [{'city': 'Yerevan', 'id': '616052'}]


                # Published
                try:
                    publish_day = int(yesterday.strftime("%d"))
                    publish_month = int(yesterday.strftime("%m"))
                    publish_year = int(yesterday.strftime("%Y"))
                except:
                    publish_day = 0
                    publish_month = 0
                    publish_year = 0
                print(publish_day)
                if yesterday_day != publish_day:
                    print("Not published yesterday")
                    continue
                

                # link to the vacancy
                try:
                    v_link = Selector(response=page).xpath(f'//*[@id="w0"]/div[{div}]/div/div/a[1]/@href').get()
                    v_link = "https://staff.am" + v_link
                except:
                    v_link = ""

                # Logo
                try:
                    logo = Selector(response=page).xpath(f'//*[@id="w0"]/div[{div}]/div/div/a[1]/div[1]/img/@data-original').get()
                except:
                    logo = ""

                outside = {
                    "company" : company,
                    "position" : position,
                    "location" : location_id,
                    "publish_day" : publish_day,
                    "publish_month" : publish_month,
                    "publish_year" : publish_year,
                    # "ends" : ends,
                    "v_link" : v_link,
                    "logo" : logo
                }

                returned = Vacancy(v_link)

                                       
                address = returned["address"]
                addresses = { "location" : { "country" : "AM", "city" : location_id }, "postal_code" : "", "appartament" : address }
                                                                        
                                                                        # COMPANY DATA
                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "url" : returned["c_link"],
                        "industry" : "1",
                        "size" : returned["N_of_employees"],
                        "logo" : logo,
                        "created_at" : datetime.datetime.utcnow(),
                        "websites" : returned["website"],
                        "emails" : returned["email"],
                        "phones" : returned["phone"],
                        "foundation_date" : returned["foundation_date"],
                        "addresses" : addresses,
                        "career_center" : {
                            "description" : returned["company_description"],
                            "custom_button_enabled" : True,
                            "custom_button_title" : "Visit",
                            "custom_button_url" : returned["c_link"]
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
                    if returned["phone"] == []:
                        user_object_id = 100000000000000000000000
                    else:
                        check = userdb.find_one({"phones" : returned["phone"]})
                        if check is None:
                            new_user_info = {
                                "phones" : returned["phone"],
                                "company_id" : ObjectId(f"{company_object_id}"),
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"phones" : returned["phone"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        else:
                            user_object_id = userdb.find_one({"phones" : returned["phone"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                else:
                    if returned["phone"] == []:
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
                    else:
                        check = userdb.find_one({"email" : returned["email"][0]})
                        if check is None:
                            new_user_info = {
                                "email" : returned["email"][0],
                                "phones" : returned["phone"],
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
                        "city" : location_id,
                        "employment_type" : returned["job_type"],
                        "employment_term" : returned["employment_term"],
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
                            "experience" : returned["candidate_level"],
                        },
                        "salarycurrency" : "AMD",
                        "salarymin" : 0,
                        "salarymax" : 0,
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : returned["candidate_level"]
                        },
                        "numberofpositions" : 1,
                        "publishday" : publish_day,
                        "publishmonth" : publish_month,
                        "publishyear" : publish_year,
                        "deadlineday" : returned["deadline_day"],
                        "deadlinemonth" : returned["deadline_month"],
                        "deadlineyear" : returned["deadline_year"]
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "staff.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)

            except Exception as e:
                print("Check div: ", e)
    except Exception as e:
        print("Page Check: ", e)