import requests, re, pymongo
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from company import Company_Info




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


driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")


def Vacancy(link):
    print("request sent for Vacancy succesfully")
    url = link
    print(url)
    # headers = {"Accept-Language": "en-US,en;q=0.5"}
    page = requests.get(url) #headers=headers)


    # C_Link
    try:
        c_link = Selector(response=page).xpath("/html/body/div[2]/div[3]/div[3]/div[2]/div/div/a/@href").get()
        c_link = "https://staff.am" + c_link
    except:
        c_link = ""


    # Industry
    try:
        industry = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[3]/div[4]/div[1]/div/div/div[1]/div[1]/p[1]/span[2]/text()').get()
    except:
        industry = ""


    # Views
    try:
        views = Selector(response=page).xpath('/html/body/div[2]/div[3]/div[3]/div[4]/div[1]/div/div/div[1]/div[1]/p[2]/span/text()').get()
    except:
        views = ""



    # Followers
    try:
        followers = Selector(response=page).xpath('//*[@id="followers_count"]/text()').get()
    except:
        followers = ""




    # Employment_Term
    try:
        employment_term = Selector(response=page).xpath('//*[@id="job-post"]/div[1]/div[3]/p[1]').get()
        employment_term = employment_term.split("</span> ")
        employment_term = remove_tags(employment_term[1]).strip()
    except:
        employment_term = ""


    # Category
    try:
        category = Selector(response=page).xpath('//*[@id="job-post"]/div[1]/div[3]/p[2]').get()
        category = category.split("</span> ")
        category = remove_tags(category[1]).strip()
    except:
        category = ""


    # Job_Type
    try:
        job_type = Selector(response=page).xpath('//*[@id="job-post"]/div[1]/div[4]/p[1]').get()
        job_type = job_type.split("</span> ")
        job_type = remove_tags(job_type[1]).strip()
    except:
        job_type = ""


    # Deadline
    try:
        ends = Selector(response=page).xpath('//*[@id="job-post"]/div[1]/div[2]/p/text()').get()
        ends = ends.replace("\n", " ")
        ends = ends.replace(" Deadline: ", "")
        ends = ends.split(" ")
        deadline_day = int(ends[0])
        deadline_month = int(months_en[ends[1]])
        deadline_year = int(ends[2])
    except:
        deadline_day = 0
        deadline_month = 0
        deadline_year = 0

    # Description
    try:
        description = Selector(response=page).xpath('//*[@id="job-post"]/div[2]').get()
        description = remove_tags(description)
    except:
        description = ""
    description_en = ""
    description_am = ""
    if detect(description) == "et":
        try: 
            description_en = Translate(description)
        except:
            description_en = ""
        description_am = description
    else:
        description_en = description
        description_am = ""

    # Website
    try:
        website = Selector(response=page).xpath('//*[@id="company-contact-details"]/div[1]/p[contains(., "Website")]/a/@href').get()
        website = [website]
    except:
        website = []


    # Phone Number
    try:
        phone = Selector(response=page).xpath('//*[@id="company-contact-details"]/div[1]/p[contains(., "Phone")]').get()
        phone = phone.split("</span>")[1].split("</p>")[0].strip()
        if "," in phone:
            phones = []
            phone = phone.split(", ")

            phone1 = phone[0].replace(") ", "")
            number1 = phone1.replace("-", "")
            number1 = number1.replace("(", "")
            phone1 = {"country_code" : "374", "number" : number1}

            phone2 = phone[1].replace(") ", "")
            number2 = phone2.replace("-", "")
            number2 = number2.replace("(", "")
            phone2 = {"country_code" : "374", "number" : number2}

            phones.append(phone1)
            phones.append(phone2)
        else:
            number = phone.replace(") ", "")
            number = number.replace("(", "")
            number = number.replace("-", "")
            phones = [{"country_code" : "374", "number" : number}]

    except:
        phones =[]



    # Address
    try:
        address = Selector(response=page).xpath('//*[@id="company-contact-details"]/div[1]/p[contains(., "Address")]').get()
        address = remove_tags(address)
        address = address.replace("Address: ", "").strip()
        # Garegin Hovsepyan 20, Yerevan, Armenia
    except:
        address = ""


    # About Company
    try:
        c_description = Selector(response=page).xpath('//*[@id="company-details"]/div[1]/div[2]').get()
        c_description = remove_tags(c_description).strip()
    except:
        c_description = ""


    # Canditate Level
    try:
        candidate_level = Selector(response=page).xpath('//*[@id="job-post"]/div[2]/h3[contains(., "candidate level")]/span/text()').get()
        if candidate_level == "Not defined":
            candidate_level = ""
    except:
        candidate_level = ""

    
    # Email
    try:
        driver.get(link)
        email = driver.find_element_by_class_name('desc_email').text
        email = [email]
    except:
        email = []
    print("Vacancy Scraped Successfully")

    ccc = Company_Info(c_link)


# //*[@id="followers_count"]
    data = {
        "c_link" : c_link,
        "industry" : industry,
        "views" : views,
        "followers" : followers,
        "employment_term" : employment_term,
        "category" : category,
        "job_type" : job_type,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        "description_en" : description_en,
        "description_am" : description_am,
        "website" : website,
        "phone" : phones,
        "address" : address,
        "company_description" : c_description,
        "candidate_level" : candidate_level,
        "email" : email,
        "type_of_company" : ccc["type_of_company"],
        "N_of_employees" : ccc["N_of_employees"],
        "foundation_date" : ccc["foundation_date"]
    }

    print("Data is ready to be added to a DB")

    return data

# Vacancy('https://staff.am/en/digital-marketing-specialist-219')

# https://staff.am/en/apariki-zargacman-bazni-asxatakic
# https://staff.am/en/digital-marketing-specialist-219

# //*[@id="job-post"]/div[1]/div[2]/p
# //*[@id="job-post"]/div[1]/div[2]/p