from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Remote(
   command_executor='http://worker:4444/wd/hub',
   desired_capabilities={'browserName': 'firefox'})

driver.get("https://www.joemonster.org")
driver.implicitly_wait(20)

try:
    driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div/div/div[1]/div[1]/h2/span")
    print("Have to go through the cookie consent page...")
    acceptButton = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]/span")
    acceptButton.click()
    driver,implicitly_wait(10)
except:
    print("Logging into the page")


loginLink = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/a[1]")
loginLink.click()

# Pass the username and a password
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div[1]/div[2]/form/table/tbody/tr[2]/td[2]/input"))
)
userNameField = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div[2]/form/table/tbody/tr[2]/td[2]/input")
userNameField.send_keys("krichot")
passwordField = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div[2]/form/table/tbody/tr[3]/td[2]/input[1]")
passwordField.send_keys("97roxanne")
driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div[2]/form/table/tbody/tr[4]/td/center/input").click()

print(driver.title)

#driver.implicitly_wait(10)
#driver.close()
