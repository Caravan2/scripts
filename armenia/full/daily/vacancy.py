import requests, re, pymongo, time, datetime
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geonames_en import Geonames
# from company import Company_Info




months_en = {
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

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]


t = time.localtime()
year = time.strftime("%Y", t)
year = int(year)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))
yesterday_month = int(yesterday.strftime("%m"))

# driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")


def Vacancy(link):
    print("request sent for Vacancy succesfully")
    url = link
    print(url)
    # headers = {"Accept-Language": "en-US,en;q=0.5"}
    page = requests.get(url) #headers=headers)
    
    # Published
    try:
        published = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/ul/li[2]/span/text()[2]').get()
        published = published.strip().split(" ")
        publish_day = int(published[0].split("/")[0])
        publish_month = int(published[0].split("/")[1])
        publish_year = int(published[0].split("/")[2])
    except Exception as e:
        publish_day = 0
        publish_month = 0
        publish_year = 0
    if yesterday_day != publish_day or yesterday_month != publish_month:
        print("Not published yesterday")
        return

    # Location #
    try:
        location = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/ul/li[1]/text()').get()
        location = location.strip()
        location_id = []
        location = {"city" : f"{location}", "id" : f"{Geonames(location)}"}
        location_id.append(location)
    except:
        location_id = [{'city': 'Yerevan', 'id': '616052'}]
    

    # Posted by
    try:
        posted_by = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/p[1]/text()').get()
        posted_by = posted_by.strip()
    except:
        posted_by = ""


    # Email
    try:
        email = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/p[2]/text()').get()
        email = email.strip()
        if email == "":
            email = []
        else:
            email = [email]
    except:
        email = []

    # Workspace
    try:
        workspace = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[2]/div[2]/div[2]/p/text()').get()
        workspace = workspace.strip()
    except:
        workspace = ""

    # Job_type
    try:
        job_type = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[3]/div[2]/div[2]/p/text()').get()
        job_type = job_type.strip()
    except:
        job_type = ""


    # Salary
    try:
        salary = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[4]/div[2]/div[2]/p/text()').get()
        salary = salary.strip().replace("Until ", "")
        if "-" in salary:
            salary = salary.split("-")
            min_salary = int(salary[0].strip())
            max_salary = int(salary[1].strip())
        elif "-" not in salary and salary != '':
            min_salary = int(salary)
            max_salary = int(salary)
        else:
            min_salary = 0
            max_salary = 0    
    except:
        min_salary = 0
        max_salary = 0


    # Education
    try:
        education = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[5]/div[2]/div[2]/p/text()').get()
        education = education.strip()
    except:
        education = ""

    # Experience
    try:
        experience = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[6]/div[2]/div[2]/p/text()').get()
        experience = experience.strip()
    except:
        experience = ""

    # Gender
    try:
        gender = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[7]/div[2]/div[2]/p/i/@class').get()
        if "female" in gender:
            gender = "female"
        elif "male" in gender:
            gender = "male"
        else:
            gender = ''
    except:
        gender = ""



    # Age
    try:
        age = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[8]/div[2]/div[2]/p/text()').get()
        age = age.strip()
    except:
        age = ""

    print(1)


    # Description
    try:
        description = Selector(response=page).xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[10]/div[2]/div/p/text()').get()
        description = description.strip()
    except:
        description = ""
    description_en = ""
    description_am = ""
    try:
        if detect(description) == "et":
            try: 
                description_en = Translate(description)
            except:
                description_en = ""
            description_am = description
        else:
            description_en = description
            description_am = ""
    except:
        description_en = ""
        description_am = ""


    # Phone
    try:
        phone = Selector(response=page).css('#sidebar-border > div.detailed-info-block.form-inline.clearfix > div.clearfix > div > div.user-details').extract()
        phones = []
        for phone in phone:
            phone = remove_tags(phone).strip()
            area_code = "374"
            number = phone.replace(" ", "")
            number = number.replace("-", "")
            number = number.replace("(", "")
            number = number.replace(")", "")
            phones.append({'country_code' : area_code, "number": number})
    except:
        phone = []



    # Username
    try:
        username = Selector(response=page).xpath('//*[@id="sidebar-border"]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/h6/a/text()').get()
        username = username.strip()
    except:
        username = ""



    data = {
        "publish_day" : publish_day,
        "publish_month" : publish_month,
        "publish_year" : publish_year,
        "location_id" : location_id,
        "posted_by" : posted_by,
        "email" : email,
        "workspace" : workspace,
        "job_type" : job_type,
        "min_salary" : min_salary,
        "max_salary" : max_salary,
        "education" : education,
        "experience" : experience,
        "gender" : gender,
        "age" : age,
        "description_am" : description_am,
        "description_en" : description_en,
        "phone" : phones,
        "username" : username
    }

    print(data)
    return data

# Vacancy("https://full.am/en/job/public/view/1163")

# https://full.am/en/job/public/view/12067
# https://full.am/en/job/public/view/1163