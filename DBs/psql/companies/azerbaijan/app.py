import requests, pymongo
import re, os, io
import time
from pprint import pprint as pp
from PIL import Image
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from langdetect import detect
from bson import ObjectId
import datetime
import sys
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# with open("ids.txt", "r") as f:
#     lines = f.readlines()

# for each in lines:
#     pp(each.strip())

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

driver.implicitly_wait(5)

def Get_Info(_id):
    driver.get('https://www.e-taxes.gov.az/ebyn/commersialChecker.jsp')

    for n in _id:
        driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[3]/td[1]/input').send_keys(n)
        time.sleep(1)

    driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input[2]').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/button').click()

    pp("Good Job")

Get_Info('2004985811')