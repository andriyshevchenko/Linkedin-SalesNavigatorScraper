from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import os
import openpyxl
from tkinter import Tk
import argparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def scrap_from_url(args, driver,url=None, load_page=True):
    if url == None:
        url = 'https://www.linkedin.com/sales/search/people?savedSearchId=50603306&page={}'

    time.sleep(3)
#################################### INSERT URL ####################################

    number_page = 1
    while number_page <= 100:
        try:
            driver.get(url.format(number_page))
            time.sleep(5)
            height = 0
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            while height < driver.execute_script("return document.body.scrollHeight"):
                driver.execute_script("window.scrollTo(0, {});".format(height))
                height += 20
            time.sleep(3)

            select_all = driver.find_element(By.XPATH, './/div[@class="flex align-items-center ph3 full-width"]//descendant::input')
            driver.execute_script("arguments[0].click();", select_all)
            unsave = driver.find_element(By.XPATH, './/button[@class="ml2 mv-2 font-weight-400 pt2 pb2 artdeco-button artdeco-button--1 artdeco-button--tertiary ember-view"]')
            unsave.click()
            _continue = driver.find_element(By.XPATH, './/button[@class="artdeco-button artdeco-button--2 artdeco-button--pro artdeco-button--primary ember-view delete-button ml2 float-right"]')
            _continue.click()
        
            number_page += 1
        except:
            number_page = 1
       
        # next_button = driver.find_element_by_class_name("search-results__pagination-next-button")
        # next_button.click()
        # print(links)
        # print(len(links))

####################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_words', default=None)
    parser.add_argument('--url', default=None)
    parser.add_argument('--mode', default='url')
    args = parser.parse_args()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.linkedin.com')
    driver.maximize_window()
    time.sleep(10)
    username = driver.find_element(By.ID,'session_key')
    username.send_keys('shewchenkoandriy@gmail.com')  # Insert your e-mail

    password = driver.find_element(By.ID,'session_password')
    password.send_keys('BinanceZalupa228')  # Insert your password here

    log_in_button = driver.find_element(By.CLASS_NAME,"sign-in-form__submit-btn--full-width")
    log_in_button.click()
    time.sleep(1)
    try:
        confirm_button = driver.find_element(By.ID,'remember-me-prompt__form-secondary')
        confirm_button.click()
    except:
        pass
    print('Submit')
    time.sleep(10)
    

    print(args)
    if args.mode == 'url':
        scrap_from_url(args, driver, args.url)
    else:
        print('MODE wrongly specified!!!')







