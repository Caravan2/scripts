import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
from translator import Translate
from company import Company_Info
from vacancy import Vacancy_Info
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


for page in range(1, 10):
    try:
        url = f"https://job.am/en/jobs?p={page}"
        page = requests.get(url)
        
        for div in range(1, 27):
            try:
                # Company
                try:
                    company = Selector(response=page).xpath(f'/html/body/div[2]/form/div[2]/div[2]/div[{div}]/div[2]/div/div[2]/span/a/text()').get()
                except:
                    company = ""

                # Company link
                try:
                    c_link = Selector(response=page).xpath(f'/html/body/div[2]/form/div[2]/div[2]/div[{div}]/div[2]/div/div[2]/span/a/@href').get()
                    c_link = "https://job.am" + c_link
                except:
                    c_link = ""

                # Position
                try:
                    position = Selector(response=page).xpath(f'/html/body/div[2]/form/div[2]/div[2]/div[{div}]/div[2]/div/div[1]/a/text()').get()
                except:
                    position = ""

                # Vacancy Link
                try:
                    v_link = Selector(response=page).xpath(f'/html/body/div[2]/form/div[2]/div[2]/div[{div}]/div[2]/div/div[1]/a/@href').get()
                    v_link = "https://job.am" + v_link
                except:
                    v_link = ""


                # Logo
                try:
                    logo = Selector(response=page).xpath(f'/html/body/div[2]/form/div[2]/div[2]/div[{div}]/div[1]/img/@src').get()
                    logo = "https://job.am" + logo
                except:
                    logo = ""


                # Location
                try:
                    location = Selector(response=page).xpath(f'/html/body/div[2]/form/div[2]/div[2]/div[{div}]/div[3]/div/span/text()').get()
                    location_id = {"city" : f"{location}", "id" : f"{Geonames(location)}"}
                except:
                    location_id = {'city': 'Yerevan', 'id': '616052'}


                data = {
                    "company" : company,
                    "c_link" : c_link,
                    "position" : position,
                    "v_link" : v_link,
                    "logo" : logo,
                    "location" : location,
                }

                print(data)

                Company_returned = Company_Info(c_link)
                print(Company_returned)

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
                        "websites" : Company_returned["website"],
                        "phones" : Company_returned["phone"],
                        "career_center" : {
                            "description" : Company_returned["description_en"],
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


                Vacancy_returned = Vacancy_Info(v_link)
                
                # User
                if Vacancy_returned["email"] == []:
                    if Company_returned["phone"] == []:
                        user_object_id = 100000000000000000000000
                    else:
                        check = userdb.find_one({"phones" : Company_returned["phone"]})
                        if check is None:
                            new_user_info = {
                                "phones" : Company_returned["phone"],
                                "company_id" : ObjectId(f"{company_object_id}"),
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"phones" : Company_returned["phone"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        else:
                            user_object_id = userdb.find_one({"phones" : Company_returned["phone"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                else:
                    if Company_returned["phone"] == []:
                        check = userdb.find_one({"email" : Vacancy_returned["email"]})
                        if check is None:
                            new_user_info = {
                                "email" : Vacancy_returned["email"],
                                "company_id" : ObjectId(f"{company_object_id}"),
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"email" : Vacancy_returned["email"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        else:
                            user_object_id = userdb.find_one({"email" : Vacancy_returned["email"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                    else:
                        check = userdb.find_one({"email" : Vacancy_returned["email"]})
                        if check is None:
                            new_user_info = {
                                "email" : Vacancy_returned["email"],
                                "phones" : Company_returned["phone"],
                                "company_id" : ObjectId(f"{company_object_id}"),
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"email" : Vacancy_returned["email"]})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        else:
                            user_object_id = userdb.find_one({"email" : Vacancy_returned["email"]})
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
                        "city" : [location_id],
                        "employment_type" : Vacancy_returned["employment_type"],
                        "description" : [
                            {
                                "language" : "am",
                                "description" : Vacancy_returned["description_am"],
                            },
                            {
                                "language" : "en",
                                "description" : Vacancy_returned["description_en"],
                            }
                        ],
                        "required" : {
                            "experience" : "",
                        },
                        "salarycurrency" : "AMD",
                        "salarymin" : Vacancy_returned["salary"],
                        "salarymax" : Vacancy_returned["salary"],
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : ""
                        },
                        "numberofpositions" : 1,
                        "publishday" : 0,
                        "publishmonth" : 0,
                        "publishyear" : year,
                        "deadlineday" : Vacancy_returned["deadline_day"],
                        "deadlinemonth" : Vacancy_returned["deadline_month"],
                        "deadlineyear" : Vacancy_returned["deadline_year"]
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "job.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)


            except Exception as e:
                print("Check div: ", e)

    except Exception as e:
        print("Check Page: ", e)
