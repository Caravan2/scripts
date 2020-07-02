import pymongo
import time
from geonames_en import Geonames
from vacancy import Vacancy
from company import Company_Search
from cookies import Get_Cookies
from bia import BiaFunction
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bson import ObjectId
import datetime
import sys
# sys.path.append("/home/miriani/Desktop/main")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]

months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
    }

t = time.localtime()
# print(t)
year = time.strftime("%Y", t)
year = int(year)

# Here I get cookies for english language for hr.ge
cookies = Get_Cookies("https://www.hr.ge")
# cookies_2 = Get_Cookies("https://www.hr.ge/customer-details/10908/%e1%83%93%e1%83%90%e1%83%a1%e1%83%90%e1%83%a5%e1%83%9b%e1%83%94%e1%83%91%e1%83%98%e1%83%a1-%e1%83%a1%e1%83%90%e1%83%90%e1%83%92%e1%83%94%e1%83%9c%e1%83%a2%e1%83%9d-%e1%83%94%e1%83%98%e1%83%a9%e1%83%90%e1%83%a0%e1%83%98")


# Here I Open a browser and change a language
driver = webdriver.Chrome("/home/miriani/Desktop/parser/hr/final/drivers/chromedriver")

driver.get(f"https://www.hr.ge/announcements/all?page=1")
driver.find_element_by_css_selector("#top-menu > ul.nav.navbar-nav.navbar-right.left.aut > li.contact-details > a").click()

# Range function to get all the info from home page - it consistos mostly of company and vacancy info. not job info

