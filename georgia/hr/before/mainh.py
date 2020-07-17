import requests, re, pymongo, browsercookie
from bs4 import BeautifulSoup
from geonames_en import Geonames

months = {
    "იან": "01",
    "თებ": "02",
    "მარ": "03",
    "აპრ": "04",
    "მაი": "05",
    "ივნ": "06",
    "ივლ": "07",
    "აგვ": "08",
    "სექ": "09",
    "ოქტ": "10",
    "ნოე": "11",
    "დეკ": "12"
}

months_en = {
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

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["test"]

url = "https://www.hr.ge/announcement/120952/ყასაბი-თეთრიწყაროში"
print(url)
cookies = { "Cookie": "_ga=GA1.2.1309521551.1584452197; _gid=GA1.2.261988966.1584452197; __gads=ID=95127d89078bf33f:T=1584453521:S=ALNI_Mbwc4Y6avGIT46ADaTzU1sfdY3LOQ; WSID=v1naylnpsggeey414yeo2vmi; __RequestVerificationToken=XEAyXtmFJM8Z6oV2WNIMRb_073vn4cmNXIzukDWwevfndLmlSQZy3syDAWnSw2YPkjEjSMYPoqh5DQF52fbY9JPbNdHOUZVYjI9zkPPvJY81; LastVisit=2020-03-18T09:13:19.1669901+04:00" }
page = requests.get(url, cookies=cookies)


#Data
soup = BeautifulSoup(page.text, 'html.parser')
details = soup.find('div', attrs={"class": "anncmt-details"})



# --------------------------------------------------------------------------------  Requirements  ------------------------------------------------------------------------------------------------
# Position
position = soup.find('div', attrs={"class": "anncmt-title"}).text
position = position.lstrip()
position = position.rstrip()
print("Position: ", position)



# Company
company = soup.find('div', attrs={"class": "anncmt-customer"}).text
company = company.lstrip()
company = company.rstrip()
print("Company: ", company)



# Dates
try:
    published = str(details).split("<strong>Dates:</strong>")
    published = published[1].split("-")
    ends = published[1].split("</td>")
    ends = ends[0].lstrip()
    ends = ends.rstrip()
    ends = ends.split()
    ends = ends[0]+"/"+months_en[f"{ends[1]}"]
    published = published[0].lstrip()
    published = published.rstrip()
    published = published.split()
    published = published[0]+"/"+months_en[f"{published[1]}"] #Converting verbal month into numeric
except:
    published = ""
    ends = ""
print("Published: ", published)
print("Ends: ", ends)



# Location
try:
    location = str(details).split("<strong>Location:</strong>")
    location = location[1].split("</td>")
    location = location[0].lstrip()
    location = location.rstrip()
    location = location.replace("<span>", "")
    location = location.replace("</span>", "")
    if "," in location:
        location_id = []
        locations = location.split(',')
        for location1 in locations:
            location1 = location1.lstrip()
            location1 = location1.rstrip()
            try:
                # print(Geonames(location1))
                location_id.append({ "Location" : f"{location1}", "ID" : f"{Geonames(location1)}" } )
            except:
                location_id.append( {"Location" : f"{location1}", "ID" : "" } )
    else:
        location_id = [ { "Location" : f"{location}", "ID" : f"{Geonames(location)}" } ]
except:
    location_id = [{"Location" : "", "ID" : ""}]
print("Location: ", location_id)




# Job Type
try:
    jtype = str(details).split("<strong> Employment form:</strong>")
    jtype = jtype[1].split("</td>")
    jtype = jtype[0].lstrip()
    jtype = jtype.rstrip()
except:
    jtype = ""
print("Job_Type: ", jtype)



# Salary + Bonuses
try:
    salary = str(details).split("<strong> Salary:</strong>")
    salary = salary[1].split("</td>")
    salary = salary[0].lstrip()
    salary = salary.rstrip()
    if "+" in salary and "-" not in salary:
        max_salary = salary.split("+")[0].rstrip()
        min_salary = max_salary
        bonuses = "Yes"
    elif "+" in salary and "-" in salary:
        salary = salary.split("+")[0].rstrip()
        max_salary = salary.split("-")[1]
        min_salary = salary.split("-")[0]
        bonuses = "Yes"
    elif "+" not in salary and "-" in salary:
        max_salary = salary.split("-")[1]
        min_salary = salary.split("-")[0]
        bonuses = "No"
    else:
        min_salary = max_salary = salary
        bonuses = "No"
except:
    min_salary = ""
    max_salary = ""
    bonuses = ""
print("Min_Salary: ", min_salary)
print("Max_Salary: ", max_salary)
print("Bonuses: ", bonuses)



# Experience
try:
    experience = str(details).split("<strong> Experience:</strong>")
    experience = experience[1].split("</td>")
    experience = experience[0].lstrip()
    experience = experience.rstrip()
except:
    experience = ""
print("Experience: ", experience)



# Education
try:
    education = str(details).split("<strong> Education:</strong>")
    education = education[1].split("</td>")
    education = education[0].lstrip()
    education = education.rstrip()
except:
    education = ""
print("Education: ", education)



# Languages
try:
    languages = str(details).split("<strong> Languages:</strong>")
    languages = languages[1].split("</span>")
    languages = languages[0].replace("<span>", "").lstrip()
except:
    languages = ""
print("Languages: ", languages)



# Driver's License
try:
    dLicense = str(details).split("<strong> Driving licence:</strong>")
    dLicense = dLicense[1].split("</td>")
    dLicense = dLicense[0].lstrip()
    dLicense = dLicense.rstrip()
    dLicense = dLicense.replace("<span>", "")
    dLicense = dLicense.replace("</span>", "")
except:
    dLicense = ""
print("D_License: ", dLicense)




# -------------------------------------------------------------------------  Info  ------------------------------------------------------------------------------
# E-mail
try:
    email = str(details).split("<strong> Email:</strong>")
    email = email[1].split("</td>")
    email = email[0].lstrip()
    raw_email = email.rstrip()
    email =  re.findall(r'[\w\.-]+@[\w\.-]+', raw_email)[0]
except:
    email = ""
print("Email: ", email)



# Phone Number
try:
    pNumber = str(details).split("<strong> Phone:</strong>")
    pNumber = pNumber[1].split("</td>")
    pNumber = pNumber[0].lstrip()
    pNumber = pNumber.rstrip()
except:
    pNumber = ""
print("Phone_Number: ", pNumber)



# Address
try:
    address = str(details).split("<strong> Address:</strong>")
    address = address[1].split("</td>")
    address = address[0].lstrip()
    address = address.rstrip()
except:
    address = ""
print("Address: ", address)



# Description
try:
    description = soup.find('div', attrs={"class": "firm-descr"}).text
    description = description.rstrip()
except:
    description = ""
print("Description: ", description)



# Web Link
try:
    web_link = re.search("(?P<url>https?://[^\s]+)", description).group("url")
except:
    web_link = ""
print("Web_link: ", web_link)



# Here I check if company exists
x = mycol.find_one({'Company_Name': company})

#Check if vacancy exists: here i append allvacancies of company in a check list
check = []
try:
    for i in range(0, 20):
        check.append(x['vacancies'][i]['Position'])
except:
    check = check

if x is not None and position in check:
    print("position already exists")
elif x is not None:
    data = {
        "Position": position,
        "Published": published,
        "Ends": ends,
        "Location": location_id,
        "Job_Type": jtype,
        "Min_Salary": min_salary,
        "Max_Salary": max_salary,
        "Bonuses": bonuses,
        "Experience": experience,
        "Education": education,
        "Languages": languages,
        "Driver_License": dLicense,
        "Address" : address,
        "Email" : email,
        "Phone_Number": pNumber,
        "Web_Link": web_link,
        "Description": description,
    }

    x = mycol.update({'Company_Name': company}, {'$push': {'vacancies': data}})
    print(x)
else:
    x = mycol.insert_one({
        "Company_Name": company,
        "vacancies": [
            {
            "Position": position,
            "Published": published,
            "Ends": ends,
            "Location": location_id,
            "Job_Type": jtype,
            "Min_Salary": min_salary,
            "Max_Salary": max_salary,
            "Bonuses": bonuses,
            "Experience": experience,
            "Education": education,
            "Languages": languages,
            "Driver_License": dLicense,
            "Address" : address,
            "Email" : email,
            "Phone_Number": pNumber,
            "Web_Link": web_link,
            "Description": description,
            }
        ]
    })
# x = mycol.insert_one(data)

# title = title[1].split('</br>')
# title = title[0]
# print(title)

# x = mycol.find_one( { "vacancies": { "$elemMatch" : { "Bonuses" : "No" } } } )