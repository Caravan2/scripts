import pymongo
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bson import ObjectId
import datetime
import sys
# sys.path.append("/home/miriani/Desktop/main")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
companydb = mydb["companies"]
 
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
x = int(yesterday.strftime("%d"))
m = int(yesterday.strftime("%m"))
print(x, m)
print(type(x))