import requests, json, re
from geonames_en import Geonames
import time
import pymongo
from scrapy.selector import Selector
from w3lib.html import remove_tags
import datetime
from vacancy import Vacancy
from bson import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]


t = time.localtime()
year = time.strftime("%Y", t)
year = int(year)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))
yesterday_month = int(yesterday.strftime("%m"))

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

for i in range(0, 7):
    try:
        i = i * 15
        url = f'https://careercenter.am/en/jobs?status=all&view=classic&category_id=&type=&search=&offset={i}'
        headers = { "X-CSRF-TOKEN" : "Jmwnw9sAcdZkDPWDZKjCkM6hqP87JnBZvQgIed2g", "X-Requested-With" : "XMLHttpRequest" }
        info = requests.get(url, headers=headers).json()

        for n in range (0, 15):
            try:
                # print(n, info["jobs"][n])

                # Job ID
                try:
                    job_id = info["jobs"][n]["jobId"]
                except:
                    job_id = ""

                # Vacancy link
                try:
                    v_link = info["jobs"][n]["slug"]
                    v_link = "https://careercenter.am/en/get/job?slug=" + v_link
                except:
                    v_link = ""

                # Ends
                try:
                    ends = info["jobs"][n]["expiration_date"]
                    ends = ends.split(" ")[0]
                    deadline_day = int(ends.split("-")[2])
                    deadline_month = int(ends.split("-")[1])
                    deadline_year = int(ends.split("-")[0])
                except:
                    deadline_day = 0
                    deadline_month = 0
                    deadline_year = 0
            
                # Published
                try:
                    published = info["jobs"][n]["opening_date"]
                    published = published.split(" ")
                    publish_day = int(published[0])
                    publish_month = int(months[published[1]])
                    publish_year = int(published[2])
                except:
                    publish_day = 0
                    publish_month = 0
                    publish_year = 0
                if yesterday_day != publish_day or yesterday_month != publish_month:
                    print("Not published yesterday")
                    continue

                # position
                try:
                    position = info["jobs"][n]["title"]
                except:
                    position = ""

                # Company
                try:
                    company = info["jobs"][n]["organization"]
                except:
                    company = ""

                # Company description
                try:
                    c_description = info["jobs"][n]["description"]
                except:
                    c_description = ""

                # Logo
                try:
                    logo = info["jobs"][n]["logo"]
                    logo = "https://careercenter.am/storage//" + logo
                except:
                    logo = ""


                data = {
                    "job_id" : job_id,
                    "v_link" : v_link,
                    "deadline_day" : deadline_day,
                    "deadline_month" : deadline_month,
                    "deadline_year" : deadline_year,
                    "publish_day" : publish_day,
                    "publish_month" : publish_month,
                    "publish_year" : publish_year,
                    "position" : position,
                    "company" : company,
                    "c_description" : c_description,
                    "logo" : logo,
                }

                returned = Vacancy(v_link)

                print(data)
                print(returned)


                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "url" : returned["c_link"],
                        "industry" : "1",
                        "logo" : logo,
                        "created_at" : datetime.datetime.utcnow(),
                        "emails" : returned["email"],
                        "career_center" : {
                            "description" : c_description,
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
                        "deadlineday" : deadline_day,
                        "deadlinemonth" : deadline_month,
                        "deadlineyear" : deadline_year
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "careercenter.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)
            except:
                print("Check json: ", n)
    except:
        print("Check: ", i)    
    
    
print("Done")
