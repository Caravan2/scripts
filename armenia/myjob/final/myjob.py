import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
# from translator import Translate
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



for page in range (1, 50):
    try:
        url = f"https://www.myjob.am/Default.aspx?pg={page}"
        page = requests.get(url)

        for div in range (1, 11):
            try:
                
                # Company
                try:
                    company = Selector(response=page).xpath(f'//*[@id="MainContentPlaceHolder_jobPageContainer"]/a[{div}]/div/div[1]/div[2]/text()').get()
                except:
                    company = ""


                # Position
                try:
                    position = Selector(response=page).xpath(f'//*[@id="MainContentPlaceHolder_jobPageContainer"]/a[{div}]/div/div[1]/div[1]/text()').get()
                except:
                    position = ""


                # Vacancy Link
                try:
                    v_link = Selector(response=page).xpath(f'//*[@id="MainContentPlaceHolder_jobPageContainer"]/a[1]/@href').get()
                    v_link = "https://www.myjob.am/" + v_link
                except:
                    v_link = ""


                # Location
                try:
                    location = Selector(response=page).xpath(f'//*[@id="MainContentPlaceHolder_jobPageContainer"]/a[{div}]/div/div[2]/div/text()').get()
                    location = location.split(",")[0]
                    location_id = [{"city" : f"{location}", "id" : f"{Geonames(location)}"}]
                except:
                    location_id = [{'city': 'Yerevan', 'id': '616052'}]


                # Publication
                try:
                    published = Selector(response=page).xpath(f'//*[@id="MainContentPlaceHolder_jobPageContainer"]/a[{div}]/div/div[1]/div[3]/text()').get()
                    published = published.replace("Published on ", "").split("/")
                    publish_day = int(published[0])
                    publish_month = int(published[1])
                    publish_year = int(published[2])
                except:
                    publish_day = 0
                    publish_month = 0
                    publish_year = 0

                

# //*[@id="MainContentPlaceHolder_jobPageContainer"]/a[1]/div/div[1]/div[2]
# //*[@id="MainContentPlaceHolder_jobPageContainer"]/a[2]/div/div[1]/div[2]


                data = {
                    "company" : company,
                    "position" : position,
                    "location" : location_id,
                    "publish_day" : publish_day,
                    "publish_month" : publish_month,
                    "publish_year" : publish_year,
                    "v_link" : v_link
                }
                print("Landing page data is scraped")
                v_returned = Vacancy(v_link)


                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "industry" : "1",
                        "created_at" : datetime.datetime.utcnow(),
                        "emails" : v_returned["email"],
                        "career_center" : {
                            "description" : "",
                            "custom_button_enabled" : True,
                            "custom_button_title" : "Visit",
                            "custom_button_url" : ""
                        },
                        "country" : "AM"
                    }
                    print(new_company_info)
                    companydb.insert_one(new_company_info)
                    company_object_id = companydb.find_one({"name" : company})
                    company_object_id = company_object_id["_id"]
                    print(company_object_id)
                else:
                    company_object_id = companydb.find_one({"name" : company})
                    company_object_id = company_object_id["_id"]
                    print("Company already exists: ", company_object_id)


                # Users
                # Vacany User
                if v_returned["email"] == []:
                    user_object_id = 100000000000000000000000
                else:
                    check = userdb.find_one({"email" : v_returned["email"][0]})
                    if check is None:
                        new_user_info = {
                            "email" : v_returned["email"][0],
                            "company_id" : ObjectId(f"{company_object_id}"),
                            "created_at" : datetime.datetime.utcnow()
                        }
                        userdb.insert(new_user_info)
                        user_object_id = userdb.find_one({"email" : v_returned["email"][0]})
                        user_object_id = user_object_id["_id"]
                        print(user_object_id)
                    else:
                        user_object_id = userdb.find_one({"email" : v_returned["email"][0]})
                        user_object_id = user_object_id["_id"]
                        print("User already exists")



                # Job Itself
                new_job_info = {
                    "user_id" : ObjectId(f"{user_object_id}"),
                    'company_id' : ObjectId(f"{company_object_id}"),
                    "job_details" : {
                        "url" : v_link,
                        "title" : position,
                        "country_id" : "AM",
                        "city" : location_id,
                        "description" : [
                            {
                                "language" : "am",
                                "description" : "",
                            },
                            {
                                "language" : "en",
                                "description" : v_returned["description"],
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
                        "publishday" : publish_day,
                        "publishmonth" : publish_month,
                        "publishyear" : publish_year,
                        "deadlineday" : v_returned["deadline_day"],
                        "deadlinemonth" : v_returned["deadline_month"],
                        "deadlineyear" : v_returned["deadline_year"]
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "myjob.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)

            except Exception as e:
                print("Check div: ", e)
    except Exception as e:
        print("Check page: ", e)
