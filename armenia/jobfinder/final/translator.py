import pymongo
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]

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

def Translate(text):
    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(5)

    driver.get(f"https://translate.google.com/")
    driver.find_element_by_xpath('//*[@id="source"]').send_keys(text)

    translated = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]").text
    return translated


# driver.find_element_by_css_selector("#top-menu > ul.nav.navbar-nav.navbar-right.left.aut > li.contact-details > a").click()


# https://translate.google.com/

# /html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]/span