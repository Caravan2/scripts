from bs4 import BeautifulSoup
import requests
from scrapy.selector import Selector

url = "https://hiro.ge/en/search?publish_up=3"
page = requests.get(url)

company = Selector(response=page).xpath('/html/body/div/div[2]/main/section[1]/@id').get()
print(company)