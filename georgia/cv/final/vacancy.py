import requests, re, pymongo
from cookies import Get_Cookies
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from geonames_ka import Geonames
from translator import Translate

months = {
    "იან": "01",
    "თებ": "02",
    "მარ": "03",
    "აპრ": "04",
    "მაი": "05",
    "ივნ": "06",
    "ივლ": "07",
    "აგვ": "08",
    "სექ": "09",
    "ოქტ": "10",
    "ნოე": "11",
    "დეკ": "12"
}

months_en = {
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

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]

# scraping a specific vacancy
def Vacancy(link, cookies):
    print("request sent for Vacancy succesfully")
    url = link
    print(url)
    cookies = { "Cookie": cookies }
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"}
    page = requests.get(url, cookies=cookies)

    # Stack
    try:
        stack = Selector(response=page).xpath('//*[@id="page"]/div/div/div/div/div/div[1]/span[2]/text()').get()
    except:
        stack = ""


    # Education
    try:
        education = Selector(response=page).xpath('//*[@id="page"]/div/div/div/div/div/div[3]/span[contains(.,"Education:")]').get()
        education = education.split("</strong>")[1]
        education = education.split("</span>")[0].strip()
    except:
        education = ""


    # Languages
    try:
        languages = Selector(response=page).xpath('//*[@id="page"]/div/div/div/div/div/div[3]/span[contains(.,"Languages:")]').get()
        languages = languages.split("</strong>")[1]
        languages = languages.split("</span>")[0].strip()
    except:
        languages = ""


    # Email
    try:
        email = Selector(response=page).xpath('//*[@id="page"]/main/div/div/div[2]/div/aside[2]/div/div/span/a/text()').get()
    except:
        email = ""
    if email is None:
        email = ""

    # Logo
    try:
        logo = Selector(response=page).xpath('//*[@id="page"]/main/div/div/div[2]/div/aside[3]/div/div/figure/img/@src').get()
    except:
        logo = ""
    if logo is None:
        logo = ""


    # Description
    try:
        description = Selector(response=page).xpath('//*[@id="page"]/main/div/div/div[1]/div[1]/article/div').get()
        description = remove_tags(description)
        description = description.rstrip()
        description = description.lstrip()
        description = description.replace('*', "")
        description = re.sub(r"\s+", " ", description)
    except:
        description = ""
    if detect(description) == "ru":
        description_ru = description
        description_en = Translate(description)
        description_ka = ""
    elif detect(description) == "et":
        description_ru = ""
        try: 
            description_en = Translate(description)
        except:
            description_en = ""
        description_ka = description
    else:
        description_ru = ""
        description_en = description
        description_ka = ""
# contains(text(),"STODOLINK")


    data = {
        "stack" : stack,
        "education" : education,
        "languages" : languages,
        "email" : email,
        "logo" : logo,
        "description" : description,
        "description_ka" : description_ka,
        "description_ru" : description_ru,
        "description_en" : description_en
    }

    print("Vacancy scraped succesfully")
    # print(data)
    return data

# Vacancy('_ga=GA1.2.2101960191.1593693483; _gid=GA1.2.453973920.1593693483; WSID=dnh4xi0r4g1qhrtdiygzn241; __RequestVerificationToken=-ZO3RUnIkifRk6Z-oYnkY1BO7sljzPZhydaRlB23lP0PyUlYkuV0iw3TrkEAsMFrOxCONP1xxAIZh8qzX2tzB_D5DSiXD8G3RyUdZn-wyGE1; LastVisit=2020-07-02T16:38:08.2821857+04:00; _gat=1', 'https://www.cv.ge/announcement/127911/office-housekeeper')