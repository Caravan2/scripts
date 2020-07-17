import requests, re, pymongo, time, datetime
from langdetect import detect
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from langdetect import detect
from w3lib.html import remove_tags
from translator import Translate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geonames_en import Geonames
# from company import Company_Info




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

t = time.localtime()
year = time.strftime("%Y", t)
year = int(year)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_day = int(yesterday.strftime("%d"))
yesterday_month = int(yesterday.strftime("%m"))


# driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")


def Vacancy(link):
    print("request sent for Vacancy succesfully")
    url = link
    print(url)
    # headers = {"Accept-Language": "en-US,en;q=0.5"}
    page = requests.get(url) #headers=headers)


    # Company
    try:
        company = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lnkCompany"]/text()').get()
    except:
        company = ""


    # Website
    try:
        website = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lnkCompany"]/@href').get()
        website = [website]
    except:
        website = []

    # Position
    try:
        position = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblJobPostTitle"]/text()').get()
    except:
        position = ""

    # logo
    try:
        logo = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_imgCompanyLogoLink"]/@src').get()
        logo = "http://jobfinder.am/" + logo
    except:
        logo = ''


    # Job_type
    try:
        job_type = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblPositionType"]/text()').get()
    except:
        job_type = ""

    # Category
    try:
        category = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblCategory"]/text()').get()
    except:
        category = ""

    # Experience
    try:
        experience = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblExperience"]/text()').get()
    except:
        experience = ""


    # Education
    try:
        education = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblEducation"]/text()').get()
    except:
        education = ""

    # Location
    try:
        location = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblLocation"]/text()').get()
    except:
        location = ""

    # Published
    try:
        published = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblDate"]/text()').get()
        published = published.split(" ")
        published = published[0].split("-")
        publish_day = int(published[0])
        publish_month = int(published[1])
        publish_year = int("20" + published[2])
    except:
        publish_day = 0
        publish_month = 0
        publish_year = 0
    if yesterday_day != publish_day or yesterday_month != publish_month:
        print("Not published yesterday")
        return

    # Ends
    try:
        ends = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblDate"]/text()').get()
        ends = ends.split(" ")
        ends = ends[0].split("-")
        deadline_day = int(ends[0])
        deadline_month = int(ends[1])
        deadline_year = int("20" + ends[2])
    except:
        deadline_day = 0
        deadline_month = 0
        deadline_year = 0

    # Salary
    try:
        salary = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblSalary"]/text()').get()
        salary = int(salary)
    except:
        salary = 0

    # Age
    try:
        age = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblAge"]/text()').get()
        if "--------" in age:
            age = ""
    except:
        age = ""


    # Gender
    try:
        gender = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblGender"]/text()').get()
        if "--------" in gender:
            gender = ""
    except:
        gender = ""

    # Job Description
    try:
        j_description = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblJobDescription"]/text()').get()
    except:
        j_description = ""

    # Job Responsibilities
    try:
        j_responsibilities = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblJobResponsibilities"]/text()').get()
    except:
        j_responsibilities = ""

    # Required Qualifications
    try:
        r_qualifications = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblRequiredQualifications"]').get()
        r_qualifications = remove_tags(r_qualifications)
    except:
        r_qualifications = ""



    # Application Procedure
    try:
        a_procedure = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblApplicationProcedure"]').get()
        a_procedure = remove_tags(a_procedure)
    except:
        a_procedure = remove_tags(a_procedure)

    
    
    
    v_description = j_description + "\n" + j_responsibilities + "\n" + r_qualifications + "\n" + a_procedure
    try:
        if detect(v_description) == "et":
            try: 
                v_description_en = Translate(v_description)
            except:
                v_description_en = ""
            v_description_am = v_description
        else:
            v_description_en = v_description
            v_description_am = ""
    except:
        v_description_en = ""
        v_description_am = ""

    # About Company
    try:
        c_description = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblAboutCompany"]').get()
        c_description = remove_tags(c_description)
    except:
        c_description = ""
    try:
        if detect(c_description) == "et":
            try: 
                c_description_en = Translate(c_description)
            except:
                c_description_en = ""
            c_description_am = c_description
        else:
            c_description_en = c_description
            c_description_am = ""
    except:
        c_description_en = ""
        c_description_am = ""

    # Email
    try:
        email = Selector(response=page).xpath('//*[@id="ctl00_bdyPlaceHolde_jfpanelViewJob_jfJobPreview_lblApplicationProcedure"]/a/text()').get()
        email = email.strip()
        email = [email]
    except:
        email = []

    # Phone
    try:
        phone = re.search(r"\d{9}", v_description_en).group()
        phone = [{"country_code" : "374", "number" : phone}]
    except:
        phone = []


    data = {
        "company" : company,
        "position" : position,
        "website" : website,
        "logo" : logo,
        "job_type" : job_type,
        "category" : category,
        "experience" : experience,
        "education" : education,
        "location" : location,
        "publish_day" : publish_day,
        "publish_month" : publish_month,
        "publish_year" : publish_year,
        "deadline_day" : deadline_day,
        "deadline_month" : deadline_month,
        "deadline_year" : deadline_year,
        "salary" : salary,
        "age" : age,
        "gender" : gender,
        "v_description_am" : v_description_am,
        "v_description_en" : v_description_en,
        "c_description_am" : c_description_am,
        "c_description_en" : c_description_en,
        "email" : email,
        "phone" : phone,
    }

    # print(data)
    return data

# Vacancy('http://jobfinder.am/ViewJob.aspx?JobPostingID=49217')