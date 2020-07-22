import requests
import re, os, io
import time
from PIL import Image
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from geonames_en import Geonames
from checkmx import CheckMx
from checkphone import CheckPhone
from langdetect import detect
from bson import ObjectId
import datetime
import sys
import psycopg2
from config import config

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


for i in range(1, 140000):
    try:
        url = f"https://www.bia.ge/En/company/{i}"
        page = requests.get(url)
        
        status = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[5]/td[1]/span[2]/text()').get()
        
        if status == "Operating":
            # Company name
            name = Selector(response=page).xpath('//*[@id="TrademarksListBox"]/li/text()').get()
            
            
            # Vat number
            vat_number = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[2]/td[2]/span[2]/text()').get()
            

            # Address
            try:
                address = Selector(response=page).xpath('//*[@id="tpAboutCompany"]/table/tbody/tr[4]/td[2]/span[2]/text()').get()
                raw = address.split(",")
                postal_code = raw[0]
                if "Tbilisi" in raw[1]:
                    location = raw[1].strip()
                    region = raw[2]
                else:
                    location = raw[2].strip()
                    region = raw[1]
                appartment = raw[3]
                address = {"location" : location, "postal_code" : postal_code, "appartament" : appartment, "region" : region}
            except:
                print("OOOps")
                address = []
            try:            
                location_id = Geonames(location)
            except:
                location_id = None

            # Splitting house number from a street
            possibilities1 = ["str.", "Str.", "Ave.", "ln.", "Ln.", "Plateau", "settlement", "mass.", "sq.", "Sq.", "In.", "In", "Highway", "Alley", "cul-de-sac", "(Temka)", "Plot.", "Range", "Ascent", "Embankment", "Q."]
            possibilities2 = ["Vazha-Pshavela", "Varketili", "Vazisubani", "Sanzona"]
            for each in possibilities1:
                if each in appartment:
                    try:
                        house_number = appartment.split(each)[1]
                        street = appartment.split(each)[0] + each
                        break
                    except:
                        house_number = None
                        street = appartment
                        break
                else:
                    house_number = None
                    street = appartment

            if house_number is None:
                for each in possibilities2:
                    if each in appartment:
                        try:
                            house_number = appartment.split(each)[1]
                            street = appartment.split(each)[0] + each
                            break
                        except:
                            house_number = None
                            street = appartment
                            break
                    else:
                        house_number = None
                        street = appartment


            # if "str." in appartment:
            #     try:
            #         house_number = appartment.split("str.")[1]
            #         street = appartment.split("str.")[0] + "str."
            #     except:
            #         house_number = None
            #         street = appartment
            # elif "Ave." in appartment:
            #     try:
            #         house_number = appartment.split("Ave.")[1]
            #         street = appartment.split("Ave.")[0] + "Ave."
            #     except:
            #         house_number = None
            #         street = appartment
            # else:
            #     house_number = None
            #     street = appartment


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
                business_hours = {"week_days" : None, "hour_from" : None, "hour_to" : None}

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
                        phone.append({"country_code" : code, "number" : number})
                else:
                    phone = phone.lstrip()
                    add = phone.rstrip()
                    add = add.split(" ", 1)
                    code = add[0]
                    code = code.replace("+", "")
                    number = add[1]
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
                "foundation_date" : foundation_date
            }
            print(i)

            if logo != "":
                try:
                    print('Started')
                    img_data = requests.get(logo).content
                    with open('1.jpg', 'wb') as handler:
                        handler.write(img_data)

                    im = Image.open("1.jpg") # Getting the Image
                    fp = io.BytesIO()
                    im.save(fp,"JPEG")
                    output = fp.getvalue()
                    print("Finished")
                except:
                    "Finished2"
                    output = None
            else:
                output = None

            def insert_vendor(name, vat_number, output, foundation_date, emails, phones, websites, business_hours, address, location_id, house_number, street):
                """ insert a new vendor into the vendors table """
                company_sql = """INSERT INTO companies(name, vat_number, logo, foundation_date)
                        VALUES(%s, %s, %s, %s) RETURNING company_id;"""

                email_sql = """INSERT INTO emails(company_id, email, mail_server, provider_server)
                        VALUES(%s, %s, %s, %s);"""

                # website_sql = """INSERT INTO websites(company_id, website)
                #         VALUES(%s, %s);"""

                phone_sql = """INSERT INTO phones(company_id, country_iso, country_code, prefix, phone_number, extension, provider, land_mobile, primary_number)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                
                address_sql = """INSERT INTO addresses(company_id, house_number, floor, apartment, street, post_code, city, region, country, geonames_id)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                
                business_hours_sql = """INSERT INTO business_hours(company_id, days, hour_from, hour_to)
                        VALUES(%s, %s, %s, %s);"""

                conn = None
                update = None
                try:
                    # read database configuration
                    params = config()
                    # connect to the PostgreSQL database
                    conn = psycopg2.connect(**params)
                    # create a new cursor
                    cur = conn.cursor()



                    # Company
                    # execute the INSERT statement
                    cur.execute(company_sql, (name, vat_number, output, foundation_date,))
                    # get the generated id back
                    update = cur.fetchone()[0]



                    # Emails
                    for email in emails:
                        cur.execute(email_sql, ( update, email, email.split("@")[1], CheckMx(email.split("@")[1]), ) )



                    # Phones
                    for phone in phones:
                        print(phone)
                        cur.execute(phone_sql, (update, "GE", "995", phone["number"].split(" ")[0], phone["number"].split(" ")[1], None, CheckPhone(phone["number"].split(" ")[0]), True, True ))



                    # Address
                    cur.execute(address_sql, (update, house_number, None, None, street, address["postal_code"], address["location"], address["region"], "Georgia", location_id ))



                    # Business Hours
                    cur.execute(business_hours_sql, (update, business_hours["week_days"], business_hours["hour_from"], business_hours["hour_to"] ))



                    # commit the changes to the database
                    conn.commit()
                    # close communication with the database
                    cur.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
                    
                print(update)
                return update
            insert_vendor(name, vat_number, output, foundation_date, email, phone, web, business_hours, address, location_id, house_number, street)
        

    except Exception as e:
        print(e)








# def insert_vendor(vendor_name):
#     """ insert a new vendor into the vendors table """
#     sql = """INSERT INTO companies(name, vat_number, logo, foundation_date)
#              VALUES(%s, %s, %s, %s) RETURNING vendor_id;"""
#     conn = None
#     vendor_id = None
#     try:
#         # read database configuration
#         params = config()
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(**params)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql, (vendor_name,))
#         # get the generated id back
#         vendor_id = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

#     print(vendor_id)
#     return vendor_id
# insert_vendor("Miriani")
