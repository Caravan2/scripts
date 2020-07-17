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

for p in range(1, 15):
    try:
        url = f"https://boss.az/vacancies?page={p}"
        page = requests.get(url)
        for div in range(1, 30):
            try:
                # Company
                try:
                    company = Selector(response=page).xpath(f'/html/body/div[4]/div[2]/div/div[{div}]/a/text()').get()
                except:
                    company = ""


                # Position
                try:
                    position = Selector(response=page).xpath(f'/html/body/div[4]/div[2]/div/div[{div}]/h3/text()').get()
                except:
                    position = ""


                # Salary
                try:
                    salary = Selector(response=page).xpath(f'/html/body/div[4]/div[2]/div/div[{div}]/div[1]/div/text()').get()
                    salary = salary.replace(" AZN", '')
                    if "-" in salary:
                        salary = salary.split(" - ")
                        min_salary = int(salary[0])
                        max_salary = int(salary[1])
                    else:
                        min_salary = int(salary)
                        max_salary = int(salary)
                except:
                    min_salary = 0
                    max_salary = 0
                
                # Vacancy Link
                try:
                    v_link = Selector(response=page).xpath(f'/html/body/div[4]/div[2]/div/div[{div}]/div[1]/a/@href').get()
                    v_link = "https://boss.az" + v_link
                except:
                    v_link = ""

                data = {
                    "company" : company,
                    "position" : position,
                    "min_salary" : min_salary,
                    "max_salary" : max_salary,
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
                        "created_at" : datetime.datetime.utcnow(),
                        "emails" : returned["email"],
                        "phones" : returned["phone"],
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
                        "salarymin" : min_salary,
                        "salarymax" : max_salary,
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : ""
                        },
                        "numberofpositions" : 1,
                        "publishday" : returned["publish_day"],
                        "publishmonth" : returned["publish_month"],
                        "publishyear" : returned["publish_year"],
                        "deadlineday" : returned["deadline_day"],
                        "deadlinemonth" : returned["deadline_month"],
                        "deadlineyear" : returned["deadline_year"]
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "boss.az",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)
                    

            except Exception as e:
                print("Check div: ", e)
    except Exception as e:
        print("Check p: ", e)