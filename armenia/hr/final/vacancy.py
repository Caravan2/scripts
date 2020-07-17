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
    page = requests.get(url) #headers=headers)

    # Description
    try:
        description = Selector(response=page).xpath('/html/body/section[2]/div[3]').get()
        description = remove_tags(description)
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

    # Company Link
    try:
        c_link = Selector(response=page).xpath('/html/body/section[2]/section/div[1]/div[2]/a/@href').get()
        c_link = "http://hr.am" + c_link
    except:
        c_link = ""


    # Email
    try:
        driver.get(c_link)
        email = driver.find_element_by_xpath('/html/body/section[2]/div[10]/div[1]/a').get_attribute("href")
        email = email.replace('mailto:', "")
        email = [email]
    except:
        email = []

    if email == []:
        try:
            email = email = re.findall(r'[\w\.-]+@[\w\.-]+', description)
        except:
            email = []

    # Phone
    try:
        phone = re.search(r"\d{9}", v_description_en).group()
        phone = [{"country_code" : "374", "number" : phone}]
    except:
        phone = []

    data = {
        "description_en" : description_en,
        "description_am" : description_am,
        "c_link" : c_link,
        "email" : email,
        "phone" : phone
    }

    print(data)
    return data

# Vacancy('http://hr.am/vacancy/view/vid/73244/t/')