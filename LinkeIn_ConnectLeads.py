from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv
from tkinter import Tk
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.driver_cache import DriverCacheManager
import numpy as np
import math
import pathlib 
import os
from datetime import date
import random

def connect_from_csv(input_file, startDate: date, skipLeadsPerDayNumber: int):
    driver = constructDriver(True)
    print(f'number of rows = {len(input_file)}')
    skip = (date.today() - startDate).days * skipLeadsPerDayNumber
    print(f'skipping {skip} items')
    print(f'remaining number of lines: {len(input_file[skip:skip+skipLeadsPerDayNumber])}')
    input()
    for row in input_file[skip:skip+skipLeadsPerDayNumber]:
        attempts = 0
        try:
            attempts += 1
            driver.get(row['ProfileUrl'])
            button_more = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '(.//button[@aria-label="More actions"])[last()]'))
            )           
            button_more.click()
            time.sleep(random.uniform(1.0, 5.0))

            WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, './/div[@class="class="pvs-overflow-actions-dropdown__content artdeco-dropdown__content artdeco-dropdown--is-dropdown-element artdeco-dropdown__content--justification-left artdeco-dropdown__content--placement-bottom ember-view"]'))
            )       
            connect_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '(.//div[@class="artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view full-width display-flex align-items-center"]/*[contains(text(), "Connect")]/..)[last()]'))
            )  
            time.sleep(random.uniform(1.0, 5.0))
            full_name = driver.find_element(By.XPATH, './/div[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text.strip()
            print(f'Connected {full_name}')
            time.sleep(random.uniform(1.0, 5.0))
        except Exception as error:
            if attempts == 10:
                driver = constructDriver(True)
            if attempts > 10:
                driver.quit()
                raise error
            else:
                print(error)
                time.sleep(10)   
    driver.quit()

def constructDriver(headless = False):
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')

    if headless:
        options.add_argument("--window-size=1280,700")
        options.add_argument("--headless=new")
        options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    cache_manager = DriverCacheManager(root_dir=pathlib.Path.cwd())

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_manager=cache_manager).install(), options=options))

    driver.get('https://www.linkedin.com/sales')
    #driver.maximize_window()
    username = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID,'username'))
    )
    username.send_keys('shewchenkoandriy@gmail.com')  # Insert your e-mai
    password = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID,'password'))
    )
    password.send_keys('BinanceZalupa228')  # Insert your password her
    log_in_button = WebDriverWait(driver=driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="btn__primary--large from__button--floating"')))
    
    time.sleep(random.uniform(1.0, 5.0))
    log_in_button.click()
    
    return driver

if __name__ == '__main__':
     
    with open('Ukraine IT CEO 2023-08-19.csv', newline='') as csvfile: 
        reader = list(csv.DictReader(csvfile))

        print(f'len(reader){len(reader)}')

        connect_from_csv(reader, date(2023, 8, 19), 15)





