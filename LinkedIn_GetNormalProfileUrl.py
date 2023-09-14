from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import math
import csv
from tkinter import Tk
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.driver_cache import DriverCacheManager
import pathlib 
import random
from datetime import date, datetime
import gc
from telegram import Bot
import asyncio
from TelegramLog import TelegramLog
import json
import traceback

async def scrap_from_csv(input_file, log):
    input = list(map(lambda row: row['ProfileUrl'], input_file))
    driver = constructDriver(True)
    print('scrap_from_csv')
    start_time = datetime.now()
    path = f'Ukraine IT CEO {date.today()}.csv'
    with open(path, 'w', encoding='utf8', newline='') as output_file, open('LinkedIn_GetNormalProfileUrl.json', 'r+') as config_file:
        config = json.load(config_file)
        current_lead = config['CURRENT_LEAD']
        if len(current_lead) == 0:
            current_lead_index = 0
        else:
            current_lead_index = input.index(current_lead) + 1
        await log.write(f'There are {current_lead_index} processed profiles. Continue')
        writer = csv.DictWriter(output_file, delimiter=',', fieldnames=['ProfileUrl', 'FullName'])
        writer.writeheader()
        print(f'number of rows = {len(input)}')
        index = current_lead_index
        while index < len(input):
            try:
                row = input[index]
                link = row

                if math.floor((datetime.now() - start_time).total_seconds() / 3600) == 2:
                    await log.write('Free memory: start')
                    gc.collect()
                    await log.write('Free memory: done')
                    start_time = datetime.now()
            
                driver.get(link)

                WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, './/section[@id="profile-card-section"]'))
                )

                full_name = driver.find_element(By.XPATH, './/section[@id="profile-card-section"]/descendant::h1[@data-anonymize]').text.strip()
              
                hidden_profile = driver.find_elements(By.XPATH, '//*[text()[contains(., "LinkedIn Member") or contains(., "Unlock full profile")]]')
                    
                if hidden_profile is not None and len(hidden_profile) > 0:
                    await log.write(f'Hidden profile {link}. Skipping')
                    index = index + 1
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

            except (ConnectionError, WebDriverException) as error:
                print(error)
                message = traceback.format_exception(error)
                if "net::ERR_CONNECTION_TIMED_OUT" in message:
                    time.sleep(60*30)
                    await log.write('Connection error. Retrying in 30 minutes.')
                else:
                    await log.write(f'Broken link:\n{link}\nDebugging information:\n__{message}__')
                    index = index + 1
            except Exception as error:
                print(error)
                await log.write(f'Uknown error.\n\nLink{link}\nDebugging information:\n__{message}__')
                index = index + 1
            finally:
                if (index == 1):
                    await log.write('Successfully started scraper')
                config_file.truncate(0)
                config['CURRENT_LEAD'] = link
                json.dump(config, config_file, indent=4)
                config_file.flush()
                print('Waiting...')
                time.sleep(30)   

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
    driver.switch_to.window(driver.current_window_handle)
    return driver

async def main():
    log = TelegramLog(Bot(token='6464053578:AAGbooTDuVCdiYqMhN2akhMMEJI0wVZSr7k'), '-1001801037236', 'GetNormalProfileUrl')  
    await log.write('Function started')
        
    with open('links.csv', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        await scrap_from_csv(reader, log)
    await log.write('Function quit')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())


