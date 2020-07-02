from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/home/miriani/Desktop/parser/hr/drivers/chromedriver")

driver.get(f"https://www.hr.ge/announcements/all?page=1")
driver.find_element_by_css_selector("#top-menu > ul.nav.navbar-nav.navbar-right.left.aut > li.contact-details > a").click()

for page in range(1, 10):
    driver.get(f"https://www.hr.ge/announcements/all?page={page}")
    try:
        try:
            for i in range(1, 2000):
                e = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[1]/div[{i}]")
                print(e)
        except:
                try:
                    for i in range(1, 2000):
                        e = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[2]/div[{i}]")
                        print(e)
                except:
                    try:
                        for i in range (1, 2000):
                            e = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[3]/div[{i}]")
                            print(e)
                    except:
                        try:
                            for i in range (1, 2000):
                                e = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[4]/div[{i}]")
                                print(e)
                        except:
                            try:
                                for i in range (1, 2000):
                                    e = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[5]/div[{i}]")
                                    print(e)
                            except:
                                print("done")
    except:
        print("Completely Done")
# /html/body/div[3]/div/div[3]/div[1]
# /html/body/div[3]/div/div[3]/div[2]

# /html/body/div[3]/div/div[5]/div[1]

# /html/body/div[3]/div/div[7]/div[1]

# /html/body/div[3]/div/div[8]/div[1]

# /html/body/div[3]/div[2]/div[6]/nav/ul/li[7]/a
# /html/body/div[3]/div[2]/div[4]/nav/ul/li[8]/a/span
# /html/body/div[3]/div[2]/div[3]/nav/ul/li[8]/a/span

# /html/body/div[3]/div[2]/div[1]/div[1]
# /html/body/div[3]/div[2]/div[2]/div[1]
# /html/body/div[3]/div[2]/div[3]/div[1]
# /html/body/div[3]/div[2]/div[5]/div[1]

# /html/body/div[3]/div[2]/div[2]/div[340]