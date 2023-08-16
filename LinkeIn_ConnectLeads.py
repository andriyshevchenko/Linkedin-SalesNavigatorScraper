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
import concurrent.futures
from webdriver_manager.core.driver_cache import DriverCacheManager
import numpy as np
import math
import pathlib 
import os

def connect_from_csv(input_file):
    time.sleep(index)
    driver = constructDriver(True)
    print('scrap_from_csv')
    print(f'index = {index}')
    file_exists = os.path.exists(f'normalLinks{str(index+1)}.csv')
    file_length = 0
    with open(f'normalLinks{str(index+1)}.csv',  newline='') as output_file:
        file_length = len(list(csv.DictReader(output_file)))

    with open(f'normalLinks{str(index+1)}.csv', 'a', encoding='utf8', newline='') as output_file:
        print('opened file')
        writer = csv.DictWriter(output_file, delimiter=',', fieldnames=['ProfileUrl'])
        if not file_exists:
            writer.writeheader()
        print(f'number of rows = {len(input_file)}')
        print(f'type = {type(input_file)}')
        skip = file_length
        print(f'skipping {skip} items')
        print(f'remaining number of lines: {len(input_file[file_length::])}')
        input()
        for row in input_file[skip::]:
            attempts = 0
            try:
                attempts += 1
                driver.get(row['ProfileUrl'])
                ellipsis = WebDriverWait(driver=driver, timeout=10).until(
                    EC.element_to_be_clickable((By.XPATH, './/button[@class="ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n"]'))
                )       

                ellipsis.click()
                time.sleep(1)

                WebDriverWait(driver=driver, timeout=10).until(
                    EC.presence_of_element_located((By.XPATH, './/div[@class="_container_x5gf48 _visible_x5gf48 _container_iq15dg _raised_1aegh9"]'))
                )       
                menuItems = driver.find_elements(By.XPATH, './/div[@class="_container_x5gf48 _visible_x5gf48 _container_iq15dg _raised_1aegh9"]//descendant::li')
                copyLinkedInUrl = list(filter(lambda item: item.find_element(By.XPATH, './/div[@class="_text_1xnv7i"]').text.strip() == 'Copy LinkedIn.com URL', menuItems))

                if len(copyLinkedInUrl) == 1:
                    copyButton = copyLinkedInUrl[0].find_element(By.XPATH, './/button[@class="ember-view _item_1xnv7i"]')
                    WebDriverWait(driver=driver, timeout=10).until(
                        EC.element_to_be_clickable(copyButton)
                    )
                    copyButton.click()
                    linkedin_url = Tk().clipboard_get().strip()
                    print(linkedin_url)
                    writer.writerow({ 'ProfileUrl': linkedin_url })
                    output_file.flush()
            except Exception as error:
                if attempts == 10:
                    driver = constructDriver(True)
                if attempts > 10:
                    driver.quit()
                    raise error
                else:
                    print(error)
                    time.sleep(5)

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
    
    time.sleep(1)
    log_in_button.click()
    
    return driver


def connect_leads(event, context):
     
    with open('normalLinks.csv', newline='') as csvfile: 
        reader = list(csv.DictReader(csvfile))

        print(f'type(reader){type(reader)}')
        print(f'len(reader){len(reader)}')

        connect_from_csv(reader)





