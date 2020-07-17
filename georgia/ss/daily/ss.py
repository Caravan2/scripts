import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_ka import Geonames
from translator import Translate
from langdetect import detect
import datetime
from bson import ObjectId
import sys
# sys.path.append("/home/miriani/Desktop/main")


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))

for n in range(7, 10):
    try:
        url_0 = f"https://ss.ge/ka/jobs/list?Page={n}&JobsDealTypeId=1&Sort.SortExpression=%22OrderDate%22%20DESC,%20%22Applications%22.%22ApplicationId%22%20DESC"
        page_0 = requests.get(url_0)

        for i in range(1, 40):
            try:
                url = "https://ss.ge" + Selector(response=page_0).xpath(f'//*[@id="list"]/div[3]/div/div[{i}]/div[1]/div[1]/div[1]/div/div[1]/a[1]/@href').get()
                print(url)
                page = requests.get(url)


                # ID
                try:
                    _id = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/div/span/text()').get()
                except:
                    _id = ""


                # Position
                try:
                    position = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]/span/text()').get()
                except:
                    position = ""


                # Views
                try:
                    views = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/span/text()').get()
                except:
                    views = ""

                #Date
                try:
                    published = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]/text()').get()
                    published = published.lstrip()
                    published = published.rstrip()
                    # print(published)
                    published = published.split(".")
                    # print(published)
                    publish_day = published[0].rstrip()
                    publish_day = int(publish_day)
                    print(publish_day)
                    # print(int(time.strftime("%d"))-1)
                    publish_month = published[1].rstrip()
                    publish_month = int(publish_month)
                    publish_year = published[2].split("/")[0].rstrip()
                    publish_year = int(publish_year)
                except:
                    publish_day = 0
                    publish_month = 0
                    publish_year = 0
                if yesterday_day != publish_day:
                    print("Not published yesterday")
                    continue


                # Location
                try:
                    location = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div[1]/div[contains(.,"მდებარეობა:")]').get()
                    location = location.split('<span>')
                    location = location[1].split('</span>')[0]
                    location = location.lstrip()
                    location = location.rstrip()
                    location_id = []
                    try:
                        location_id.append({ "city" : f"{location}", "id" : f"{Geonames(location)}" } )
                    except:
                        location_id.append({ "city" : f"{location}", "id" : "611717" } )
                except:
                    location_id = [{"city" : "Tbilisi", "id" : "611717"}]


                # Field
                try:
                    category = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div[1]/div[contains(.,"სფერო:")]').get()
                    category = category.split('<span>')
                    category = category[1].split('</span>')[0]
                    category = category.lstrip()
                    category = category.rstrip()
                except:
                    category = ""


                # Stack
                try:
                    stack = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div[1]/div[contains(.,"სამუშაო გრაფიკი:")]').get()
                    stack = stack.split('<span>')
                    stack = stack[1].split('</span>')[0]
                    stack = stack.lstrip()
                    stack = stack.rstrip()
                    if "სრული განაკვეთი" in stack:
                        stack = "Full-time"
                except:
                    stack = ""


                # Experience
                try:
                    experience = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div[1]/div[contains(.,"გამოცდილება:")]').get()
                    experience = experience.split('<span>')
                    experience = experience[1].split('</span>')[0]
                    experience = experience.lstrip()
                    experience = experience.rstrip()
                except:
                    experience = ""


                # Vacancy owner
                try:
                    vacancy_owner = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/div[1]/div/text()').get()
                    vacancy_owner = vacancy_owner.rstrip()
                    vacancy_owner = vacancy_owner.lstrip()
                except:
                    vacancy_owner = ""


                # Salary
                try:
                    salary = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[3]/div[8]/div').get()
                    salary = remove_tags(salary)
                    salary = salary.replace(" ", "")
                    salary = salary.replace('\n', "")
                    if "-" in salary:
                        salary = 0
                        period = "month"
                    else:
                        if "/თვეში" in salary:
                            salary = salary.replace("/თვეში", "")
                            salary = salary.replace("l", "")
                            salary = int(float(salary.strip()))
                            perion = "month"
                        elif "/დღეში" in salary:
                            salary = salary.replace("/დღეში", "")
                            salary = salary.replace("l", "")
                            salary = int(float(salary.strip()))
                            period = "day"
                        elif "შეთანხმებით" in salary:
                            salary = 0
                            period = "month"
                except Exception as e:
                    print(e)
                    salary = 0
                    period = "month"


                #Email
                try:
                    email = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[contains(.,"კონტაქტი")]').get()
                    email = email.split('"email_contact">')
                    email = email[1].split('</span>')[0]
                except:
                    email = ""


                # Phone
                try:
                    phone = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/div[3]/div[1]/div[1]/div[3]/div/text()').get()
                    phone = phone.replace(" ", "")
                    phone = [{"country_code" : "995", "number" : f"{phone}"}]
                except:
                    phone = ""


                # Description
                try:
                    description = Selector(response=page).xpath('//*[@id="main-body"]/div[2]/div/div[1]/div[1]/div[1]/div/div[3]').get()
                    full_description = remove_tags(description)
                    description = full_description.split("auto translate")
                    description = description[1].split("Show original")
                    description = description[0].rstrip()
                    description = description.lstrip()
                except:
                    description = ""
                if detect(description) == "ru":
                    description_ru = description
                    description_en = Translate(description)
                    description_ka = ""
                elif detect(description) == "et":
                    description_ru = ""
                    description_en = Translate(description)
                    description_ka = description
                else:
                    description_ru = ""
                    description_en = description
                    description_ka = ""


                x = {
                    "ID": _id,
                    "Position": position,
                    "Views": views,
                    "Location": location_id,
                    "Category": category,
                    "Stack": stack,
                    "Experience": experience,
                    "Vacancy_owner": vacancy_owner,
                    "Salary": salary,
                    "Phone": phone,
                    "Email": email,
                    "Description": description,
                    "Full_Description": full_description
                }
                
                # Vacancy User
                if email == "":
                    if phone == "":
                        user_object_id = 100000000000000000000000
                    else:
                        check = userdb.find_one({"phone" : phone})
                        if check is None:
                            new_user_info = {
                                "name" : vacancy_owner,
                                "phone" : phone,
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"phone" : phone})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        else:
                            user_object_id = userdb.find_one({"phone" : phone})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        
                else:
                    check = userdb.find_one({"email" : email})
                    if check is None:
                        if phone == "":
                            new_user_info = {
                                "name" : vacancy_owner,
                                "email" : email,
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"email" : email})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                        else:
                            new_user_info = {
                                "name" : vacancy_owner,
                                "email" : email,
                                "phone" : phone,
                                "created_at" : datetime.datetime.utcnow()
                            }
                            userdb.insert(new_user_info)
                            user_object_id = userdb.find_one({"email" : email})
                            user_object_id = user_object_id["_id"]
                            print(user_object_id)
                    else:
                        user_object_id = userdb.find_one({"email" : email})
                        user_object_id = user_object_id["_id"]
                        print(user_object_id)
                

                # Company ID:
                default_id = companydb.find_one({"name" : "Unknown_Company"})
                default_id = default_id["_id"]


                new_job_info = {
                    "user_id" : ObjectId(f"{user_object_id}"),
                    "job_details" : {
                        "url" : url,
                        "title" : position,
                        "country_id" : "GE",
                        "city" : location_id,
                        "industry" : category,
                        "views" : views,
                        "employment_type" : stack,
                        "description" : [
                            {
                                "language" : "ka",
                                "description" : description_ka,
                            },
                            {
                                "language" : "en",
                                "description" : description_en,
                            },
                            {
                                "language" : "ru",
                                "description" : description_ru,
                            }
                        ],
                        "required" : {
                            "experience" : experience,
                        },
                        "salarycurrency" : "GEL",
                        "salarymin" : salary,
                        "salarymax" : salary,
                        "salaryinterval" : period,
                        "additional_info" : {
                            "suitable_for" : experience
                        },
                        "numberofpositions" : 1,
                        "publishday" : publish_day,
                        "publishmonth" : publish_month,
                        "publishyear" : publish_year,
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "ss.ge",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)


            except Exception as e:
                print(e)
    except:
        print("Finished")
# Position
# //*[@id="list"]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/a[1]/div/span
# //*[@id="list"]/div[3]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/a[1]/div/span

# //*[@id="list"]/div[3]/div/div[4]/div[1]/div[1]/div[1]/div/div[1]/a[1]