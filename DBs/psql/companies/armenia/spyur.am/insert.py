import pymongo
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Test"]
mycol = mydb["armenia_companies"]

# russian_alphabet = ["А", "Б", "В", "Г", "Д", 'Е', "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]

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

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

driver.implicitly_wait(5)

letters = ['Z']



def Translate(letter, number):
    driver.get(f"https://www.spyur.am/en/yellow_pages-{number}/alpha/{letter}?from=home")

    page_data = []

    for i in range(1, 21):
        try:
            company = driver.find_element_by_xpath(f'//*[@id="ajax-result"]/div/div[{i}]/div[2]/a').text
            c_link = driver.find_element_by_xpath(f'//*[@id="ajax-result"]/div/div[{i}]/div[2]/a').get_attribute("href")
            mycol.insert_one({"company" : company, "c_link" : c_link })
            page_data.append({"company" : company, "c_link" : c_link })
        except:
            company = ""
            c_link = ""

    return page_data








for letter in letters:
    for number in range(1, 300):
        page_data = Translate(letter, number)
        if page_data == []:
            continue
        else:
            print(page_data)







# [0-9]{2,3}(\s|-)[0-9]{2,3}(\s|-)[0-9]{4,7} ( regex for the phone numbers)







# driver.find_element_by_css_selector("#top-menu > ul.nav.navbar-nav.navbar-right.left.aut > li.contact-details > a").click()


# https://translate.google.com/

# /html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]/span




# import requests
# import re
# import time
# from bs4 import BeautifulSoup
# from scrapy.selector import Selector
# from w3lib.html import remove_tags
# from langdetect import detect
# import datetime
# from bson import ObjectId

# letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# for letter in letters:
#     print(letter)
#     url = f"https://www.spyur.am/en/yellow_pages/alpha/{letter}?from=home&tab=yello_p"

#     # payload = {}
#     # files = {}
#     # headers = {
#     # 'Cookie': '__cfduid=dd0625aed6d11eb3c619633bc7d7d0e321595848420; PHPSESSID=jho9f60v3j42tvs3nhqbuhfsd6'
#     # }

#     headers = {
#         "User_Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
#         "Cookie" : "__cfduid=de0e2f56f475a9fd04f46d5709d49fe971595833523; __utmz=75818839.1595833579.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ym_uid=1595833583644130424; _ym_d=1595833583; _ym_isad=2; _ga=GA1.2.2141583591.1595833579; _gid=GA1.2.605629760.1595833584; __gads=ID=861bedc056fa911f:T=1595833588:S=ALNI_MbGLGGZ1LyIpU5CtXm3YB8eRwzPHQ; PHPSESSID=a1rifdm15ct0ad3nat5j2drqd2; __utmc=75818839; __utmt=1; __utma=75818839.2141583591.1595833579.1595846728.1595852022.3; _ym_visorc_24064984=w; _dc_gtm_UA-3003737-1=1; mif.tree:switch=; mif.tree:select=; __utmb=75818839.2.10.1595852023; mif.tree:toggle=%5B%223%22%5D"
#     }

#     page = requests.get(url, headers=headers)
#     print(page.content)

#     company = Selector(response=page).xpath('//*[@id="ajax-result"]/div').get()

#     data = {
#         "company" : company
#     }

#     print(data)