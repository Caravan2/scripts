import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
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

def Company_Info(link):
    url = link
    page = requests.get(url)
    
    # Description
    try:
        description = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]').get()
        description = remove_tags(description).strip()
    except:
        description = ""


    # Type
    try:
        type_of_company = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/text()').get()
    except:
        type_of_company = ""


    # Number of Employees
    try:
        N_of_employees = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]/p[1]/span[3]/text()').get()
    except:
        N_of_employees = ""


    # Address
    try:
        address = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]/p[2]/span[3]/text()').get()
    except:
        address = ""

    
    # Date of Founcation
    try:
        foundation_date = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/table/tbody/tr[3]/td[2]/text()').get()
    except:
        foundation_date = ""


    # Phone
    try:
        phone = Selector(response=page).xpath('//*[@id="hs_contact_block"]/div/div/div[1]/div[2]/span[2]/text()').get()
        if "," in phone:
            phones = []
            phone = phone.split(", ")

            phone1 = phone[0].replace(") ", "")
            number1 = phone1.replace("-", "")
            number1 = number1.replace("(", "")
            phone1 = {"country_code" : "374", "number" : number1}

            phone2 = phone[1].replace(") ", "")
            number2 = phone2.replace("-", "")
            number2 = number2.replace("(", "")
            phone2 = {"country_code" : "374", "number" : number2}

            phones.append(phone1)
            phones.append(phone2)
        else:
            number = phone.replace(") ", "")
            number = number.replace("(", "")
            number = number.replace("-", "")
            phones = [{"country_code" : "374", "number" : number}]
    except:
        phones = ""



    data = {
        "description" : description,
        "type_of_company" : type_of_company,
        "N_of_employees" : N_of_employees,
        "address" : address,
        'foundation_date' : foundation_date,
        "phone" : phones
    }

    print("Company Scraped Succesully")
    return data

# Company_Info("https://staff.am/en/company/aregak-uco-cjsc")