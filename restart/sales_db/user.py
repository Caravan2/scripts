import pymongo
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bson import ObjectId
import datetime
import sys
# sys.path.append("/home/miriani/Desktop/main")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["user_db"]
jobdb = mydb["jobs"]
companydb = mydb["companies"]
userdb = mydb["user"]


userdb.delete_many({})