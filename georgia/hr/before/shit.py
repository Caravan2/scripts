from googletrans import Translator
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]

x = mycol.find_one({'Name': 'IT SPE'})
print(x)

# x = Translator().translate("კურიერი ჭიათურაში").src
# print(x)