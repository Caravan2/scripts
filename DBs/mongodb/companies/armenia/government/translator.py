from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

driver.implicitly_wait(5)


def Translate(text):

    driver.get(f"https://translate.google.com/")
    driver.find_element_by_xpath('//*[@id="source"]').send_keys(text)

    translated = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]").text
    return translated

