import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Jobs"]
_company = mydb["company"]

def CompanyDB(company):

    x = {
        "status":"ACTIVATED",
        "name":f"{company['name']}",
        "url":f"{company['url']}",
        "logo": f"{company['logo']}",
        "industry":f"{company['industry']}",
        "type":f"{company['type']}",
        "size":f"{company['size']}",
        "parking":f"{company['parking']}",
        "business_hours":f"{company['business_hours']}",
        "addresses":[
            {
                "name":"",
                "location":{
                    "country":f"{company['country_id']}",
                    "city":f"{company['city_int']}",
                    "name":f"{company['city_name']}",
                    "subdivision":"Herat"
                },
                "zip_code" : f"{company['zip_code']}",
                "apartment":f"{company['apartment']}",
                "street":f"{company['street']}",
                "phones":f"{company['phones']}",
                "geopos":{
                    "lantitude":f"{company['lantitude']}",
                    "longitude":f"{company['longitude']}"
                },
                "is_primary":True,
                "business_hours":f"{company['business_hours']}",
                "websites":f"{company['website']}"
            }
        ],
        "foundation_date":f"{company['company_created_at']}",
        "emails":[
            {
                "email":f"{company['email']}",
                "activated":True,
                "primary":True
                }
            ],
        "phones":[
            {
                "country_code":{
                    "code":f"{company['country_code']}",
                    "country_id":f"{company['country_id']}"
                },
                "number":f"{company['phones']}",
                "activated":True,
                "primary":True
            }
        ],
        "created_at":f"{company['info_created_at']}",
        "websites":[
            {
                "website":f"{company['website']}"
            }
        ],
        "vat":f"{company['vat']}",
        "invited_by":"",
        "company_type":f"{company['type']}",
        "career_center":{
            "is_opened":True,
            "title":f"{company['title']}",
            "description":f"{company['description']}",
            "cb_button_enabled":True,
            "custom_button_enabled":True,
            "custom_button_title":"Visit",
            "custom_button_url":f"{company['url']}",
            "created_at":f"{company['company_created_at']}"
        }
    }

    y = _company.insert(x)
    print(y)