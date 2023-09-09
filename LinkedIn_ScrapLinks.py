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
from selenium.webdriver.chrome.options import Options
import os.path

def saveLeads(driver):
    select_all = driver.find_element(By.XPATH, './/div[@class="flex align-items-center ph3 full-width"]//descendant::input')
    driver.execute_script("arguments[0].click();", select_all)
    save = driver.find_element(By.XPATH, './/button[@class="ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _emphasized_ps32ck _left_ps32ck _container_iq15dg ml2 mr-2 inline-flex justify-center align-items-center mt-1 mb-1 _bulk-action-control_1igybl"]')
    save.click()
    
def scrap_from_url(driver,url=None):
    fieldnames = ['ProfileUrl']
    file_exists = os.path.isfile('links.csv')    
    with open('links.csv', 'a', encoding='utf8', newline='') as output_file:
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
                container = driver.find_element(By.XPATH, './/div[@class="p4 _vertical-scroll-results_1igybl"]')
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
                time.sleep(1)
                
                saveLeads(driver)

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
    options.headless = headless
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("start-maximized")
    chrome_options = webdriver.ChromeOptions()

    if headless:        
        chrome_options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), chrome_options=chrome_options), options=options)
    return driver

if __name__ == '__main__':
    
    driver = constructDriver()
    time.sleep(5)
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
    
    time.sleep(1)

    scrap_from_url(driver, 'https://www.linkedin.com/sales/search/people?savedSearchId=50603298&page={}')







