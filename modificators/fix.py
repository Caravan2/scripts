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
 
# "" to Unknown company
find = {"name" : ""}
_id = companydb.find_one(find)

find = {"company_id" : ObjectId(f"{_id['_id']}") }
new = {"$set" : { "company_id" : ObjectId("5efb453fbf493ac1a00cb7b4") } }

x = jobdb.update_many(find, new)
print(x.modified_count, "documents updated.")


# Null to unknown company
find = {"name" : {"$type" : 10}}
_id = companydb.find_one(find)

find = {"company_id" : ObjectId(f"{_id['_id']}") }
new = {"$set" : { "company_id" : ObjectId("5efb453fbf493ac1a00cb7b4") } }

x = jobdb.update_many(find, new)
print(x.modified_count, "documents updated.")

# x = jobdb.find_one({"company_id" : ObjectId("5efc2e5852a5e2698c0984ee") })
# print(x)

# 5efb453fbf493ac1a00cb7b4   Unknown Company