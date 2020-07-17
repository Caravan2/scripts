import pymongo
from cookies import Get_Cookies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["bia.ge"]


driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

for i in range(16447, 45000):
    print(i)
    driver.get(f"https://www.bia.ge/EN/Company/{i}")

    try:
        logo = driver.find_element_by_id('LogoImageUploaderBox').get_attribute("style")
    except:
        logo = ""
    print(logo)

    try:
        name = driver.find_element_by_id('CompanyNameBox').text
    except:
        name = ""
    print(name)

    try:
        trademarks = driver.find_element_by_xpath('//*[@id="TrademarksListBox"]/li').text
    except:
        trademarks = ""
    print(trademarks)

    try:
        legal_form = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[1]/span[2]').text
    except:
        legal_form = ""
    print(legal_form)

    try:
        registration_number = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[3]/td[1]/span[2]').text
    except:
        registration_number = ""
    print(registration_number)

    try:
        registration_authority = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[1]/span[2]').text
    except:
        registration_authority = ""
    print(registration_authority)

    try:
        status = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[1]/span[2]').text
    except:
        status = ""
    print(status)

    try:
        brands = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[1]/td[2]/span[2]').text
    except:
        brands = ""
    print(brands)

    try:
        vat_number = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[2]/span[2]').text
    except:
        vat_number = ""
    print(vat_number)
    
    try:
        registration_date = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[3]/td[2]/span[2]').text
    except:
        registration_date = ""
    print(registration_date)

    try:
        legal_address = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[2]/span[2]').text
    except:
        legal_address = ""
    print(legal_address)

    try:
        working_hours = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[2]/ul/li').text
    except:
        working_hours = ""
    print(working_hours)

    try:
        phone = driver.find_element_by_xpath('//*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span').text
    except:
        phone = ""
    print(phone)

    try:
        website = driver.find_element_by_xpath('//*[@id="ContactsBox"]/table/tbody/tr[3]/td[2]/span').text
    except:
        website = ""
    print(website)

    x = mycol.insert_one({
        "Name": name,
        "Logo": logo,
        "Trademarks": trademarks,
        "Legal_Form": legal_form,
        "Registration_Number": registration_number,
        "Registration_Authority": registration_authority,
        "Status": status,
        "Brands": brands,
        "VAT_Number": vat_number,
        "Registration_Date": registration_date,
        "Legal_Address": legal_address,
        "Working_Hours": working_hours,
        "Phone": phone,
        "Website": website
    })

    # driver.find_element_by_xpath('').text

# driver.find_element_by_xpath('').text

# //*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span/a
# //*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span