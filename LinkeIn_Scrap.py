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
    
def scrap_from_csv(driver):
    extracted_infos = []
    count=0
    for link in links:
        count += 1
        # if count > 1:
        #     break
        driver.get(link)
        time.sleep(1)
        person_profile = {}
        ## Implement BeautifulSoup for html parser## TODO
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')

        # get full name
        full_name = soup.title.text.split('|')[0]

        # company url
        companies = ','.join(
            list(
                map(
                    driver.find_element(By.XPATH, './/ul[@class="_positions-list_q5pnp1"]/descendant::a[@class="ember-view _company-icon_p4eb22"]'),
                    lambda a: a.get_attribute('href')
            )))

        # linkedin profile url
        try:
            trip = driver.find_element(By.CSS_SELECTOR,
                "button[class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n']")
            trip.click()
            cop_button = driver.find_element(By.CSS_SELECTOR,"div[data-control-name='copy_linkedin']")
            time.sleep(1)
            cop_button.click()
            time.sleep(1)
            linkedin_url = Tk().clipboard_get()
        except:
            linkedin_url = ''

        # profile description
        try:
            profile_summary = driver.find_element(By.XPATH, './/div[@class="_bodyText_1e5nen _default_1i6ulk"]').text.strip()
        except:
            profile_summary = ''


        ##---------------------------------------##
        number_candidate += 1
        print("{} /".format(number_candidate) + " {}".format(len(links)))
        person_profile['NAME'] = full_name
        person_profile['COMPANIES'] = companies
        person_profile['LINKEDIN WEBPAGE'] = linkedin_url
        person_profile['DESCRIPTION'] = profile_summary
        extracted_infos.append(person_profile)
        time.sleep(3)

    with open('results.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=extracted_infos[0].keys())
        fc.writeheader()
        fc.writerows(extracted_infos)
    # df = pd.DataFrame(np.array(tab))
    # df.to_excel(r'{}/Linkedin_Scrap.xlsx'.format(path), index=False, header=True)
    print('DONE')
    return extracted_infos
def scrap_from_keywords(args, driver,keywords=None):
    # filter_page_url = 'https://www.linkedin.com/sales/search/people?page=1&rsLogId=969614316&searchSessionId=1qpyQattToCh2lFvET1Cwg%3D%3D'
    filter_page_url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=12&geoIncluded=103644278&logHistory=true&page=1&rsLogId=994102108&searchSessionId=1qpyQattToCh2lFvET1Cwg%3D%3D&seniorityIncluded=6%2C8%2C7'
    # print(filter_page_url)
    driver.get(filter_page_url)
    time.sleep(3)

    kwd_input = driver.find_element(By.ID,'ember44-input')
    kwd_input.send_keys(keywords)
    kwd_input.send_keys(Keys.ENTER)
    time.sleep(1)
    profiles = scrap_from_url(args, driver, url=driver.current_url, load_page=False)
    return profiles
def scrap_from_company_list(args, driver, fpath=''):
    company_list = read_company_list(fpath)
    rets = []
    for company in company_list:
        profiles = scrap_from_keywords(args, driver,keywords=company)
        rets.extend(profiles)
    with open('all_company.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=rets[0].keys())
        fc.writeheader()
        fc.writerows(rets)
    return rets
def read_company_list(fpath):
    with open(fpath) as f:
        lines = f.readlines()
    f.close()
    lines = [line.strip() for line in lines]
    return lines


####################################################################################

if __name__ == '__main__':

    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
    
    time.sleep(1)
   
    scrap_from_csv(driver)






