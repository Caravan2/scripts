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



url = "http://jobfinder.am/default.aspx"
page = requests.get(url)

number = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_grdJobs_JFTabContainer_JFJobs_lblSearchCriteria"]/b/text()').get()
print(number)
number = int(number)


for i in range(2, number+4):
    try:
        # Vacancy Link
        try:
            v_link = Selector(response=page).xpath(f'//*[@id="ctl00_bdyPlaceHolde_grdJobs_JFTabContainer_JFJobs_grdResultView"]/tr[{i}]/td[1]/table/tr/td/a[2]/@href').get()
            v_link = "http://jobfinder.am/" + v_link
        except:
            v_link = ""


        data = {
            "v_link" : v_link,
        }

        returned = Vacancy(v_link)


        # Check if company already exists in a collection
        check = companydb.find_one({"name" : returned["company"]})
        if check is None:
            new_company_info = {
                "name" : returned["company"],
                "industry" : "1",
                "logo" : returned["logo"],
                "created_at" : datetime.datetime.utcnow(),
                "websites" : returned["website"],
                "emails" : returned["email"],
                "phones" : returned["phone"],
                "career_center" : {
                    "description" : returned["c_description_en"],
                    "custom_button_enabled" : True,
                    "custom_button_title" : "Visit",
                    "custom_button_url" : returned["website"]
                },
                "country" : "AM"
            }
            print("Company details emerged")
            company_object_id = companydb.insert(new_company_info)
            nm = companydb.find_one({"name" : returned["company"]})
            print(nm)
        else:
            company_object_id = companydb.find_one({"name" : returned["company"]})
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
                "title" : returned["position"],
                "country_id" : "AM",
                "city" : [{'city': 'Yerevan', 'id': '616052'}],
                "employment_type" : returned["job_type"],
                "description" : [
                    {
                        "language" : "am",
                        "description" : returned["v_description_am"],
                    },
                    {
                        "language" : "en",
                        "description" : returned["v_description_en"],
                    }
                ],
                "required" : {
                    "experience" : returned["experience"],
                    "education" : returned["education"],
                    "gender" : returned["gender"],
                    "age": returned["age"],
                },
                "salarycurrency" : "AMD",
                "salarymin" : returned["salary"],
                "salarymax" : returned["salary"],
                "salaryinterval" : "month",
                "additional_info" : {
                    "suitable_for" : returned["education"]
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
            "source" : "jobfinder.am",
            "status" : "active"
        }
        jobdb.insert(new_job_info)



        print(returned)
    except:
        print("Check number: ", i)

print(Done)










# for i in range(2, 3):
#     driver.find_element_by_xpath(f'//*[@id="ctl00_bdyPlaceHolde_grdJobs_JFTabContainer_JFJobs_grdResultView"]/tbody/tr[{i}]/td[1]/table/tbody/tr/td/a[2]').click()
#     print(i)

#     # Company
#     try:
#         company = driver.find_element_by_xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lnkCompany"]').text
#     except:
#         company = ""

#     # Company Link
#     try:
#         c_link = driver.find_element_by_xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lnkCompany"]').get_attribute("href")
#     except:
#         c_link = ""

    

#     data = {
#         "company" : company,
#         "c_link" : c_link,
#     }

#     print(data)
    # driver.switch_to.window(original_window)

# //*[@id="ctl00_bdyPlaceHolde_grdJobs_JFTabContainer_JFJobs_grdResultView"]/tbody/tr[2]/td[1]/table/tbody/tr/td/a[2]
# //*[@id="ctl00_bdyPlaceHolde_grdJobs_JFTabContainer_JFJobs_grdResultView"]/tbody/tr[3]/td[1]/table/tbody/tr/td/a[2]

# //*[@id="ctl00_bdyPlaceHolde_grdJobs_JFTabContainer_JFJobs_grdResultView"]/tbody/tr[16]/td[1]/table/tbody/tr/td/a[2]