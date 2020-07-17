import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from w3lib.html import remove_tags
from geonames_en import Geonames
from translator import Translate
# from vacancy import Vacancy
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



for n_page in range(1, 172):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver", chrome_options=options)
        driver.implicitly_wait(5)
        driver.get(f'https://www.list.am/category/29/{n_page}')
        driver.find_element_by_xpath('//*[@id="lbar"]').click()
        driver.find_element_by_xpath('//*[@id="lmenu"]/a[2]').click()
        for a in range(1, 40):
            
            try:
                v_link = driver.find_element_by_xpath(f'//*[@id="contentr"]/div[2]/a[{a}]').get_attribute("href")
                driver.get(v_link)

                # Position
                try:
                    position = driver.find_element_by_xpath('//*[@id="pcontent"]/div/div[1]/div/h1').text
                except:
                    position = ""

                # Company
                try:
                    company = driver.find_element_by_xpath('//*[@id="attr"]/div[2]/div[2]').text
                except:
                    company = ""


                # Job_type
                try:
                    job_type = driver.find_element_by_xpath('//*[@id="attr"]/div[4]/div[2]').text
                except:
                    job_type = ""

                # Employment Type
                try:
                    employment_type = driver.find_element_by_xpath('//*[@id="attr"]/div[3]/div[2]').text
                except:
                    employment_type = ""

                # Salaary
                try:
                    salary = driver.find_element_by_xpath('//*[@id="attr"]/div[5]/div[2]').text
                    salary = salary.replace('֏', '').strip()
                    salary = int(salary)
                except:
                    salary = 0

                # Published
                try:
                    published = driver.find_element_by_xpath('//*[@id="pcontent"]/div/div[4]/span[3]').text
                    published = published.split(",")
                    publish_day = int(published[0].split(" ")[2])
                    publish_month = int(months[published[0].split(" ")[1]])
                    publish_year = int(published[1].split(" ")[1])
                except:
                    published = 0
                    publish_month = 0
                    publish_year = 0


                # Logo
                try:
                    logo = driver.find_element_by_xpath('//*[@id="uinfo"]/div[1]/a/img').get_attribute("src")
                except:
                    logo = ""


                # Description
                try:
                    description = driver.find_element_by_xpath('//*[@id="pcontent"]/div/div[3]').text
                except:
                    description = ""
                description_en = ""
                description_am = ""
                if detect(description) == "et":
                    try: 
                        description_en = Translate(description)
                    except:
                        description_en = ""
                    description_am = description
                else:
                    description_en = description
                    description_am = ""

                # Phone
                try:
                    phone = driver.find_element_by_xpath('//*[@id="uinfo"]/div[2]/div[2]/a').click()
                    phone = driver.find_element_by_xpath('//*[@id="callPhoneInfo"]/div[3]/div').text
                    if "\n" not in phone:
                        phone = phone.replace(" ", "")
                        phone = phone.replace(")", "")
                        phone = phone.replace("(", "")
                        phone = phone.replace("-", "")
                        phone = [{"country_code" : "374", "number" : phone}]
                    else:
                        raw = phone
                        phone = []
                        raw = raw.split('\n')
                        for each in raw:
                            number = each.replace(" ", "")
                            number = number.replace(")", "")
                            number = number.replace("(", "")
                            number = number.replace("-", "")
                            phone.append({"country_code" : "374", "number" : number})

                except:
                    phone = [] 
                
                if phone == []:
                    try:
                        phone = driver.find_element_by_xpath('//*[@id="uinfo"]/div[3]/div[2]/a').click()
                        phone = driver.find_element_by_xpath('//*[@id="callPhoneInfo"]/div[4]/div').text
                        if "\n" not in phone:
                            phone = phone.replace(" ", "")
                            phone = phone.replace(")", "")
                            phone = phone.replace("(", "")
                            phone = phone.replace("-", "")
                            phone = [{"country_code" : "374", "number" : phone}]
                        else:
                            raw = phone
                            phone = []
                            raw = raw.split('\n')
                            for each in raw:
                                number = each.replace(" ", "")
                                number = number.replace(")", "")
                                number = number.replace("(", "")
                                number = number.replace("-", "")
                                phone.append({"country_code" : "374", "number" : number})
                    except:
                        phone = []
                else:
                    a = "Phones are done"



                data = {
                    "position" : position,
                    "company" : company,
                    "job_type" : job_type,
                    "employment_type" : employment_type,
                    "salary" : salary,
                    "publish_day" : publish_day,
                    "publish_month" : publish_month,
                    "publish_year" : publish_year,
                    "phone" : phone,
                    "v_link" : v_link,
                    "logo" : logo,
                    "description_en" : description_en,
                    "description_am" : description_am
                }

                print(data)


                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "industry" : "1",
                        "logo" : logo,
                        "created_at" : datetime.datetime.utcnow(),
                        "phones" : phone,
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
                if phone == []:
                    user_object_id = 100000000000000000000000
                else:
                    check = userdb.find_one({"phones" : phone})
                    if check is None:
                        new_user_info = {
                            "phones" : phone,
                            "company_id" : ObjectId(f"{company_object_id}"),
                            "created_at" : datetime.datetime.utcnow()
                        }
                        userdb.insert(new_user_info)
                        user_object_id = userdb.find_one({"phones" : phone})
                        user_object_id = user_object_id["_id"]
                        print(user_object_id)
                    else:
                        user_object_id = userdb.find_one({"phones" : phone})
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
                        "description" : [
                            {
                                "language" : "am",
                                "description" : description_am,
                            },
                            {
                                "language" : "en",
                                "description" : description_en,
                            }
                        ],
                        "required" : {
                            "experience" : "",
                        },
                        "salarycurrency" : "AMD",
                        "salarymin" : salary,
                        "salarymax" : salary,
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : ""
                        },
                        "numberofpositions" : 1,
                        "publishday" : publish_day,
                        "publishmonth" : publish_month,
                        "publishyear" : publish_year,
                        "deadlineday" : 0,
                        "deadlinemonth" : 0,
                        "deadlineyear" : 0
                    },
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "list.am",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)



                driver.execute_script("window.history.go(-1)")
            
# //*[@id="contentr"]/div[2]/a[1]
# //*[@id="contentr"]/div[2]/a[2]





            except Exception as e:
                print('Check div: ', e)
    except Exception as e:
        print("Check page: ", e)