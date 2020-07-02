import pymongo
from geonames_en import Geonames
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import time, requests, re
from w3lib.html import remove_tags

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["bia.ge"]

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


driver = webdriver.Chrome("/home/miriani/Desktop/parser/hr/final/drivers/chromedriver")

def BiaFunction(company):
    driver.get(f"https://www.bia.ge/EN")
    
    driver.find_element_by_xpath('//*[@id="Filter_Query"]').send_keys(f"{company}")
    time.sleep(3)
    try:
        link = driver.find_element_by_xpath('/html/body/div[8]/div[2]').get_attribute('data-url')

        page = requests.get(link)

        # Company name
        name = Selector(response=page).xpath('//*[@id="TrademarksListBox"]/li/text()').get()
        
        
        # Vat number
        vat_number = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[2]/span[2]/text()').get()
        

        # Address
        try:
            address = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[2]/span[2]/text()').get()
            raw = address.split(",")
            postal_code = raw[0]
            location = raw[1]
            location = location.lstrip()
            region = raw[2]
            appartment = raw[3]
            city_id = Geonames(location)
            address = {"location" : {"country" : "GE", "city" : { "id" : f"{city_id}", "city" : location }}, "postal_code" : postal_code, "appartament" : appartment, "region" : region}
        except Exception as e:
            print(e)
            address = {}

        # Working hours
        try:
            working_hours = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[2]/ul/li/text()').get()
            raw = working_hours.split(":", 1)
            days = raw[0].split("-")
            till = days[1].lstrip().lower()
            days = []
            for day in weekdays:
                if day != till:
                    days.append(day)
                else:
                    days.append(day)
                    break

            hourfrom = raw[1].split("-")[0]
            hourfrom = hourfrom.lstrip()
            hourfrom = hourfrom.rstrip()

            hourto = raw[1].split("-")[1]
            hourto = hourto.lstrip()
            hourto = hourto.rstrip()
            business_hours = {"week_days" : days, "hour_from" : hourfrom, "hour_to" : hourto}
        except:
            business_hours = {}

        # Foundation Date
        foundation_date = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[3]/td[2]/span[2]/text()').get()

        # Phone
        try:
            phone = Selector(response=page).xpath('//*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span').get()
            phone = remove_tags(phone)
            if "," in phone:
                array = phone.split(",")
                phone = []
                for each in array:
                    each = each.lstrip()
                    each = each.rstrip()
                    each = each.split(" ", 1)
                    code = each[0]
                    code = code.replace("+", "")
                    number = each[1]
                    number = number.replace(" ", "")
                    phone.append({"country_code" : code, "number" : number})
            else:
                phone = phone.lstrip()
                add = phone.rstrip()
                add = add.split(" ", 1)
                code = add[0]
                code = code.replace("+", "")
                number = add[1]
                number = number.replace(" ", "")
                phone = [{"country_code" : code, "number" : number}]
        except:
            phone = []


        # Web   
        try:
            web = Selector(response=page).xpath('//*[@id="ContactsBox"]/table/tbody/tr[3]/td[2]/span').get()
            web = remove_tags(web)
            if "," in web:
                array = web.split(",")
                web = []
                for each in array:
                    each = each.lstrip()
                    each = each.rstrip()
                    web.append(each)
            else:
                web = web.lstrip()
                add = web.rstrip()
                web = [add]
        except:
            web = []


        # Email
        try:
            email = Selector(response=page).xpath('//*[@id="TabPanelBox"]').get()
            email = email.replace("sales@bia.ge", "")
            email = re.findall(r'[\w\.-]+@[\w\.-]+', email)
        except:
            email = []


        # Logo
        try:
            logo = Selector(response=page).xpath('//*[@id="LogoImageUploaderBox"]').get()
            logo = logo.split("url(\'")
            logo = logo[1].split("')")
            logo = logo[0]
        except:
            logo = ""


        info = {
            "name" : name,
            "vat" : vat_number,
            "addresses" : address,
            "business_hours" : business_hours,
            "phones" : phone,
            "websites" : web,
            "emails" : email,
            "foundation_date" : foundation_date,
            "logo" : logo
        }
        print("Bia Scraped Successfully")
        # print(info)
        return info
    except:
        print("No info")
        return "No info"


# BiaFunction("Spar")
    # driver.find_element_by_xpath('//*[@id="Filter_Query"]').send_keys(Keys.RETURN)




        # try:
        #     logo = driver.find_element_by_id('LogoImageUploaderBox').get_attribute("style")
        # except:
        #     logo = ""
        # print(logo)

        # try:
        #     name = driver.find_element_by_id('CompanyNameBox').text
        # except:
        #     name = ""
        # print(name)

        # try:
        #     trademarks = driver.find_element_by_xpath('//*[@id="TrademarksListBox"]/li').text
        # except:
        #     trademarks = ""
        # print(trademarks)

        # try:
        #     legal_form = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[1]/span[2]').text
        # except:
        #     legal_form = ""
        # print(legal_form)

        # try:
        #     registration_number = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[3]/td[1]/span[2]').text
        # except:
        #     registration_number = ""
        # print(registration_number)

        # try:
        #     registration_authority = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[1]/span[2]').text
        # except:
        #     registration_authority = ""
        # print(registration_authority)

        # try:
        #     status = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[1]/span[2]').text
        # except:
        #     status = ""
        # print(status)

        # try:
        #     brands = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[1]/td[2]/span[2]').text
        # except:
        #     brands = ""
        # print(brands)

        # try:
        #     vat_number = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[2]/span[2]').text
        # except:
        #     vat_number = ""
        # print(vat_number)
        
        # try:
        #     registration_date = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[3]/td[2]/span[2]').text
        # except:
        #     registration_date = ""
        # print(registration_date)

        # try:
        #     legal_address = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[2]/span[2]').text
        # except:
        #     legal_address = ""
        # print(legal_address)

        # try:
        #     working_hours = driver.find_element_by_xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[2]/ul/li').text
        # except:
        #     working_hours = ""
        # print(working_hours)

        # try:
        #     phone = driver.find_element_by_xpath('//*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span').text
        # except:
        #     phone = ""
        # print(phone)

        # try:
        #     website = driver.find_element_by_xpath('//*[@id="ContactsBox"]/table/tbody/tr[3]/td[2]/span').text
        # except:
        #     website = ""
        # print(website)

        # x = mycol.insert_one({
        #     "Name": name,
        #     "Logo": logo,
        #     "Trademarks": trademarks,
        #     "Legal_Form": legal_form,
        #     "Registration_Number": registration_number,
        #     "Registration_Authority": registration_authority,
        #     "Status": status,
        #     "Brands": brands,
        #     "VAT_Number": vat_number,
        #     "Registration_Date": registration_date,
        #     "Legal_Address": legal_address,
        #     "Working_Hours": working_hours,
        #     "Phone": phone,
        #     "Website": website
        # })

    # driver.find_element_by_xpath('').text

# driver.find_element_by_xpath('').text

# //*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span/a
# //*[@id="ContactsBox"]/table/tbody/tr[2]/td[2]/span