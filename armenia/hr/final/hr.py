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


for p in range(1, 2):
    try:
        url = "http://hr.am/main/loadvacancies/"
        data = { "page" : p }
        headers = { "Accept-Encoding" : "gzip, deflate, br" }
        page = requests.post(url, data=data, headers=headers)
        page = page.content.decode('utf-8')

        every = page.split('<div class="vacancy-item"')
        for each in every:
            try:
            
                # Company name
                try:
                    company = each.split('<div class="company">')[1].split("</div>")[0]
                except:
                    company = ""
                if company == "":
                    continue


                # Position
                try:
                    position = each.split('<div class="title">')[1].split('</div>')[0]
                except:
                    position = ""

                # Logo
                try:
                    logo = each.split('<img src="')[1].split('">')[0]
                    logo = "http://hr.am/" + logo
                except:
                    logo = ""


                # Ends
                try:
                    ends = each.split('<span>')[1].split('</span>')[0]
                    ends = ends.split(",")
                    deadline_year = int(ends[1].strip())
                    deadline_day = ends[0].split(" ")[0]
                    deadline_day = int(deadline_day)
                    deadline_month = ends[0].split(" ")[1]
                    deadline_month = int(months[deadline_month])
                except Exception as e:
                    edeadline_year = 0
                    deadline_day = 0
                    deadline_month = 0


                # Vacancy Link
                try:
                    v_link = each.split('data-id="')[1].split('">')[0]
                    v_link = f"http://hr.am/vacancy/view/vid/{v_link}/t/"
                except:
                    v_link = ""






                data = {
                    "company" : company,
                    "position" : position,
                    "logo" : logo,
                    "deadline_day" : ends,
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
                        "city" : [{"city" : "Yerevan", "id" : "616052"}],
                        "employment_type" : "Full Time",
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
                            "experience" : "",
                        },
                        "salarycurrency" : "AMD",
                        "salarymin" : 0,
                        "salarymax" : 0,
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : ""
                        },
                        "numberofpositions" : 1,
                        "publishday" : int(today.strftime("%d")),
                        "publishmonth" : int(today.strftime("%m")),
                        "publishyear" : int(today.strftime("%Y")),
                        "deadlineday" : deadline_day,
                        "deadlinemonth" : deadline_month,
                        "deadlineyear" : deadline_year
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "hr.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)



            except Exception as e:
                print("Check div: ", e)
    except Exception as e:
        print("Check p: ", p, e)