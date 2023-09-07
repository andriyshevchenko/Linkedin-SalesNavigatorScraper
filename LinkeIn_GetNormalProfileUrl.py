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
import pathlib 
import random
import os
import argparse
from datetime import date
import gc

def scrap_from_csv(input_file, index: int):
    driver = constructDriver(True)
    print('scrap_from_csv')
    start_date = date.today()
    print(f'index = {index}')
    path = 'Ukraine IT CEO 2023-09-03.csv'
    with open(path, 'w', encoding='utf8', newline='') as output_file:
        print('opened file')
        writer = csv.DictWriter(output_file, delimiter=',', fieldnames=['ProfileUrl'])
        writer.writeheader()
        print(f'number of rows = {len(input_file)}')
        print(f'type = {type(input_file)}')
        for row in input_file[3716:]:
            try:
                if (date.today() - start_date).days > 0:
                    start_date = date.today()
                    gc.collect()

                WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, './/section[@id="profile-card-section"]'))
                )

                try:
                    driver.get(row['ProfileUrl'])

                    hidden_profile = driver.find_elements(By.XPATH, '//*[text()[contains(., "LinkedIn Member") or contains(., "Unlock full profile")]]')
                    if hidden_profile is not None:
                        print('Hidden profile')
                        continue
                except:
                    pass

                ellipsis = WebDriverWait(driver=driver, timeout=60).until(
                    EC.element_to_be_clickable((By.XPATH, './/button[@class="ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n"]'))
                )     

                time.sleep(random.uniform(5.0, 10.0))
                ellipsis.click()

                WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, './/div[@class="_container_x5gf48 _visible_x5gf48 _container_iq15dg _raised_1aegh9"]'))
                )       
                menuItems = driver.find_elements(By.XPATH, './/div[@class="_container_x5gf48 _visible_x5gf48 _container_iq15dg _raised_1aegh9"]//descendant::li')
                copyLinkedInUrl = list(filter(lambda item: item.find_element(By.XPATH, './/div[@class="_text_1xnv7i"]').text.strip() == 'Copy LinkedIn.com URL', menuItems))

                if len(copyLinkedInUrl) == 1:
                    copyButton = copyLinkedInUrl[0].find_element(By.XPATH, './/button[@class="ember-view _item_1xnv7i"]')
                    WebDriverWait(driver=driver, timeout=60).until(
                        EC.element_to_be_clickable(copyButton)
                    )
                    time.sleep(random.uniform(5.0, 10.0))
                    copyButton.click()
                    linkedin_url = Tk().clipboard_get().strip()
                    print(linkedin_url)
                    writer.writerow({ 'ProfileUrl': linkedin_url })
                    output_file.flush()
                
                print('Waiting...')
                time.sleep(45)
            except Exception as error:
                print(error)
                time.sleep(60*30)

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
    username = WebDriverWait(driver=driver, timeout=60).until(
        EC.presence_of_element_located((By.ID,'username'))
    )
    username.send_keys('shewchenkoandriy@gmail.com')  # Insert your e-mai
    password = WebDriverWait(driver=driver, timeout=60).until(
        EC.presence_of_element_located((By.ID,'password'))
    )
    password.send_keys('BinanceZalupa228')  # Insert your password her
    log_in_button = WebDriverWait(driver=driver, timeout=60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="btn__primary--large from__button--floating"')))
    
    time.sleep(random.uniform(5.0, 10.0))
    log_in_button.click()
    
    return driver

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profiles', default=None)
    args = parser.parse_args()
    number_jobs = 1
     
    with open('links 2023-08-22.csv', newline='') as csvfile: 
        reader = list(csv.DictReader(csvfile))
        chunks = np.array_split(reader, number_jobs)

        print(f'type(chunks){type(chunks)}')
        print(f'len(chunks){len(chunks)}')
        print(f'type(chunks[0]){type(chunks[0])}')
        print(f'len(chunks[0]){len(chunks[0])}')

        futures = []
         # scrape and crawl
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for number in range(number_jobs):
                futures.append(
                   executor.submit(scrap_from_csv, chunks[number], number))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())






