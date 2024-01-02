from selenium import webdriver
import os 
from select import select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC3
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os
from idna import valid_contextj
from datetime import datetime, timedelta
import logging
import shutil



logging.basicConfig(format='%(asctime)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p' , filename='auto_pendency.logs' , level=logging.DEBUG )

op = webdriver.ChromeOptions()
# op.add_argument('--headless=new')
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory' : r"/home/administrator/cbs_bag_hold/data",
    'directory_upgrade': True
}
op.add_experimental_option('prefs' , prefs)
driver = webdriver.Chrome(options=op)
driver.get("http://10.24.0.157/")
time.sleep(5)
print(driver.title)


def login():
    username = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[1]")
    username.send_keys("ca.2670054")
    password = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
    password.send_keys("Chauhan@8091")
    time.sleep(1)
    submit = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/div[4]/button/span")
    submit.click()
    time.sleep(3)


def hubSystem():
    try:
        fac = driver.find_element(By.ID , "selectFacility")
        fac.click()
        fac.send_keys("MotherHub_YKB")
        fac.send_keys(Keys.RETURN)
        print("I am here")
    except Exception as e:
        print(e)
    time.sleep(30)
    try:
        menu = driver.find_element(By.CLASS_NAME , "humberger")
        menu.click()
        time.sleep(3)
        handover = driver.find_element(By.XPATH ,"/html/body/div[1]/div[2]/sidebar-main/div[2]/div[1]/ul[7]/li[1]")
        handover.click()
    except Exception as e:
        print("error at Put screen")
        print(e)


login()
hubSystem()
print("Here")
time.sleep(2000)