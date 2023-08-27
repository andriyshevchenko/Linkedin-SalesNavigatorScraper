from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv
from tkinter import Tk
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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
import argparse

def connect_from_csv(input_file, startDate: date, skipLeadsPerWeekNumber: int, production: bool):
    driver = constructDriver(True)
    print(f'number of rows = {len(input_file)}')
    skip = math.floor((date.today() - startDate).days / 7) * skipLeadsPerWeekNumber
    print(f'skipping {skip} items')
    print(f'remaining number of lines: {len(input_file[skip:skip+skipLeadsPerWeekNumber])}')
    for row in input_file[skip:skip+skipLeadsPerWeekNumber]:
        driver.get(row['ProfileUrl'])
        connect_button = None
        try:
            # Connect
            print('Connect')
            connect_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, './/button[contains(@class, "artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action") and contains(., "Connect")]'))
            )
        except:
           pass

        if (connect_button is None):
            # More -> Connect    
            print('More -> Connect')
            # Initialize ActionChains
            actions = ActionChains(driver)
            button_more = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '(.//button[@aria-label="More actions"])[last()]'))
            )           
            # Right-click or hover over the trigger element to reveal the context menu
            actions.move_to_element(button_more).perform()
            actions.click(button_more).perform()
            time.sleep(random.uniform(5.0, 10.0))
            
            connect_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '(.//div[@class="artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view full-width display-flex align-items-center"]/*[contains(text(), "Connect")]/..)[last()]'))
            ) 

        time.sleep(random.uniform(5.0, 10.0))
        actions.move_to_element(connect_button)
        actions.click(connect_button).perform()
        submit_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, './/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1"]'))
        )
        time.sleep(random.uniform(5.0, 10.0))
        submit_button.click()
        full_name = driver.find_element(By.XPATH, './/h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text.strip()
        print(f'Connected {full_name}')
        time.sleep(random.uniform(5.0, 10.0))
        
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
    options.add_argument("--disable-gpu")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    cache_manager = DriverCacheManager(root_dir=pathlib.Path.cwd())

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_manager=cache_manager).install(), options=options))

    attempts = 0
    while True:
        try:
            attempts += 1
            if attempts == 1:
                driver.get('https://www.linkedin.com/sales')
            else:
                driver.refresh()

            driver.maximize_window()

            time.sleep(random.uniform(5.0, 10.0))
            
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

            time.sleep(random.uniform(5.0, 10.0))
            log_in_button.click()

            return driver
        except Exception as error:
            if attempts == 3:
                driver.quit()
                raise error

if __name__ == '__main__':
    with open('Ukraine IT CEO 2023-08-19.csv', newline='') as csvfile: 
        reader = list(csv.DictReader(csvfile))

        print(f'len(reader){len(reader)}')

        connect_from_csv(reader, date(2023, 8, 27), 100, True)





