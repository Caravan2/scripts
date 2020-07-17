import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from geonames_en import Geonames
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




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

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

def Vacancy(link):
    print("request sent for Vacancy succesfully")
    url = link
    print(url)
    # headers = {"Accept-Language": "en-US,en;q=0.5"}
    page = requests.get(url) #headers=headers)


    # Location
    try:
        location = Selector(response=page).xpath('/html/body/main/section/div/div[1]/div[3]/ul/li[3]/a/text()').get()
        location = location.strip()
        location = location.split(",")[0]
        location = [{ "city" : location, "id" : Geonames(location) }]
    except:
        location = [{ "city" : "Yerevan", "id" : "616052" }]

    # Website
    try:
        website = Selector(response=page).xpath('/html/body/main/section/div/div[1]/div[3]/ul/li[4]/a/@href').get()
        if website is None:
            website = []
        else:
            website = [website]
    except:
        website = []



    # Job Type
    try:
        job_type = Selector(response=page).xpath('/html/body/main/section/div/div[2]/div/ul/li[3]/text()').get()
        job_type = job_type.strip()
    except:
        job_type


    # Published
    try:
        published = Selector(response=page).xpath('/html/body/main/section/div/div[2]/div/ul/li[7]/text()').get()
        published = published.strip()
    except:
        published = ""
    if "Երեկ" not in published:
        print("Not published yesterday")
        return

    # Salary
    try:
        salary = Selector(response=page).xpath('/html/body/main/section/div/div[2]/div/ul/li[2]/text()').get()
        salary = salary.strip()
        salary = salary.replace("֏", "")
        salary = salary.replace(",", "")
        salary = salary.replace(" ", "")
        salary = int(salary)
    except:
        salary = 0

    # Gender
    try:
        gender = Selector(response=page).xpath('/html/body/main/section/div/div[2]/div/ul/li[4]/text()[2]').get()
        gender = gender.strip()
    except:
        gender = ""
        

    # Description
    try:
        description = Selector(response=page).xpath('/html/body/main/section/div/div[2]/div/p').get()
        description = remove_tags(description).strip()
    except:
        description = ""
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
    

    # Email
    try:
        driver.get(link)
        email = driver.find_element_by_xpath('/html/body/main/section/div/div[2]/div/p').text
        email = re.findall(r'[\w\.-]+@[\w\.-]+', email)
    except Exception as e:
        email = [e]
    


    data = {
        "location" : location,
        "website" : website,
        "job_type" : job_type,
        "publish_day" : published,
        "salary" : salary,
        "gender" : gender,
        "description_am" : description_am,
        "description_en" : description_en,
        "email" : email
 
    }

    # print(data)
    return data

# Vacancy("https://www.worknet.am/en/job/%D5%A2%D5%A1%D5%B6%D5%BE%D5%B8%D6%80-%D5%BA%D5%A1%D5%B0%D5%A5%D5%BD%D5%BF%D5%AB-%D5%A1%D5%B7%D5%AD%D5%A1%D5%BF%D5%A1%D5%AF%D5%AB%D6%81-4656")