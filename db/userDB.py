import pymongo
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Jobs"]
_user = mydb["user"]

def UserDB(user):
    x = {
        "company_id": ObjectId(f"{user['company_id']}"),
        "name": user['name'],
        "email":user['email'],
        "phone":user['phone'],
        "created_at":user['created_at']
    }

    y = _user.insert(x)
    print(y)