for page in range(1, 10):
    try:
        driver.get(f"https://www.hr.ge/announcements/all?page={page}")
        for div in range(1, 6):
            try:
                for i in range(1, 2000):
                    try:
                        e = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]")


                        #                              ------------------------------------------- Position Title ----------------------------------------------
                        try:
                            position = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[1]/a/span").text
                        except:
                            position = ""
                        # print("Position scraped, NO_E")


                        #                           -------------------------------------------- Company Name and link ----------------------------------------------------------
                        try:
                            company = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[5]/a").text
                        except:
                            company = ""
                        # print("Company name scraped, NO_E")
                        try:
                            company_link = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[5]/a").get_attribute("href")
                        except:
                            company_link = ""
                        # print("Company_Link scraped, NO_E")



                        #                           --------------------------------------------------- Location  ------------------------------------------------------
                        try:
                            vacancy_locations = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[7]/div[2]").text
                            if "," in vacancy_locations:
                                location_id = []
                                locations = vacancy_locations.split(',')
                                for location1 in locations:
                                    location1 = location1.lstrip()
                                    location1 = location1.rstrip()
                                    try:
                                        # print(Geonames(location1))
                                        location_id.append({ "city" : f"{location1}", "id" : f"{Geonames(location1)}" } )
                                    except:
                                        location_id.append( {"city" : f"{location1}", "id" : "611717" } )
                            elif "," not in vacancy_locations:
                                location_id = [ { "city" : f"{vacancy_locations}", "id" : f"{Geonames(vacancy_locations)}" } ]
                        except:
                            location_id = [ { "city" : "Tbilisi", "id" : "611717" } ]
                        # print("location scraped, NO_E")


                        #                                 ---------------------------------------------------- Publish Date ---------------------------------------------------
                        try:
                            published = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[7]/div[1]/span/span[1]").text
                            published = str(published).split(" ")
                            publish_day = int(published[0]) 
                            publish_month = int(months[f"{published[1]}"])
                            publish_year = year
                        except:
                            publish_day = "" 
                            publish_month = ""
                            publish_year = ""


                        #                                     ----------------------------------------------------- End Date  -------------------------------------------------------
                        try:
                            ends = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[7]/div[1]/span/span[2]").text
                            ends = str(ends).split(" ")
                            deadline_day = int(ends[0])
                            deadline_month = int(months[f"{ends[1]}"])
                            deadline_year = year
                        except:
                            deadline_day = ""
                            deadline_month = ""
                            deadline_year = ""
                        # print("Dates scraped, NO_E")


                        #                                    --------------------------------------------------- Type of Vacancy  -----------------------------------------------------
                        try:
                            vacancy_type = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[8]/div[1]").get_attribute("class")
                        except:
                            vacancy_type = ""

                        if "vipcv" in str(vacancy_type):
                            vacancy_type = "VIP CV"
                        elif "vip" in str(vacancy_type):
                            vacancy_type = "VIP"
                        elif "exclusive" in str(vacancy_type):
                            vacancy_type = "Exclusive"
                        elif "p2" in str(vacancy_type):
                            vacancy_type = "P2"
                        elif "p1" in str(vacancy_type):
                            vacancy_type = "P1"
                        elif len(str(vacancy_type)) == 0:
                            vacancy_type = ""
                        else:
                            vacancy_type = "From cv.ge"
                        # print("Type of Vacancy scraped, NO_E")

                        #                                         ------------------------------------------------------ Link to the Vacancy  ------------------------------------------------------
                        try:
                            vacancy_link = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[1]/a").get_attribute("href")
                            vacancy_link = str(vacancy_link)
                        except:
                            vacancy_link = ""
                        # print("Link to the Vacancy scraped, NO_E")



                        #                                        --------------------------------------------------- Link to Logo of Company -------------------------------------------------------
                        try:
                            logo = e.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[{div}]/div[{i}]/div[4]/a/img").get_attribute("src")
                            logo_link = str(logo)
                        except:
                            logo_link = ""
                        # print("Link of the logo scraped, NO_E")


                        #   This is a check print. in case to make its maintanance easier
                        print("Main Page is scraped Succesfully")

                        
                        # Check if company already exists in a collection
                        check = companydb.find_one({"name" : company})
                        # print(check)
                        # Dunmping into MongoDB - at this point it has unique structure (meaning, fits for every option)
                        if check is None:
                            company_returned = Company_Search(company_link, cookies)
                            bia_data = BiaFunction(company)
                            print(bia_data)
                            if "No info" not in bia_data:
                                print(1)
                                new_company_info = {
                                    "name" : bia_data["name"],
                                    "url" : company_link,
                                    "industry" : "1",
                                    "size" : company_returned["Number_Of_Employees"],
                                    "logo" : logo_link,
                                    "logo_bia" : bia_data["logo"],
                                    "created_at" : datetime.datetime.utcnow(),
                                    "websites" : bia_data["websites"],
                                    "emails" : bia_data["emails"],
                                    "phones" : bia_data["phones"],
                                    "foundation_date" : bia_data["foundation_date"],
                                    "vat" : bia_data["vat"],
                                    "addresses" : bia_data["addresses"],
                                    "business_hours" : bia_data["business_hours"],
                                    "career_center" : {
                                        "description" : company_returned["Description"],
                                        "custom_button_enabled" : True,
                                        "custom_button_title" : "Visit",
                                        "custom_button_url" : company_link
                                    },
                                    "country" : "GE"
                                }
                                print("Company details emerged")
                                company_object_id = companydb.insert(new_company_info)
                                nm = companydb.find_one({"name" : company})
                                print(nm)
                            else:
                                new_company_info = {
                                    "name" : company,
                                    "url" : company_link,
                                    "industry" : "1",
                                    "size" : company_returned["Number_Of_Employees"],
                                    "logo" : logo_link,
                                    "created_at" : datetime.datetime.utcnow(),
                                    "websites" : company_returned["Website"],
                                    "emails" : company_returned["Email"],
                                    "career_center" : {
                                        "description" : company_returned["Description"],
                                        "custom_button_enabled" : True,
                                        "custom_button_title" : "Visit",
                                        "custom_button_url" : company_link
                                    },
                                    "country" : "GE"
                                }
                            companydb.insert(new_company_info)
                            company_object_id = companydb.find_one({"name" : company})
                            company_object_id = company_object_id["_id"]
                            print(company_object_id)
                            print("done")
                        else:
                            company_object_id = companydb.find_one({"name" : company})
                            company_object_id = company_object_id["_id"]
                            print("Company already exists: ", company_object_id)
                        


                        # Vacany User
                        vacancy_returned = Vacancy(vacancy_link, location_id, cookies)
                        if vacancy_returned["Email"] == "":
                            if vacancy_returned["Phone_Number"] == "":
                                user_object_id = 100000000000000000000000
                            else:
                                check = userdb.find_one({"phone" : vacancy_returned["Phone_Number"]})
                                if check is None:
                                    phone = vacancy_returned["Phone_Number"]
                                    add = phone.split(" ", 1)
                                    code = add[0]
                                    code = code.replace("+", "")
                                    number = add[1]
                                    number = number.replace(" ", "")
                                    phone = [{"country_code" : code, "number" : number}]
                                    new_user_info = {
                                        "phone" : phone,
                                        "company_id" : ObjectId(f"{company_object_id}"),
                                        "created_at" : datetime.datetime.utcnow()
                                    }
                                    userdb.insert(new_user_info)
                                    user_object_id = userdb.find_one({"phone" : vacancy_returned["Phone_Number"]})
                                    user_object_id = user_object_id["_id"]
                                    print(user_object_id)
                                else:
                                    user_object_id = userdb.find_one({"phone" : vacancy_returned["Phone_Number"]})
                                    user_object_id = user_object_id["_id"]
                                    print(user_object_id)
                        else:
                            if vacancy_returned["Phone_Number"] == "":
                                check = userdb.find_one({"email" : vacancy_returned["Email"]})
                                if check is None:
                                    new_user_info = {
                                        "email" : vacancy_returned["Email"],
                                        "company_id" : ObjectId(f"{company_object_id}"),
                                        "created_at" : datetime.datetime.utcnow()
                                    }
                                    userdb.insert(new_user_info)
                                    user_object_id = userdb.find_one({"email" : vacancy_returned["Email"]})
                                    user_object_id = user_object_id["_id"]
                                    print(user_object_id)
                                else:
                                    user_object_id = userdb.find_one({"email" : vacancy_returned["Email"]})
                                    user_object_id = user_object_id["_id"]
                                    print(user_object_id)
                            else:
                                check = userdb.find_one({"email" : vacancy_returned["Email"]})
                                if check is None:
                                    phone = vacancy_returned["Phone_Number"]
                                    add = phone.split(" ", 1)
                                    code = add[0]
                                    code = code.replace("+", "")
                                    number = add[1]
                                    number = number.replace(" ", "")
                                    phone = [{"country_code" : code, "number" : number}]
                                    new_user_info = {
                                        "email" : vacancy_returned["Email"],
                                        "phone" : phone,
                                        "company_id" : ObjectId(f"{company_object_id}"),
                                        "created_at" : datetime.datetime.utcnow()
                                    }
                                    userdb.insert(new_user_info)
                                    user_object_id = userdb.find_one({"email" : vacancy_returned["Email"]})
                                    user_object_id = user_object_id["_id"]
                                    print(user_object_id)
                                else:
                                    user_object_id = userdb.find_one({"email" : vacancy_returned["Email"]})
                                    user_object_id = user_object_id["_id"]
                                    print(user_object_id)
                            


                        new_job_info = {
                            "user_id" : ObjectId(f"{user_object_id}"),
                            'company_id' : ObjectId(f"{company_object_id}"),
                            "job_details" : {
                                "url" : vacancy_link,
                                "title" : position,
                                "country_id" : "GE",
                                "city" : location_id,
                                "employment_type" : vacancy_returned["Job_Type"],
                                "description" : [
                                    {
                                        "language" : "ka",
                                        "description" : vacancy_returned["Description_ka"],
                                    },
                                    {
                                        "language" : "en",
                                        "description" : vacancy_returned["Description_en"],
                                    },
                                    {
                                        "language" : "ru",
                                        "description" : vacancy_returned["Description_ru"],
                                    }
                                ],
                                "required" : {
                                    "experience" : vacancy_returned["Experience"],
                                    "language" : vacancy_returned["Languages"],
                                    "education" : vacancy_returned["Education"],
                                    "license" : vacancy_returned["Driver_License"]
                                },
                                "salarycurrency" : "GEL",
                                "salarymin" : vacancy_returned["Min_Salary"],
                                "salarymax" : vacancy_returned["Max_Salary"],
                                "salaryinterval" : "month",
                                "additional_compensation" : vacancy_returned["Bonuses"],
                                "additional_info" : {
                                    "suitable_for" : vacancy_returned["Education"]
                                },
                                "numberofpositions" : 1,
                                "publishday" : publish_day,
                                "publishmonth" : publish_month,
                                "publishyear" : publish_year,
                                "deadlineday" : deadline_day,
                                "deadlinemonth" : deadline_month,
                                "deadlineyear" : deadline_year
                            },
                            "vacancy_type" : vacancy_type,
                            "created_at" : datetime.datetime.utcnow(),
                            "source" : "hr.ge",
                            "status" : "active"
                        }
                        jobdb.insert(new_job_info)

                        print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    except Exception as e:
                        print(e)   
            except:
                print(f"Checking next index in a range                 {div}")   
    except:
        print(f"Checking next index in a range        {page}")

print("DONE") 
    # /html/body/div[3]/div[2]/div[1]/div[1]/div[1]/a

    # /html/body/div[3]/div[2]/div[1]/div[2]/div[1]/a/span
    # /html/body/div[3]/div[2]/div[1]/div[2]/div[7]/div[2]