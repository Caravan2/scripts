from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

driver.implicitly_wait(5)

def Get_Cookies(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver"), chrome_options=options)

    driver.get(f"{link}")
    driver.find_element_by_xpath('//*[@id="page"]/header/div/div/div/div/nav/ul/li[4]/a').click()

    x = driver.get_cookies()

    _ga = x[2]["value"]
    _gid = x[3]["value"]
    WSID = x[5]["value"]
    __RequestVerificationToken = x[4]["value"]
    LastVisit = x[0]["value"]
    _gat = x[1]["value"]

    cookies= f"_ga={_ga}; _gid={_gid}; WSID={WSID}; __RequestVerificationToken={__RequestVerificationToken}; LastVisit={LastVisit}; _gat={_gat}"
    driver.close()
    print(cookies)
    print("Cookies are recieved and browser is closed \n -----------------------------------------------------------------------------------------")
    return cookies