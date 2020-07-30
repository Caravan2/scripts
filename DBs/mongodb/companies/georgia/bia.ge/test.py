import requests
import re, os, io
import time
from PIL import Image
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



def insert_vendor():
    """ insert a new vendor into the vendors table """
    company_sql = """INSERT INTO companies(name, vat_number, logo, foundation_date)
            VALUES(%s, %s, %s, %s) RETURNING company_id;"""

    img_data = requests.get("https://www.bia.ge/CompanyMedia.ashx?Id=5400.png").content
    with open('1.jpg', 'wb') as handler:
        handler.write(img_data)

    im = Image.open("1.jpg") # Getting the Image
    fp = io.BytesIO()
    im.save(fp,"JPEG")
    output = fp.getvalue()
    
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
        cur.execute(company_sql, ("Miro", "Miro", output, "Miro",))
        # get the generated id back
        update = cur.fetchone()[0]
        
        

        
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    

    time.sleep(3)
    os.system("rm 1.jpg")

insert_vendor()






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





# \COPY geoname (geonameid,name,asciiname,alternatenames,latitude,longitude,fclass,fcode,country,cc2,admin1,admin2,admin3,admin4,population,elevation,gtopo30,timezone,moddate) FROM 'stuff/allCountries.txt' NULL AS ' ENCODING 'utf-8';\COPY alternatename (alternatenameid,geonameid,isolanguage,alternatename, ispreferredname,isshortname,iscolloquial,ishistoric) FROM 'stuff/alternateNames.txt' NULL AS ' ENCODING 'utf-8';\COPY countryinfo (iso_alpha2,iso_alpha3,iso_numeric,fips_code,name,capital,areainsqkm,population,continent,tld,currencycode,currencyname,phone,postalcodeformat,postalcoderegex,languages,geonameid,neighbors,equivfipscode) FROM 'stuff/countryInfo.txt' NULL AS 'ENCODING 'utf-8';\COPY hierarchy (parentid,childid,type) FROM 'stuff/hierarchy.txt' NULL AS ' ENCODING 'utf-8';\COPY admin1codes (admin1,name,asciiname,geonameid) FROM 'stuff/admin1CodesASCII.txt' NULL AS ' ENCODING 'utf-8';\COPY admin2codes (admin2,name,asciiname,geonameid) FROM 'stuff/admin2Codes.txt' NULL AS ' ENCODING 'utf-8';\COPY languagecodes (iso6393,iso6392,iso6391,languagename) FROM 'stuff/iso-languagecodes.txt' NULL AS ' ENCODING 'utf-8' CSVHEADER DELIMITER E'\t';\COPY featurecodes (fcode,name,description) FROM 'stuff/featureCodes_en.txt' NULL AS ' ENCODING 'utf-8' CSV DELIMITER E'\t';


# \COPY featurecodes (fcode,name,description) FROM '/home/miriani/Desktop/geonames/featureCodes_en.txt' NULL AS '' ENCODING 'utf-8' CSV DELIMITER E'\t';


# \COPY geoname (geonameid,name,asciiname,alternatenames,latitude,longitude,fclass,fcode,country,cc2,admin1,admin2,admin3,admin4,population,elevation,gtopo30,timezone,moddate) FROM '/home/miriani/Desktop/geonames/allCountries.txt' NULL AS ' ENCODING 'utf-8';