# Whatsapp Bot
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


options = webdriver.ChromeOptions()
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
driver.get("https://web.whatsapp.com/")
#<==SEND MESSAGE==>
Msg = input("Enter your message: ")
phone = input("Enter the phone number: ")
API = f"https://web.whatsapp.com/send?phone={phone}&text={Msg}"
driver.get(API)
print("Sending message...")


#<==SEND FILE==>
filename = input("Enter the filename: ")
WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-icon='clip']"))).click()
driver.find_element_by_xpath("//input[@type='file']").send_keys(os.getcwd()+'\\'+filename)
time.sleep(3)
WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-icon='send']"))).click()
time.sleep(2)
print("File sent...")