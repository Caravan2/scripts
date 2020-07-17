import time
import os, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]

# x = jobdb.find({"job_details.title" : "" } )

# for x in x:
#     print(x)

x = jobdb.delete_many( {"job_details.title" : ""} )

print(x.deleted_count, " documents deleted.")