import pymongo
import time
from geonames_en import Geonames
from vacancy import Vacancy
# from company import Company_Search
from cookies import Get_Cookies
from bia import BiaFunction
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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

# Here I get cookies for english language for cv.ge
cookies = Get_Cookies("https://www.cv.ge")
# cookies_2 = Get_Cookies("https://www.hr.ge/customer-details/10908/%e1%83%93%e1%83%90%e1%83%a1%e1%83%90%e1%83%a5%e1%83%9b%e1%83%94%e1%83%91%e1%83%98%e1%83%a1-%e1%83%a1%e1%83%90%e1%83%90%e1%83%92%e1%83%94%e1%83%9c%e1%83%a2%e1%83%9d-%e1%83%94%e1%83%98%e1%83%a9%e1%83%90%e1%83%a0%e1%83%98")


# Here I Open a browser and change a language
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver"), chrome_options=options)

driver.get(f"https://www.cv.ge/announcements/all?page=1")
driver.find_element_by_xpath('//*[@id="page"]/header/div/div/div/div/nav/ul/li[4]/a').click()


# Range function to get all the info

for page in range(1, 7):
    try:
        driver.get(f"https://www.cv.ge/announcements/all?page={page}")
        for div in range(1, 700):
            try:
                # Position
                try:
                    position = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[1]/p/a').text
                except Exception as e:
                    position = ""
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[1]/p/a
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[2]/div[1]/p/a



                # Company
                try:
                    company = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[1]/div/a').text
                except Exception as e:
                    company = ""
                if company == "":
                    continue
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[1]/div/a
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[2]/div[1]/div/a


                # Location
                try:
                    location = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[1]/div/span').text
                    location_id = [{ "city" : f"{location}", "id" : f"{Geonames(location)}" }]
                except Exception as e:
                    location_id = [{"city" : f"{location}", "id" : "611717" }]
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[1]/div/span



                # type of vacancy
                try:
                    vacancy_type = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[2]/p').text
                except Exception as e:
                    vacancy_type = ""
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[2]/p



                # Published
                try:
                    published = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[2]/span').text
                    published = published.split('-')[0]
                    published = str(published).split(" ")
                    publish_day = int(published[0]) 
                    publish_month = int(months[f"{published[1]}"])
                    publish_year = year
                except Exception as e:
                    publish_day = 0 
                    publish_month = 0
                    publish_year = 0
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[2]/span
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[2]/div[2]/span/


                # Ends
                try:
                    ends = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[2]/span').text
                    ends = ends.split('-')[1]
                    ends = str(ends).split(" ")
                    deadline_day = int(ends[1]) 
                    deadline_month = int(months[f"{ends[2]}"])
                    deadline_year = year
                except Exception as e:
                    deadline_day = 0
                    deadline_month = 0
                    deadline_year = 0


                # Company Link
                try:
                    c_link = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[1]/div/a').get_attribute('href')
                except Exception as e:
                    c_link = ""
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[1]/div/a


                # Vacancy Link
                try:
                    v_link = driver.find_element_by_xpath(f'//*[@id="page"]/main/div/div/div[1]/div[2]/div[{div}]/div[1]/p/a').get_attribute('href')
                except Exception as e:
                    v_link = ""
                # //*[@id="page"]/main/div/div/div[1]/div[2]/div[1]/div[1]/p/a

                print(company, position, location, vacancy_type, publish_day, publish_month, publish_year, deadline_day, deadline_month, deadline_year, c_link, v_link)
            





                # Check if company already exists in a collection
                check = companydb.find_one({"name" : company})
                # print(check)
                # Dunmping into MongoDB - at this point it has unique structure (meaning, fits for every option)
                if check is None:
                    bia_data = BiaFunction(company)
                    print(bia_data)
                    if "No info" not in bia_data:
                        print(1)
                        new_company_info = {
                            "name" : bia_data["name"],
                            "url" : c_link,
                            "industry" : "1",
                            "logo" : bia_data["logo"],
                            "created_at" : datetime.datetime.utcnow(),
                            "websites" : bia_data["websites"],
                            "emails" : bia_data["emails"],
                            "phones" : bia_data["phones"],
                            "foundation_date" : bia_data["foundation_date"],
                            "vat" : bia_data["vat"],
                            "addresses" : bia_data["addresses"],
                            "business_hours" : bia_data["business_hours"],
                            "career_center" : {
                                "description" : "",
                                "custom_button_enabled" : True,
                                "custom_button_title" : "Visit",
                                "custom_button_url" : c_link
                            },
                            "country" : "GE"
                        }
                        print("Company details emerged")
                        company_object_id = companydb.insert(new_company_info)
                        nm = companydb.find_one({"name" : bia_data["name"]})
                        print(nm)
                    else:
                        new_company_info = {
                            "name" : company,
                            "url" : c_link,
                            "industry" : "1",
                            "created_at" : datetime.datetime.utcnow(),
                            "career_center" : {
                                "description" : "",
                                "custom_button_enabled" : True,
                                "custom_button_title" : "Visit",
                                "custom_button_url" : c_link
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




                vacancy_returned = Vacancy(v_link, cookies)



                # Vacancy User
                if vacancy_returned["email"] == "":
                    user_object_id = 100000000000000000000000
                else:
                    check = userdb.find_one({"email" : vacancy_returned["email"]})
                    if check is None:
                        new_user_info = {
                            "email" : vacancy_returned["email"],
                            "company_id" : ObjectId(f"{company_object_id}"),
                            "created_at" : datetime.datetime.utcnow()
                        }
                        userdb.insert(new_user_info)
                        user_object_id = userdb.find_one({"email" : vacancy_returned["email"]})
                        user_object_id = user_object_id["_id"]
                        print(user_object_id)
                    else:
                        user_object_id = userdb.find_one({"email" : vacancy_returned["email"]})
                        user_object_id = user_object_id["_id"]
                        print(user_object_id)
                


                # Vacancy
                new_job_info = {
                    "user_id" : ObjectId(f"{user_object_id}"),
                    'company_id' : ObjectId(f"{company_object_id}"),
                    "job_details" : {
                        "url" : v_link,
                        "logo" : vacancy_returned["logo"],
                        "title" : position,
                        "country_id" : "GE",
                        "city" : location_id,
                        "employment_type" : vacancy_returned["stack"],
                        "description" : [
                            {
                                "language" : "ka",
                                "description" : vacancy_returned["description_ka"],
                            },
                            {
                                "language" : "en",
                                "description" : vacancy_returned["description_en"],
                            },
                            {
                                "language" : "ru",
                                "description" : vacancy_returned["description_ru"],
                            }
                        ],
                        "required" : {
                            "language" : vacancy_returned["languages"],
                            "education" : vacancy_returned["education"],
                        },
                        "salarycurrency" : "GEL",
                        "salarymin" : 0,
                        "salarymax" : 0,
                        "salaryinterval" : "month",
                        "additional_info" : {
                            "suitable_for" : vacancy_returned["education"]
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
                    "source" : "cv.ge",
                    "status" : "active"
                }
                jobdb.insert(new_job_info)

                print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


            except Exception as e:
                print("Check: ", e)
    except Exception as e:
        print("Check: ", e)







