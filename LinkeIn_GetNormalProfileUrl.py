from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import math
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
from datetime import date, datetime
import gc
from telegram import Bot
import asyncio

class TelegramLog:
    def __init__(self, bot, chat_id, _function):
        self.bot = bot
        self.chat_id = chat_id
        self._function = _function

    def write(self, text):
        print(self.chat_id)
        # Replace 'YOUR_CHAT_ID' with your actual chat ID
        asyncio.run(self.bot.send_message(self.chat_id, f'Function: {self._function}, Timestamp: {datetime.now()}: {text}'))

def scrap_from_csv(input_file, log):
    driver = constructDriver(True)
    print('scrap_from_csv')
    start_date = date.today()
    start_time = datetime.now()
    path = 'Ukraine IT CEO 2023-09-08.csv'
    with open(path, 'w', encoding='utf8', newline='') as output_file:
        writer = csv.DictWriter(output_file, delimiter=',', fieldnames=['ProfileUrl', 'FullName'])
        writer.writeheader()
        print(f'number of rows = {len(input_file)}')
        index = 917
        while index < len(input_file):
            try:
                row = input_file[index]
                if (date.today() - start_date).days > 0:
                    start_date = date.today()
                    log.write('Free memory')
                    gc.collect()
                
                if math.floor((datetime.now() - start_time).total_seconds() / 3600) == 1:
                    log.write(f'Processed {index} profiles')
                    start_time = datetime.now()

                driver.get(row['ProfileUrl'])

                WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, './/section[@id="profile-card-section"]'))
                )

                full_name = driver.find_element(By.XPATH, './/section[@id="profile-card-section"]/descendant::h1[@data-anonymize]').text.strip()
              
                hidden_profile = driver.find_elements(By.XPATH, '//*[text()[contains(., "LinkedIn Member") or contains(., "Unlock full profile")]]')
                    
                if hidden_profile is not None and len(hidden_profile) > 0:
                    log.write(f'Hidden profile {row}')
                    continue
              
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
                    writer.writerow({ 'ProfileUrl': linkedin_url, 'FullName': full_name })
                    output_file.flush()
                
                index = index + 1
            except ConnectionError as error:
                print(error)
                log.write('Connection error. Retrying in 30 minutes.')
                time.sleep(60*30)
            except Exception as error:
                print(error)
                log.write(f'Broken link {row}')
                index = index + 1
            finally:
                print('Waiting...')
                time.sleep(45)   

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
    time.sleep(60)
    return driver

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profiles', default=None)
    args = parser.parse_args()
    number_jobs = 1
    log = TelegramLog(Bot(token='6464053578:AAGbooTDuVCdiYqMhN2akhMMEJI0wVZSr7k'), '-1001801037236', 'GetNormalProfileUrl')  
    log.write('Function started')
    with open('links 2023-08-22.csv', newline='') as csvfile: 
        reader = list(csv.DictReader(csvfile))
        chunks = np.array_split(reader, number_jobs)

        futures = []
         # scrape and crawl
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for number in range(number_jobs):
                futures.append(
                   executor.submit(scrap_from_csv, chunks[number], log))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())





