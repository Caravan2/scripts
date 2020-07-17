import pymongo
import time, re
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
userdb = mydb["user"]
 
# 5f031017763b482acd39d284
# 5f0307c8763b482acd39d189


# Georgian Version - Phones = []
companies = companydb.find({"phones" : []})

for company in companies:
    desciptions = jobdb.find({"company_id" : ObjectId(company["_id"]), "job_details.description" : { "$exists" : True }})
    phones = []

    for each in desciptions:
        desciption = each["job_details"]["description"][0]["description"]
        for i in range(1, 5):
            try:
                number = re.search(r"(\d{1,3}\s)?\(?\d{1,3}\)?[\s.-]\d{1,3}[\s.-]\d{0,4}?[\s.-]\d{0,4}", desciption).group()
                desciption = desciption.replace(number, "")
                if "995 " in number:
                    number = number.replace("995", "").strip()
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
                else:
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
            except Exception as e:
                a = 0

    # print(phones)
    if phones == []:
        m = 0
    else:
        query = { "_id": ObjectId(company["_id"]) }
        new = { "$set": { "phones": phones } }
        companydb.update_one(query, new)
        print("Numbers Updated +++++++++++++++")




# Georgian Version - Phones are not present
companies = companydb.find({"phones" : { "exists" : False } } )

for company in companies:
    desciptions = jobdb.find({"company_id" : ObjectId(company["_id"]), "job_details.description" : { "$exists" : True }})
    phones = []

    for each in desciptions:
        desciption = each["job_details"]["description"][0]["description"]
        for i in range(1, 5):
            try:
                number = re.search(r"(\d{1,3}\s)?\(?\d{1,3}\)?[\s.-]\d{1,3}[\s.-]\d{0,4}?[\s.-]\d{0,4}", desciption).group()
                desciption = desciption.replace(number, "")
                if "995 " in number:
                    number = number.replace("995", "").strip()
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
                else:
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
            except Exception as e:
                a = 0

    # print(phones)
    if phones == []:
        m = 0
    else:
        query = { "_id": ObjectId(company["_id"]) }
        new = { "$set": { "phones": phones } }
        companydb.update_one(query, new)
        print("Numbers Updated +++++++++++++++")











# Georgian Version - Phones are not present   (9 digit number)
companies = companydb.find({"phones" : [] } )

for company in companies:
    desciptions = jobdb.find({"company_id" : ObjectId(company["_id"]), "job_details.description" : { "$exists" : True }})
    phones = []

    for each in desciptions:
        desciption = each["job_details"]["description"][0]["description"]
        for i in range(1, 5):
            try:
                number = re.search(r"\d{9}", desciption).group()
                desciption = desciption.replace(number, "")
                if "995 " in number:
                    number = number.replace("995", "").strip()
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
                else:
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
            except Exception as e:
                a = 0

    # print(phones)
    if phones == []:
        m = 0
    else:
        query = { "_id": ObjectId(company["_id"]) }
        new = { "$set": { "phones": phones } }
        companydb.update_one(query, new)
        print("Numbers Updated +++++++++++++++")











# English Version - phones = []
for company in companies:
    desciptions = jobdb.find({"company_id" : ObjectId(company["_id"]), "job_details.description" : { "$exists" : True }})
    phones = []

    for each in desciptions:
        desciption = each["job_details"]["description"][1]["description"]
        for i in range(1, 5):
            try:
                number = re.search(r"(\d{1,3}\s)?\(?\d{1,3}\)?[\s.-]\d{1,3}[\s.-]\d{0,4}?[\s.-]\d{0,4}", desciption).group()
                desciption = desciption.replace(number, "")
                if "995 " in number:
                    number = number.replace("995", "").strip()
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
                else:
                    try:
                        number = number.replace(" ", "")
                    except:
                        number = number
                    number = {"country_code" : "995", "number" : number}
                    if number in phones:
                        continue
                    else:
                        phones.append(number)
            except Exception as e:
                a = 0

    # print(phones)
    if phones == []:
        m = 0
    else:
        query = { "_id": ObjectId(company["_id"]) }
        new = { "$set": { "phones": phones } }
        companydb.update_one(query, new)
        print("Numbers Updated +++++++++++++++")




# Emails = []
companies = companydb.find({"emails" : []})

for company in companies:
    descriptions = jobdb.find({"company_id" : ObjectId(company["_id"]), "job_details.description" : { "$exists" : True }})
    emails = []

    for each in desciptions:
        desciption = each["job_details"]["description"][0]["description"]
        
        try:
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', description)[0]
            emails = [emails]
        except:
            emails = []

    # print(emails)
    if emails == []:
        n = 0
    else:
        query = { "_id": ObjectId(company["_id"]) }
        new = { "$set": { "emails": emails } }
        companydb.update_one(query, new)
        print("Emails Updated +++++++++++++++")




# Emails are no present
companies = companydb.find({"emails" : { "$exists" : False }})

for company in companies:
    descriptions = jobdb.find({"company_id" : ObjectId(company["_id"]), "job_details.description" : { "$exists" : True }})
    emails = []

    for each in descriptions:
        desciption = each["job_details"]["description"][0]["description"]
        
        try:
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', description)[0]
            emails = [emails]
        except:
            emails = []

    # print(emails)
    if emails == []:
        n = 0
    else:
        query = { "_id": ObjectId(company["_id"]) }
        new = { "$set": { "emails": emails } }
        companydb.update_one(query, new)
        print("Emails Field added +++++++++++++++")


# Perfecto Regexo
# (\+\d{1,3}\s)?\(?\d{1,3}\)?[\s.-]\d{1,3}[\s.-]\d{1,4}[\s.-]\d{1,4}

















#   --------------------------------------------------------------- USERDB --------------------------------------------------------------------------------------------------------------------------------









# # Georgian Version - Phones are not present
# users = userdb.find( { "phones" : { "exists" : False } } )
# for i in users:
#     print(i)

# for user in users:
#     desciptions = jobdb.find({"company_id" : ObjectId(user["_id"]), "job_details.description" : { "$exists" : True }})
#     phones = []

#     for each in desciptions:
#         desciption = each["job_details"]["description"][0]["description"]
#         for i in range(1, 5):
#             try:
#                 number = re.search(r"(\d{1,3}\s)?\(?\d{1,3}\)?[\s.-]\d{1,3}[\s.-]\d{0,4}?[\s.-]\d{0,4}", desciption).group()
#                 desciption = desciption.replace(number, "")
#                 if "995 " in number:
#                     number = number.replace("995", "").strip()
#                     try:
#                         number = number.replace(" ", "")
#                     except:
#                         number = number
#                     number = {"country_code" : "995", "number" : number}
#                     if number in phones:
#                         continue
#                     else:
#                         phones.append(number)
#                 else:
#                     try:
#                         number = number.replace(" ", "")
#                     except:
#                         number = number
#                     number = {"country_code" : "995", "number" : number}
#                     if number in phones:
#                         continue
#                     else:
#                         phones.append(number)
#             except Exception as e:
#                 a = 0

#     # print(phones)
#     if phones == []:
#         m = 0
#     else:
#         query = { "_id": ObjectId(user["_id"]) }
#         new = { "$set": { "phones": phones } }
#         userydb.update_one(query, new)
#         print("In userdb - Numbers Updated +++++++++++++++")























