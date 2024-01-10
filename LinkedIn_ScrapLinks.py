from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import math
from tkinter import Tk
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.driver_cache import DriverCacheManager
import pathlib 
import random
from datetime import datetime
import gc
from telegram import Bot
import asyncio
from TelegramLog import TelegramLog
import traceback
import asyncpg
import asyncpg.exceptions
import csv
import os
    
def scrap_from_url(driver,url=None):
    fieldnames = ['ProfileUrl']
    file_exists = os.path.isfile('architect.csv')    
    with open('architect.csv', 'a', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=fieldnames)

        if not file_exists:
            fc.writeheader()

        number_page = 1
        remaining_results = ''
        while number_page <= 100:
            try:
                driver.get(url.format(number_page))
                time.sleep(5)
                height = 0
                remaining_results = driver.find_element(By.XPATH, './/div[@class="t-14 flex align-items-center mlA pl3"]/span').text.strip().split(' ')[0]
                container = driver.find_element(By.XPATH, './/div[@class="_vertical-scroll-results_1od37d"]')
                while height < driver.execute_script("return arguments[0].scrollHeight", container):
                    height += 20
                    driver.execute_script("arguments[0].scrollTo(0, {});".format(height), container)
                    time.sleep(0.0125)

                page_links = list(map(
                    lambda a: { 'ProfileUrl': a.get_attribute('href') },
                    driver.find_elements(By.XPATH, './/div[@class="artdeco-entity-lockup__image artdeco-entity-lockup__image--type-circle ember-view"]/a')))
                fc.writerows(page_links)
                output_file.flush()
                print(page_links)
                time.sleep(45)

                if number_page == 100:
                    number_page = 1
                else:
                    number_page += 1
            except Exception as error:
                print("An exception occurred:", error)
                if number_page == 1 or remaining_results == '0':
                    print('Scraping finished')
                    break
                else:
                    number_page = 1
                
            # next_button = driver.find_element_by_class_name("search-results__pagination-next-button")
            # next_button.click()
            # print(links)
            # print(len(links))

        # df = pd.DataFrame(np.array(tab))
        # df.to_excel(r'{}/Linkedin_Scrap.xlsx'.format(path), index=False, header=True)

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
    driver.switch_to.window(driver.current_window_handle)
    return driver

if __name__ == '__main__':
    
    driver = constructDriver()

    scrap_from_url(driver, 'https://www.linkedin.com/sales/search/people?coach=false&savedSearchId=1744382205&page={}')







