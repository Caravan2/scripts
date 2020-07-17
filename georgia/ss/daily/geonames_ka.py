import requests, re, pymongo
from bs4 import BeautifulSoup

transform = {
    "ა" : "a",
    "ბ" : "b",
    "გ" : "g",
    "დ" : "d",
    "ე" : "e",
    "ვ" : "v",
    "ზ" : "z",
    "თ" : "t",
    "ი" : "i",
    "კ" : "k",
    "ლ" : "l",
    "მ" : "m",
    "ნ" : "n",
    "ო" : "o",
    "პ" : "p",
    "ჟ" : "zh",
    "რ" : "r",
    "ს" : "s",
    "ტ" : "t",
    "უ" : "u",
    "ფ" : "f",
    "ქ" : "k",
    "ღ" : "gh",
    "ყ" : "k",
    "შ" : "sh",
    "ჩ" : "ch",
    "ც" : "ts",
    "ძ" : "dz",
    "წ" : "ts",
    "ჭ" : "ch",
    "ხ" : "kh",
    "ჯ" : "j",
    "ჰ" : "h"
}

def Geonames(city):
    word = ""
    city = city.lstrip()
    city = city.rstrip()
    for letter in city:
        word += transform[f'{letter}']
    # print(word)

    url = f"https://www.geonames.org/search.html?q={word}&country="
    # print(url)
    page = requests.get(url)

    links = []

    #Companies
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.select("a")
    # print(data)
    for data in data:
        if word in str(data):
            links.append(data)
            # print(data)
            # print("----------------------------------------------------------------------------")
    # print(links[1])
    id = str(links[1]).split('href="/')
    id = id[1].split("/")
    id = id[0]
    # print(id)
    return id
