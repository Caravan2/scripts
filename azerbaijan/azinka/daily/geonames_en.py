import requests, re, pymongo
from bs4 import BeautifulSoup


def Geonames(city):
    url = f"https://www.geonames.org/advanced-search.html?q={city}&country=&featureClass=P&continentCode="
    # print(url)

    page = requests.get(url)
    links = []

    #Companies
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.select("td", text = re.compile(f"{city}"))
    # print(data)
    # print(data)
    for data in data:
        if city in str(data):
            links.append(str(data))
            # print(data)
            # print("----------------------------------------------------------------------------")
    # print(links)
    id = str(links[1]).split('href="/')
    id = id[1].split("/")
    id = id[0]
    # print(id)
    return id

# Geonames("Baku")