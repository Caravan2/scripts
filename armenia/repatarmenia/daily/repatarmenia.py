import requests, json, re
from geonames_en import Geonames
import time
import pymongo
from scrapy.selector import Selector
from w3lib.html import remove_tags
import datetime
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

months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
    }


url = 'http://repatarmenia.org/en/engage/careers/LatestPostsFilter?jsonData={%22Count%22:9,%22LoadMoreCount%22:%229%22,%22SortBy%22:0}'

info = requests.get(url).json()

# data = info.content.decode("utf-8-sig").encode("utf-8")
# data = json.loads(data)

# print(info[0]["CompanyName"])


for n in range(0, 9):

    # Company
    try:
        company = info[n]["CompanyName"]
    except:
        company = ""


    # Position
    try:
        position = info[n]["Title"]
    except:
        position = ""


    # Location
    try:
        location = info[n]["Location"]
        location_id = [{"city" : f"{location}", "id" : f"{Geonames(location)}"}]
    except:
        location_id = [{'city': 'Yerevan', 'id': '616052'}]

    # Logo
    try:
        logo = "http://repatarmenia.org" + info[n]["CareersImage"]
    except:
        logo = ""

    # Description
    try:
        description = info[n]["Description"]
    except:
        description = ""


    # Vacancy Link
    try:
        v_link = "http://repatarmenia.org" + info[n]["ItemDefaultUrl"]
    except:
        v_link = ""


    # Deadline
    try:
        ends = info[n]["DeadLine"]
        ends = ends.split(" ")
        deadline_day = ends[1].replace(",", "")
        deadline_day = int(deadline_day)
        deadline_month = int(months[f"{ends[0]}"])
        deadline_year = int(ends[2])
    except Exception as e:
        deadline_day = e
        deadline_month = 0
        deadline_year = 0

    
    # Email
    try:
        email = re.findall(r'[\w\.-]+@[\w\.-]+', description)[0]
    except Exception as e:
        email = []

    # Publication stuff
    v_page = requests.get(v_link)

    try:
        published = Selector(response=v_page).xpath('//*[@id="ContentplaceholderMain_T7553F19B005_Col00"]/div[2]/div[2]/div[1]/div[1]/text()').get()
        published = published.strip()
        published = published.split(" ")
        publish_day = published[1].replace(",", "")
        publish_day = int(publish_day)
        publish_month = int(months[f"{published[0]}"])
        publish_year = int(published[2])
    except:
        published = 0
        publish_month = 0
        publish_year = 0
    if publish_day != yesterday_day:
        print("Not published Yesterday")
        continue


    data = {
        "company" : company,
        "position" : position,
        "location" : location,
        "logo" : logo,
        # "description" : description,
        "v_link" : v_link,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        "publish_day" : publish_day,
        "publish_month" : publish_month,
        "publish_year" : publish_year,
        "email" : email,
    }
    print("Data is scraped succesfully")


    # Check if company already exists in a collection
    check = companydb.find_one({"name" : company})
    if check is None:
        new_company_info = {
            "name" : company,
            "industry" : "1",
            "logo" : logo,
            "created_at" : datetime.datetime.utcnow(),
            "emails" : email,
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
    if email == []:
        user_object_id = 100000000000000000000000
    else:
        check = userdb.find_one({"email" : email})
        if check is None:
            new_user_info = {
                "email" : email,
                "company_id" : ObjectId(f"{company_object_id}"),
                "created_at" : datetime.datetime.utcnow()
            }
            userdb.insert(new_user_info)
            user_object_id = userdb.find_one({"email" : email})
            user_object_id = user_object_id["_id"]
            print(user_object_id)
        else:
            user_object_id = userdb.find_one({"email" : email})
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
                    "description" : description,
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
        "source" : "repatarmenia.org",
        "status" : "active"
    }
    jobdb.insert(new_job_info)



    print(data)