import requests, re, pymongo
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]



def Company_Search(link, cookies):
    url = link
    # print(url)
    cookies = { "Cookie": cookies }
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"}
    page = requests.get(url, cookies=cookies)


    #scrape
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.select("div", attrs={"class" : "details"})
    # print(data)

    #Name of Company
    try:
        name = soup.find("div", attrs={"class" : "g-title-item"}).text
        name = name.lstrip()
        name = name.rstrip()
    except:
        name = ""
    # print("Name: ", name)


    # Industry
    try:
        industry = str(data).split("<strong>Industry:</strong>")
        industry = industry[1].split("</td>")
        industry = industry[0].lstrip()
        industry = industry.rstrip()
    except:
        industry = "0"
    # print("Industry: ", industry)


    # Description
    try:
        description = soup.find("div", attrs={"class" : "g-description-item"}).text
        description = description.lstrip()
        description = description.rstrip()
    except:
        description = ""
    # print("Description: ", description)


    # Number of empoloyees
    try:
        N_employees = str(data).split("<strong>Number of employees:</strong>")
        N_employees = N_employees[1].split("</td>")
        N_employees = N_employees[0].lstrip()
        N_employees = N_employees.rstrip()
    except:
        N_employees = ""
    # print("N_employees: ", N_employees)


    # Email
    try:
        email = str(data).split("<strong>Email:</strong>")
        email = email[1].split("</td>")
        email = email[0].lstrip()
        email = email.rstrip()
        email = [email]
    except:
        email = []
    # print("Email: ", email)


    # Website
    try:
        website = str(data).split("<strong>Website:</strong>")
        website = website[1].split("</td>")
        website = website[0].lstrip()
        raw_website = website.rstrip()
        website = website.split('/">')
        website = website[1].split("</a>")
        website = [website[0]]
    except:
        website = []
    # print("Website: ", website)


    # # Logo
    # try:
    #     logo = soup.find("img", attrs={"alt" : "Logo"})
    #     logo = str(logo).split('src="')
    #     logo = logo[1].split('"/>')[0]
    # except:
    #     logo = ""
    # print("Logo: ", logo)

    # Find the company in the database
    data = {
        "Industry": industry,
        "Description": description,
        "Number_Of_Employees": N_employees,
        "Email": email,
        "Website": website,
        "_Hr_Updated": "Yes"
    }
    print("No error in company")
    return data


# Email
# try:
#     email = re.findall(r'[\w\.-]+@[\w\.-]+', description)[0]
# except:
#     try:
#         email = str(details).split("<strong> ელ. ფოსტა:</strong>")
#         email = email[1].split("</td>")
#         email = email[0].lstrip()
#         raw_email = email.rstrip()
#         email =  re.findall(r'[\w\.-]+@[\w\.-]+', raw_email)[0]
#     except:
#         email = ""
# print(email)



# USEFULL STUFF:
# data = soup.find_all('div',text = re.compile('შემადგენლობა'),attrs={"class" : "BNeawe s3v9rd AP7Wnd"})
# .replace(" a ", " ")
# re.search(r'<h3>(.*?)</h3>', str(data)).group(1)
# https://jobs.ge/ge/?view=client&client={HERE GOES COMPANY NAME}
# https://www.hr.ge/announcements/all?page=2    Pagination
# ,attrs={"class":"ann-listing-item p2    "}