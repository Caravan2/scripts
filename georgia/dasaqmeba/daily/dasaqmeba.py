import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
from translator import Translate
from langdetect import detect
import sys
from bson import ObjectId
import datetime
sys.path.append("/home/miriani/Desktop/main")
# from instantiate import InstantiateJob, InstantiateUser, InstantiateCompany

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Jobs"]
jobdb = mydb["job"]
userdb = mydb["user"]
companydb = mydb["company"]

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


url_0 = ["http://www.dasaqmeba.ge/home/load/?lan=en", "http://www.dasaqmeba.ge/home/load/120?lan=en"]
try:
    page_0 = requests.get(url_0[0])
    for vip in range(1, 50):
        try:
            position = Selector(response=page_0).xpath(f'//*[@id="vipAdsList"]/tbody/tr[{vip}]/td[2]/a[1]/h2/text()').get()
        except:
            position = ""
        
        try:
            url = Selector(response=page_0).xpath(f'//*[@id="vipAdsList"]/tbody/tr[{vip}]/td[2]/a[1]/@href').get() + "?lan=en"
        except:
            url = ""
        
        try:
            company = Selector(response=page_0).xpath(f'//*[@id="vipAdsList"]/tbody/tr[{vip}]/td[3]/a/h3/text()').get()
        except:
            company = ""
        
        try:
            logo = Selector(response=page_0).xpath(f'//*[@id="vipAdsList"]/tbody/tr[{vip}]/td[2]/a[2]/img/@src').get()
        except:
            logo = ""
        
        try:
            published = Selector(response=page_0).xpath(f'//*[@id="vipAdsList"]/tbody/tr[{vip}]/td[4]/text()').get()
            publish_day = published.split(" ")[0].rstrip()
            publish_day = publish_day.lstrip()
            publish_month = int(months[f"{published.split(' ')[1]}"])
            publish_year = year
        except:
            publish_day = ""
            publish_month = ""
            publish_year = ""
        if int(publish_day) < int(time.strftime("%d")) - 1:
            break
        
        try:
            ends = Selector(response=page_0).xpath(f'//*[@id="vipAdsList"]/tbody/tr[{vip}]/td[5]/text()').get()
            deadline_day = int(ends.split(" ")[0])
            deadline_month = int(months[f"{ends.split(' ')[1]}"])
            deadline_year = year
        except:
            deadline_day = ""
            deadline_month = ""
            deadline_year = ""
        
        
        
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        page = requests.get(url, headers={"User-Agent": user_agent})

        try:
            location = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Location")]/td[2]/span[1]/text()').get()
            location = location.rstrip()
            lcoation = location.lstrip()
            location_id = []
            try:
                location_id.append({ "Location" : f"{location}", "ID" : f"{Geonames(location)}" } )
            except:
                location_id.append({ "Location" : f"{location}", "ID" : "" } )
        except:
            location_id = ""

            
        try:
            salary = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Salary")]/td[2]/span[1]/text()').get()
            salary = salary.rstrip()
            salary = salary.lstrip()
        except:
            salary = ""
        if "-" in salary:
            max_salary = salary.split("-")[1]
            min_salary = salary.split("-")[0]
        else:
            max_salary = salary
            min_salary = salary

            
        try:
            age = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Age")]/td[2]/span[1]/text()').get()
            age = age.rstrip()
            age = age.lstrip()
        except:
            age = ""
            
        try:
            category = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Category")]/td[2]/span[1]/text()').get()
            category = category.rstrip()
            category = category.lstrip()
        except:
            category = ""
        
        try:
            working_graphic = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Working graphic")]/td[2]/span[1]/text()').get()
            working_graphic = working_graphic.rstrip()
            working_graphic = working_graphic.lstrip()
        except:
            working_graphic = ""

        try:
            languages = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Languages")]/td[2]/span[1]/text()').get()
            languages = languages.rstrip()
            languages = languages.lstrip()
        except:
            languages = ""
        
        try:
            location = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Location:")]/td[2]/span[1]/text()').get()
            location = lcoation.rstrip()
            location = location.lstrip()
        except:
            location = ""
            
        try:
            phone = Selector(response=page).xpath('//*[@id="main_content"]/div[3]/div[3]/div[2]/p[2]/span[contains(.,"5")]/text()').get()
        except:
            phone = ""

        try:
            email = Selector(response=page).xpath('//*[@id="main_content"]/div[3]/div[3]/div[2]/p[2]/a/span/text()').get()
        except:
            email = ""
            
        x = {
            "Position": position,
            "Company": company,
            "URL": url,
            "Logo": logo,
            "Published": published,
            "Ends": ends,
            "Location": location,
            "Salary": salary,
            "Age": age,
            "Category": category,
            "Working_graphic": working_graphic,
            "Languages": languages,
            "Location": location,
            "Vacancy_type": "VIP",
            "Phone": phone,
            "Email": email
        }
        print(x)

        check = companydb.find_one({"name" : company})
        # Dunmping into MongoDB - at this point it has unique structure (meaning, fits for every option)
        if check is None:
            new_company_info = {
                "name" : company,
                "url" : logo,
                "created_at" : datetime.datetime.utcnow(),
                "country" : "GE"
            }
            companydb.insert(new_company_info)
            company_object_id = companydb.find_one({"name" : company})
            company_object_id = company_object_id["_id"]
            print(company_object_id)
            print("done")
        else:
            company_object_id = companydb.find_one({"name" : company})
            company_object_id = company_object_id["_id"]
            print(company_object_id)
        
        
        if email == "":
            check = userdb.find_one({"phone" : phone})
            if check is None:
                new_user_info = {
                    "email" : email,
                    "phone" : phone,
                    "company_id" : company_object_id,
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
                new_user_info = {
                    "email" : email,
                    "phone" : phone,
                    "company_id" : company_object_id,
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
        
        new_job_info = {
            "user_id" : ObjectId(f"{user_object_id}"),
            'company_id' : ObjectId(f"{company_object_id}"),
            "job_details" : {
                "url" : url,
                "title" : position,
                "country_id" : "GE",
                "city" : location_id,
                "employment_type" : working_graphic,
                "type" : category,
                "required" : {
                    "language" : languages,
                },
                "salarycurrency" : "GEL",
                "salarymin" : min_salary,
                "salarymax" : max_salary,
                "salaryinterval" : "month",
                "numberofpositions" : 1,
                "publishday" : publish_day,
                "publishmonth" : publish_month,
                "publishyear" : publish_year,
                "deadlineday" : deadline_day,
                "deadlinemonth" : deadline_month,
                "deadlineyear" : deadline_year
            },
            "vacancy_type" : "VIP",
            "created_at" : datetime.datetime.utcnow(),
            "status" : "active"
        }
        jobdb.insert(new_job_info)
except Exception as e:
    print(e)

    
    
    
    
    
for url_0 in url_0:
    page_0 = requests.get(url_0)
    try:
        for number in range(1, 500):
            try:
                try:
                    position = Selector(response=page_0).xpath(f'//*[@id="allAdsList"]/tbody/tr[{number}]/td[2]/a[1]/h2/text()').get()
                except:
                    position = ""

                try:
                    url = Selector(response=page_0).xpath(f'//*[@id="allAdsList"]/tbody/tr[{number}]/td[2]/a[1]/@href').get() + "?lan=en"
                except:
                    url = ""

                try:
                    company = Selector(response=page_0).xpath(f'//*[@id="allAdsList"]/tbody/tr[{number}]/td[3]/a/h3/text()').get()
                except:
                    company = ""

                try:
                    logo = Selector(response=page_0).xpath(f'//*[@id="allAdsList"]/tbody/tr[{number}]/td[2]/a[2]/img/@src').get()
                except:
                    logo = ""

                try:
                    published = Selector(response=page_0).xpath(f'//*[@id="allAdsList"]/tbody/tr[{number}]/td[4]/text()').get()
                    publish_day = published.split(" ")[0].rstrip()
                    publish_day = publish_day.lstrip()
                    publish_month = int(months[f"{published.split(' ')[1]}"])
                    publish_year = year
                except:
                    publish_day = ""
                    publish_month = ""
                    publish_year = ""
                if int(publish_day) < int(time.strftime("%d")) - 1:
                    break

                try:
                    ends = Selector(response=page_0).xpath(f'//*[@id="allAdsList"]/tbody/tr[{number}]/td[5]/text()').get()
                    deadline_day = int(ends.split(" ")[0])
                    deadline_month = int(months[f"{ends.split(' ')[1]}"])
                    deadline_year = year
                except:
                    deadline_day = ""
                    deadline_month = ""
                    deadline_year = ""
                    
                    
                    
                    
                user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
                page = requests.get(url, headers={"User-Agent": user_agent})

                try:
                    location = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Location")]/td[2]/span[1]/text()').get()
                    location = location.rstrip()
                    lcoation = location.lstrip()
                    location_id = []
                    try:
                        location_id.append({ "Location" : f"{location}", "ID" : f"{Geonames(location)}" } )
                    except:
                        location_id.append({ "Location" : f"{location}", "ID" : "" } )
                except:
                    location_id = ""


                try:
                    salary = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Salary")]/td[2]/span[1]/text()').get()
                    salary = salary.rstrip()
                    salary = salary.lstrip()
                except:
                    salary = ""
                if "-" in salary:
                    max_salary = salary.split("-")[1]
                    min_salary = salary.split("-")[0]
                else:
                    max_salary = salary
                    min_salary = salary


                try:
                    age = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Age")]/td[2]/span[1]/text()').get()
                    age = age.rstrip()
                    age = age.lstrip()
                except:
                    age = ""

                try:
                    category = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Category")]/td[2]/span[1]/text()').get()
                    category = category.rstrip()
                    category = category.lstrip()
                except:
                    category = ""

                try:
                    working_graphic = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Working graphic")]/td[2]/span[1]/text()').get()
                    working_graphic = working_graphic.rstrip()
                    working_graphic = working_graphic.lstrip()
                except:
                    working_graphic = ""

                try:
                    languages = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Languages")]/td[2]/span[1]/text()').get()
                    languages = languages.rstrip()
                    languages = languages.lstrip()
                except:
                    languages = ""

                try:
                    location = Selector(response=page).xpath(f'//*[@id="main_content"]/div[3]/form/div/div[2]/table/tr[contains(.,"Location:")]/td[2]/span[1]/text()').get()
                    location = lcoation.rstrip()
                    location = location.l
                except:
                    location = ""

                try:
                    phone = Selector(response=page).xpath('//*[@id="main_content"]/div[3]/div[3]/div[2]/p[2]/span[contains(.,"5")]/text()').get()
                except:
                    phone = ""

                try:
                    email = Selector(response=page).xpath('//*[@id="main_content"]/div[3]/div[3]/div[2]/p[2]/a/span/text()').get()
                except:
                    email = ""

                x = {
                    "Position": position,
                    "Company": company,
                    "URL": url,
                    "Logo": logo,
                    "Published": published,
                    "Ends": ends,
                    "Location": location,
                    "Salary": salary,
                    "Age": age,
                    "Category": category,
                    "Working_graphic": working_graphic,
                    "Languages": languages,
                    "Location": location,
                    "Vacancy_type": "VIP",
                    "Phone": phone,
                    "Email": email
                }
                print(x)

                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                print(check)
                # Dunmping into MongoDB - at this point it has unique structure (meaning, fits for every option)
                if check is None:
                    new_company_info = {
                        "name" : company,
                        "url" : logo,
                        "created_at" : datetime.datetime.utcnow(),
                        "country" : "GE"
                    }
                    companydb.insert(new_company_info)
                    company_object_id = companydb.find_one({"name" : company})
                    company_object_id = company_object_id["_id"]
                    print(company_object_id)
                    print("done")
                else:
                    company_object_id = companydb.find_one({"name" : company})
                    company_object_id = company_object_id["_id"]
                    print(company_object_id)
                
                
                if email == "":
                    check = userdb.find_one({"phone" : phone})
                    if check is None:
                        new_user_info = {
                            "email" : email,
                            "phone" : phone,
                            "company_id" : company_object_id,
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
                        new_user_info = {
                            "email" : email,
                            "phone" : phone,
                            "company_id" : company_object_id,
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
                
                new_job_info = {
                    "user_id" : ObjectId(f"{user_object_id}"),
                    'company_id' : ObjectId(f"{company_object_id}"),
                    "job_details" : {
                        "url" : url,
                        "title" : position,
                        "country_id" : "GE",
                        "city" : location_id,
                        "employment_type" : working_graphic,
                        "type" : category,
                        "required" : {
                            "language" : languages,
                        },
                        "salarycurrency" : "GEL",
                        "salarymin" : min_salary,
                        "salarymax" : max_salary,
                        "salaryinterval" : "month",
                        "numberofpositions" : 1,
                        "publishday" : publish_day,
                        "publishmonth" : publish_month,
                        "publishyear" : publish_year,
                        "deadlineday" : deadline_day,
                        "deadlinemonth" : deadline_month,
                        "deadlineyear" : deadline_year
                    },
                    "vacancy_type" : "Standard",
                    "created_at" : datetime.datetime.utcnow(),
                    "source" : "dasaqmeba.ge",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)

            except Exception as e:
                print(e)
            # //*[@id="allAdsList"]/tbody/tr[1]/td[2]/a[1]
            # //*[@id="allAdsList"]/tbody/tr[2]/td[2]/a[1]
    except:
        print("Miriani")
    
    
# //*[@id="vipAdsList"]/tbody/tr[1]/td[2]/a[1]
# //*[@id="vipAdsList"]/tbody/tr[2]/td[2]/a[1]