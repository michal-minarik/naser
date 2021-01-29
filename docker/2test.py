from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Remote(
   command_executor='http://worker:4444/wd/hub',
   desired_capabilities={'browserName': 'firefox'})

driver.get("https://www.onet.pl")
print(driver.title)

driver.close()
