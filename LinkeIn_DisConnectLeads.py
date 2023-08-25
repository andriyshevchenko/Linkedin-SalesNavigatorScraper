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
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.core.driver_cache import DriverCacheManager
import numpy as np
import math
import pathlib 
import os
from datetime import date
import random
import argparse

def withdraw_connections(production: bool):
    driver = constructDriver(True)
    driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')
    time.sleep(random.uniform(5.0, 10.0))
    height: int = 0
    while height < driver.execute_script("return document.body.scrollHeight"):
        height += 20
        driver.execute_script("window.scrollTo(0, {});".format(height))
        time.sleep(0.0125)
    time.sleep(random.uniform(5.0, 10.0))
    buttons = driver.find_elements(By.XPATH, '(.//span[contains(.,"2 weeks")])/following::button[@class="artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view invitation-card__action-btn"][1]')
    for button in buttons:
        if (production):
            action = ActionChains(driver)
            # perform the operation
            action.move_to_element(button).click().perform()
            time.sleep(random.uniform(2.0, 5.0))
            submit_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.element_to_be_clickable((By.XPATH, './/button[@class="artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view"]')))
            submit_button.click()
            time.sleep(random.uniform(2.0, 5.0))
        else:
            print('Skipping')

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
    withdraw_connections(True)





