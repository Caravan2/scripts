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


for n_page in range(1, 50):
    try:
        url = f"https://full.am/en/job/public/list?keyword=&search_job=&job_owner%5B0%5D=individual&job_owner%5B1%5D=office&job_owner%5B2%5D=company&company_name=&job_type_id=&salary_from=&salary_to=&country=&page={n_page}"
        page = requests.get(url)

        for div in range (1, 50):
            try:

                # Position
                try:
                    position = Selector(response=page).xpath(f'/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[{div}]/div/a[2]/h5/strong/text()').get()
                except:
                    position = ""


                # Company
                try:
                    company = Selector(response=page).xpath(f'/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[{div}]/div/a[2]/p[1]/text()').get()
                except:
                    company = ""

                # Vacancy Link
                try:
                    v_link = Selector(response=page).xpath(f'/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[{div}]/div/a[2]/@href').get()
                except:
                    v_link = ""

                # Logo
                try:
                    logo = Selector(response=page).xpath(f'/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[{div}]/div/a[1]/div/img/@src').get()
                except:
                    logo = ""


                data = {
                    "position" : position,
                    "company" : company,
                    "logo" : logo,
                    # "min_salary" : min_salary,
                    # "max_salary" : max_salary,
                    "v_link" : v_link

                }

                print(data)

                returned = Vacancy(v_link)


                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "industry" : "1",
                        "logo" : logo,
                        "created_at" : datetime.datetime.utcnow(),
                        "emails" : returned["email"],
                        "phones" : returned["phone"],
                        "career_center" : {
                            "description" : "",
                            "custom_button_enabled" : True,
                            "custom_button_title" : "Visit",
                            "custom_button_url" : ""
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
                                "name" : returned["username"],
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
                                "name" : returned["username"],
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
                                "name" : returned["username"],
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
                        "city" : returned["location_id"],
                        "employment_type" : returned["job_type"],
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
                            "experience" : returned["experience"],
                            "education" : returned["education"],
                            "gender" : returned["gender"],
                            "age": returned["age"],
                        },
                        "salarycurrency" : "AMD",
                        "salarymin" : returned["min_salary"],
                        "salarymax" : returned["max_salary"],
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : returned["education"]
                        },
                        "numberofpositions" : 1,
                        "publishday" : returned["publish_day"],
                        "publishmonth" : returned["publish_month"],
                        "publishyear" : returned["publish_year"],
                        "deadlineday" : 0,
                        "deadlinemonth" : 0,
                        "deadlineyear" : 0
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "posted_by" : returned["posted_by"],
                    "source" : "full.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)



            except Exception as e:
                print("Check div: ", e)    
    except Exception as e:
        print("Check page: ", e)
