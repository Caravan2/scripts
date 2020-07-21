import requests, re, pymongo, time, datetime
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




months_en = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]


t = time.localtime()
year = time.strftime("%Y", t)
year = int(year)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))
yesterday_month = int(yesterday.strftime("%m"))



def Vacancy(link):
    print("Vacancy started scraping Succesfully")
    url = link
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36", "Accept-Language": "en-US,en;q=0.9,ru;q=0.8"}
    page = requests.get(url, headers=headers)

    # Company
    try:
        company = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[1]/h4/text()').get()
    except:
        company = ""

    # position
    try:
        position = Selector(response=page).xpath('//*[@id="loyal"]/div[2]/div/div[1]/h4/text()').get()
    except:
        position = ""

    # logo
    try:
        logo = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[1]/img/@src').get()
    except:
        logo = ""

    # Job_type
    try:
        job_type = Selector(response=page).xpath('/html/body/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]//text()[2]').get()
        job_type = job_type.strip()
    except:
        job_type = ""


    # Contact Person
    try:
        person = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[2]/div/text()[2]').get()
        person = person.strip()
    except:
        person = ""


    # Email
    try:
        email = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[2]/div/text()[3]').get()
        email = email.strip()
        email = [email]
    except:
        email = []

    # Phone
    try:
        phone = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[2]/div/text()[4]').get()
        phone = phone.strip()
        if "," in phone:
            phones = phone.split(",")
            phone = []
            for each in phones:
                each = each.strip()
                if "+" in each and " " in each:
                    number = each.split(" ", 1)[1].replace('-', "").replace(" ", "")
                    country_code = each.split(" ", 1)[0].replace('+', "")
                    phone.append({"country_code" : country_code, "number" : number})
                elif "+" in each and " " not in each:
                    if "+374" in each:
                        country_code = "374"
                        number = each.replace("+374", "")
                        phone.append({"country_code" : country_code, "number" : number})
                    elif "+1" in each:
                        country_code = "1"
                        number = each.replace("+1", "") 
                        phone.append({"country_code" : country_code, "number" : number})
                    else:
                        country_code = "374"
                        number = each
                        phone.append({"country_code" : country_code, "number" : number})
                elif "+" not in each:
                    number = each.replace('-', "").replace(" ", "")
                    country_code = "374"
                    phone.append({"country_code" : country_code, "number" : number})
        else:
            if "+" in phone and " " in phone:
                number = phone.split(" ", 1)[1].replace('-', "").replace(" ", "")
                country_code = phone.split(" ", 1)[0].replace('+', "")
                phone = [{"country_code" : country_code, "number" : number}]
            elif "+" in phone and " " not in phone:
                if "+374" in phone:
                    country_code = "374"
                    number = phone.replace("+374", "")
                    phone = [{"country_code" : country_code, "number" : number}]
                elif "+1" in phone:
                    country_code = "1"
                    number = phone.replace("+1", "") 
                    phone = [{"country_code" : country_code, "number" : number}]
                else:
                    country_code = "374"
                    number = phone
                    phone = [{"country_code" : country_code, "number" : number}]
            elif "+" not in phone:
                number = phone.replace('-', "").replace(" ", "")
                country_code = "374"
                phone = [{"country_code" : country_code, "number" : number}]

    except Exception as e:
        phone = []


    # Website
    try:
        website = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[2]/div/text()[5]').get()
        website = website.strip()
        if "not" in website:
            website = []
        else:
            website = [website]
    except:
        website = []


    # Published
    try:
        published = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[1]/div[2]/text()[2]').get()
        published = published.strip()
        publish_day = int(published.split("-")[2])
        publish_month = int(published.split("-")[1])
        publish_year = int(published.split("-")[0])
    except:
        publish_day = 0
        publish_month = 0
        publish_year = 0
    if yesterday_day != publish_day or yesterday_month != publish_month:
        print("Not published yesterday")
        return

    # Ends
    try:
        ends = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[1]/div[2]/text()[5]').get()
        ends = ends.strip()
        deadline_day = int(ends.split("-")[2])
        deadline_month = int(ends.split("-")[1])
        deadline_year = int(ends.split("-")[0])
    except:
        deadline_day = 0
        deadline_month = 0
        deadline_year = 0


    # Career Level
    try:
        career_level = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[1]/div[2]/span[1]/text()').get()
        if career_level == None:
            career_level = ""
    except:
        career_level = ""

    # Education
    try:
        education = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[1]/div[2]/span[2]/text()').get()
        if education == None:
            education = ""
    except:
        education = ""

    # Experience
    try:
        experience = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[1]/div[2]/span[3]/text()').get()
        if experience == None:
            experience = ""
    except:
        experience = ""


    # Salary
    try:
        salary = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[1]/div[2]/strong/text()').get()
        if "-" in salary:
            salary = salary.split("-")
            min_salary = salary[0].strip()
            min_salary = int(min_salary.replace(".", ""))
            max_salary = salary[1].strip()
            max_salary = int(max_salary.replace('.', ""))
        elif "-" not in salary and salary != "N/A":
            min_salary = int(salary.replace("."))
            max_salary = int(salary.replace("."))
        else:
            min_salary = 0
            max_salary = 0
    except:
        min_salary = 0
        max_salary = 0

    # Vacancy Description
    try:
        v_description = Selector(response=page).xpath('//*[@id="loyal"]/div[2]/div/div[1]').get()
        v_description = remove_tags(v_description).strip()
        v_description = v_description.replace('\xa0', " ")
    except:
        v_description = ""
    if detect(v_description) == "et":
        try: 
            v_description_en = Translate(v_description)
        except:
            v_description_en = " "
        v_description_am = v_description
    else:
        v_description_en = v_description
        v_description_am = ""

    # Company Description
    try:
        c_description = Selector(response=page).xpath('//*[@id="loyal"]/div[1]/div[2]/div[2]/div[1]/p/text()').get()
        c_description = c_description.strip()
    except:
        c_description = ""
    if detect(c_description) == "et":
        try: 
            c_description_en = Translate(c_description)
        except:
            c_description_en = " "
        c_description_am = c_description
    else:
        c_description_en = c_description
        c_description_am = ""

# c_descrip ; //*[@id="loyal"]/div[1]/div[2]/div[2]/div[1]/p/text()

    data = {
        "company" : company,
        "position" : position,
        "logo" : logo,
        "person" : person,
        "job_type" : job_type,
        "email" : email,
        "phone" : phone,
        "website" : website,
        "publish_day" : publish_day,
        "publish_month" : publish_month,
        "publish_year" : publish_year,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        "career_level" : career_level,
        "education" : education,
        "experience" : experience,
        "min_salary" : min_salary,
        "max_salary" : max_salary,
        "v_description_am" : v_description_am,
        "v_description_en" : v_description_en,
        "c_description_am" : c_description_am,
        "c_description_en" : c_description_en,
    }

    print(data)
    return data


# Vacancy("https://rezume.am/job/2184")