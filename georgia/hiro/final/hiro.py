import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_ka import Geonames
from bia import BiaFunction
from translator import Translate
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

for i in range(2391, 3500):  #It will require to change a range if you decide to run almighty scraper
    try:

        url = f"https://hiro.ge/en/statement/{i}"
        page = requests.get(url)


        try:
            company = Selector(response=page).xpath('/html/body/div[1]/div[2]/main/div[3]/div[2]/p[2]/text()').get()
        except:
            company = ""


        try:
            position = Selector(response=page).xpath('/html/body/div[1]/div[2]/main/div[3]/div[1]/p[2]/text()').get()
        except:
            position = ""


        try:
            published = Selector(response=page).xpath('/html/body/div/div[2]/main/div[3]/div[3]/p[2]/text()').get()
            publish_day = int(published.split(" ")[0])
            publish_month = int(months[f"{published.split(' ')[1]}"])
            publish_year = year
        except:
            publish_day = 0
            publish_month = 0
            publish_year = 0


        try:
            ends = Selector(response=page).xpath('/html/body/div/div[2]/main/div[3]/div[4]/p[2]/text()').get()
            deadline_day = int(ends.split(" ")[0])
            deadline_month = int(months[f"{ends.split(' ')[1]}"])
            deadline_year = year
        except:
            deadline_day = 0
            deadline_month = 0
            deadline_year = 0


        try:
            logo = "https://hiro.ge" + Selector(response=page).xpath('/html/body/div/div[2]/main/div[3]/a/img/@src').get()
        except:
            logo = ""


        try:
            description_raw = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[1]').get()
            description = remove_tags(description_raw)
            description = description.lstrip()
            description = description.rstrip()
            description = description.replace("\n", "")
            description = description.replace("\r", "")
            description = description.replace("\t", "")
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

        try:    
            location = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Location")]').get()
            location = location.split('"tagDesc">')
            location = location[1].split('</')
            location = location[0].rstrip()
            location = location.lstrip()
            location_id = []
            try:
                location_id.append({ "city" : f"{location}", "id" : f"{Geonames(location)}" } )
            except:
                location_id.append({ "city" : f"{location}", "id" : "611717" })
        except:
            location_id = [{"city" : "Tbilisi", "id" : "611717"}]


        try:    
            activity = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Activity")]').get()
            activity = activity.split('"tagDesc">')
            activity = activity[1].split('</')
            activity = activity[0].rstrip()
            activity = activity.lstrip()
        except:
            activity = ""


        try:    
            sector = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Sector")]').get()
            sector = sector.split('"tagDesc">')
            sector = sector[1].split('</')
            sector = sector[0].rstrip()
            sector = sector.lstrip()
        except:
            sector = ""


        try:
            education = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Required level of education")]').get()
            education = re.search(r'"tagDesc">(.*?)</', str(education)).group(1)
            education = education.rstrip()
            education = education.lstrip()
        except:
            education = ""


        try:
            job_type = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Job type")]').get()
            job_type = re.search(r'"tagDesc">(.*?)</', str(job_type)).group(1)
            job_type = job_type.rstrip()
            job_type = job_type.lstrip()
        except:
            job_type = ""


        try:    
            stack = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Work schedule")]').get()
            stack = re.search(r'"tagDesc">(.*?)</', str(stack)).group(1)
            stack = stack.rstrip()
            stack = stack.lstrip()
        except:
            stack = ""


        try:    
            email = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Send cv here")]').get()
            email = re.search(r'"tagDesc">(.*?)</', str(email)).group(1)
            email = email.rstrip()
            email = email.lstrip()
        except:
            email = ""


        try:
            org_type = Selector(response=page).xpath('/html/body/div/div[2]/main/div[4]/div[2]/a[contains(.,"Organization type")]').get()
            org_type = org_type.split('"tagDesc">')
            org_type = org_type[1].split('</')
            org_type = org_type[0].rstrip()
            org_type = org_type.lstrip()
        except:
            org_type = ""

#         print(" company: ", company, "\n position: ", position, published, ends, logo, "\n location :", location, "\n activity: ", activity, "\n sector: ", sector, "\n education: ", education, "\n job_type: ", job_type, "\n stack: ", stack, "\n email: ", email, "\n Organization Type: ", org_type)

        x= {
            "ID": i,
            "Company": company,
            "Postion": position,
            "Published": published,
            "Ends": ends,
            "Logo": logo,
            "Location": location,
            "Activity": activity,
            "Sector": sector,
            "Education": education,
            "job_type": job_type,
            "Stack": stack,
            "Email": email,
            "Description": description,
            "Url": url
        }
        print(x, publish_day, publish_month, publish_year, description_en)
        
        
        
        # Check if company already exists in a collection
        check = companydb.find_one({"name" : company})
        print(check)
        # Dunmping into MongoDB - at this point it has unique structure (meaning, fits for every option)
        if check is None:
            bia_data = BiaFunction(company)
            if "No info" not in bia_data:
                new_company_info = {
                    "name" : company,
                    "industry" : "1",
                    "logo" : logo,
                    "logo_bia" : bia_data["logo"],
                    "type" : activity,
                    "websites" : bia_data["websites"],
                    "emails" : bia_data["emails"],
                    "phones" : bia_data["phones"],
                    "foundation_date" : bia_data["foundation_date"],
                    "vat" : bia_data["vat"],
                    "addressed" : bia_data["addresses"],
                    "business_hours" : bia_data["business_hours"],
                    "created_at" : datetime.datetime.utcnow(),
                    "country" : "GE"
                }
                companydb.insert(new_company_info)
                company_object_id = companydb.find_one({"name" : company})
                company_object_id = company_object_id["_id"]
                print(company_object_id)
                print("done")
            else:
                new_company_info = {
                    "name" : company,
                    "industry" : "1",
                    "logo" : logo,
                    "type" : activity,
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
        
        
        check = userdb.find_one({"email" : email})
        if check is None:
            if email == "":
                user_object_id = 100000000000000000000000
            else:
                new_user_info = {
                    "email" : email,
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
                "employment_type" : stack,
                "type" : job_type,
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
                    "education" : education,
                },
                "salarycurrency" : "GEL",
                "salarymin" : 0,
                "salarymax" : 0,
                "salaryinterval" : "month",
                "additional_info" : {
                    "suitable_for" : education
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
            "source" : "hiro.ge",
            "status" : "active"
        }
        jobdb.insert(new_job_info)
    except Exception as e:
        print(f"shut up \n ------------------------------------------------------------------------- \n {e} \n\n")
# /html/body/div/div[2]/main/div[3]/div[2]/p[2]//*[@id="1194"]/div[3]/p/a
# /html/body/div[1]/div[2]/main/div[3]/div[2]/p[2]
# /html/body/div[1]/div[2]/main/div[3]/div[1]/p[2]
# /html/body/div/div[2]/main/div[3]/div[3]/p[2]
# /html/body/div/div[2]/main/div[3]/div[4]/p[2]
# /html/body/div/div[2]/main/div[3]/a/img
# /html/body/div/div[2]/main/div[4]/div[1]
# /html/body/div/div[2]/main/div[4]/div[2]/a[1]/span[2]
# /html/body/div/div[2]/main/div[4]/div[2]/a[2]/span[2]
# /html/body/div/div[2]/main/div[4]/div[2]/a[4]/span[2]
# /html/body/div/div[2]/main/div[4]/div[2]/a[5]/span[2]