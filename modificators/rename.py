import time
import os, pymongo
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]


# Rename from phone to phones in userdb
m = 1
while m == 1:
    x = userdb.update({"phone": {"$exists": True}}, {"$rename":{"phone":"phones"}}, False, True);

    m = x["nModified"]
    print("Renames: ", x["nModified"])