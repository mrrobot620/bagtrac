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

bags = []

logging.basicConfig(format='%(asctime)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p' , filename='auto_pendency.logs' , level=logging.DEBUG )

op = webdriver.ChromeOptions()
op.add_argument('--headless=new')
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory' : r"/home/administrator/cbs_bag_hold/data",
    'directory_upgrade': True
}
op.add_experimental_option('prefs' , prefs)
driver = webdriver.Chrome(options=op)


def hms_login():
    driver.get("http://10.24.0.157/")
    time.sleep(5)
    print(driver.title)
    username = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[1]")
    username.send_keys("ca.2670054")
    password = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
    password.send_keys("Chauhan@8091")
    time.sleep(3)
    password.send_keys(Keys.RETURN)
    # submit = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/div[4]/button/span")
    # submit.click()


def hubSystem():
    try:
        fac = driver.find_element(By.ID , "selectFacility")
        fac.click()
        fac.send_keys("MotherHub_YKB")
        fac.send_keys(Keys.RETURN)
        print("I am here")
    except Exception as e:
        print(e)
    time.sleep(20)
    try:
        menu = driver.find_element(By.CLASS_NAME , "humberger")
        menu.click()
        time.sleep(3)
        handover = driver.find_element(By.XPATH ,"/html/body/div[1]/div[2]/sidebar-main/div[2]/div[1]/ul[7]/li[1]")
        handover.click()
    except Exception as e:
        print("error at Put screen")
        print(e)

#EKOJKOJ-660865526
        
# bag_ids = ["EPATBLL-1374339"]
# ptc = "36b93e66-2cdb-4859-8ed9-e2796bd522dd"

def auto_bag_put(bag_id, ptc):
    def put_bag(bag):
        try:
            print(f"Sucessful:   The bag = {bag} & ptc = {ptc}")
            bag_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div/form/div[1]/input")
            bag_input.send_keys(bag)
            bag_input.send_keys(Keys.RETURN)
            # put_status = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div/form/div[2]/div/label").text
            time.sleep(1)
            put_status = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div/form/div[2]/div/label").text
            print(put_status)
            if "Put" in put_status:
                bag_input.send_keys(ptc)
                bag_input.send_keys(Keys.RETURN)
                print("Putting Done")
                return True
            else:
                print(put_status)
                print("Put is not Present")
                return False
        except Exception as e:
            print(f"The bag = {bag} & ptc = {ptc}")
            print(f"Error putting bag {bag}: {e}")
            return False
    time.sleep(2)
    success = put_bag(bag_id)
    if not success:
        success = put_bag(bag_id)
        if not success:
            print(f"Failed to put bag {bag_id} even after retry.")
        
