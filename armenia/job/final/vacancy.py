import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from company import Company_Info




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


# driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")


def Vacancy_Info(link):
    url = link
    page = requests.get(url)

    # Industry
    try:
        industry = Selector(response=page).xpath('/html/body/section/div/div/div/div[2]/div[1]/div/div/div[1]/div[contains(., "Industry:")]').get()
        industry = industry.split('"font-weight-bold">')[1].split('</span>')[0]
    except:
        industry = ""

    # Salary
    try:
        salary = Selector(response=page).xpath('/html/body/section/div/div/div/div[2]/div[1]/div/div/div[1]/div[contains(., "Salary:")]').get()
        salary = salary.split('"font-weight-bold">')[1].split('</span>')[0]
        salary = salary.replace(",", "")
        salary = int(salary)
        if salary is None:
            salary = 0
    except:
        salary = 0


    # Employment type
    try:
        employment_type = Selector(response=page).xpath('/html/body/section/div/div/div/div[2]/div[1]/div/div/div[1]/div[contains(., "Employment type:")]').get()
        employment_type = employment_type.split('"font-weight-bold">')[1].split('</span>')[0]
    except:
        employment_type = ""


    # Ends
    try:
        ends = Selector(response=page).xpath('/html/body/section/div/div/div/div[2]/div[1]/div/div/div[1]/div[contains(., "Deadline:")]').get()
        ends = ends.split('"font-weight-bold">')[1].split('</span>')[0]
        ends = ends.split('/')
        deadline_day = int(ends[0])
        deadline_month = int(ends[1])
        deadline_year = int(ends[2])
    except:
        deadline_day = 0
        deadline_month = 0
        deadline_year = 0


    # Description
    try:
        description = Selector(response=page).xpath('/html/body/section/div/div/div/div[2]/div[1]/div/div/div[2]').get()
        description = remove_tags(description)
        description = description.strip()
    except:
        description = ""
    if detect(description) == "et":
        try: 
            description_en = Translate(description)
        except:
            description_en = ""
        description_am = description
    else:
        description_en = description
        description_am = ""


    # Email
    try:
        email = Selector(response=page).xpath('//*[@id="applyEmail"]/text()').get()
    except:
        email = []


    data = {
        "industry" : industry,
        "salary" : salary,
        "employment_type" : employment_type,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        "description_en" : description_en,
        "description_am" : description_am,
        "email" : email
    }

    # print(data)
    return data

# Vacancy_Info('https://job.am/en/job/24788/grasenyaki-menejer')

