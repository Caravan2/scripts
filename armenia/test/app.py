import requests
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from langdetect import detect
import datetime
from bson import ObjectId

import sys
# sys.path.append("/home/miriani/Desktop/main")


# https://hiro.ge/en/search?publish_up=2

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]


# # type the name of Company and users and jobs will be deleted
# pre = jobdb.find({"source" : "careercenter.am" })
# for each in pre:
#     print(each["_id"])
#     x = jobdb.delete_many({"_id" : each["_id"]})
    
#     if each["user_id"] != ObjectId("100000000000000000000000"):
#         x = userdb.find_one({"_id" : each["user_id"]})
#         print(x)
#         x = userdb.delete_many({"_id" : each["user_id"]})
#         # print(x.deleted_count, " documents deleted.")


x = companydb.delete_many({"country" : "AM"})

print(x.deleted_count, " documents deleted.")


# x = userdb.find({"phones.country_code": "374"}, {"phones": {"$elemMatch": {"country_code": "374"}}});
# for x in x:
#     y = userdb.delete_many({"_id" : x["_id"]})

#     print(y.deleted_count, " documents deleted.")