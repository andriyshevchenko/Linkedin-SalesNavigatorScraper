import logging
import os
import platform
import stat
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.core.driver_cache import DriverCacheManager
import pathlib 
import random
from ErrorLog import ErrorLog
from LogByLevel import LogByLevel
from TelegramLog import TelegramLog, NullLog
from telegram import Bot
import asyncio

def perform_scroll_to_bottom(driver):
    height: int = 0
    while height < driver.execute_script("return document.body.scrollHeight"):
        height += 20
        driver.execute_script("window.scrollTo(0, {});".format(height))
        time.sleep(0.0125)

async def withdraw_connections(driver, logger):
    perform_scroll_to_bottom(driver)
    time.sleep(random.uniform(5.0, 10.0))
    buttons = driver.find_elements(By.XPATH, '(.//span[contains(.,"weeks") or contains(.,"month") or contains(.,"months")])/following::button[@class="artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view invitation-card__action-btn"][1]')
    for button in buttons:
        action = ActionChains(driver)
        # perform the operation
        action.move_to_element(button).click().perform()
        time.sleep(random.uniform(5.0, 10.0))
        submit_button = WebDriverWait(driver=driver, timeout=60).until(
            EC.element_to_be_clickable((By.XPATH, './/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view artdeco-modal__confirm-dialog-btn"]')))
        submit_button.click()
        time.sleep(random.uniform(5.0, 10.0))
    await logger.write(f'Withdrawn {len(buttons)} requests')

async def constructDriver(log):
    await log.write('Creating a driver', logging.DEBUG)

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    options.add_argument("--headless=new")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})

    driver: any

    if platform.system() == "Windows":
        await log.write('Running on Windows', logging.INFO)

        options.add_argument("--window-size=1280,700")
        
        cache_manager = DriverCacheManager(root_dir=pathlib.Path.cwd())
        chrome_install = ChromeDriverManager(cache_manager=cache_manager).install()

        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")

        driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path, options=options))
    else:
        await log.write('Running on Linux', logging.INFO)

        if 'DOCKER' in os.environ:
            await log.write('Running from Docker', logging.INFO)

        options.add_argument("start-maximized")
        options.binary_location = '/usr/bin/google-chrome'

        path = ChromeDriverManager().install().replace('THIRD_PARTY_NOTICES.', '')
        
        await log.write(f'Installed chrome web driver to: {path}', logging.DEBUG)
        
        await log.write(f'Setting permission', logging.DEBUG)
        
        # Set the file to be executable by the owner, group, and others
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |  # Owner
                       stat.S_IRGRP | stat.S_IXGRP |               # Group
                       stat.S_IROTH | stat.S_IXOTH)                # Others

        service = Service(path)

        await log.write('Starting Chrome', logging.DEBUG)

        driver = webdriver.Chrome(service=service, options=options)
    
    await log.write('Driver installed', logging.DEBUG)

    attempts = 0
    while attempts < 3:
        try:
            await log.write('Logging user in', logging.INFO)

            attempts += 1
            if attempts == 1:
                driver.get('https://www.linkedin.com/sales')
            else:
                driver.refresh()

            driver.maximize_window()

            await log.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)

            time.sleep(random.uniform(5.0, 10.0))
            
            await log.write('Typing email and password', logging.DEBUG)
            
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

            await log.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)

            time.sleep(random.uniform(5.0, 10.0))

            await log.write('Pressing login button', logging.DEBUG)

            log_in_button.click()

            await log.write(f'Waiting 60 seconds', logging.DEBUG)

            time.sleep(60)
            driver.switch_to.window(driver.current_window_handle)
            return driver
        except asyncio.CancelledError:
            await log.write('Job was cancelled', logging.WARNING)
            driver.quit()
            break
        except Exception as error:
            await log.write(f'Login error: \n\n{ErrorLog(error)}', logging.ERROR)
            if attempts == 3:
                driver.quit()
                raise error

async def main():
    log = LogByLevel(TelegramLog(Bot(token='7209921522:AAHRhEH11Clg_qBPY9SSwfEJDoPvJ5yso70'), '-1002300475780', 'DisonnectLeads'), logging.DEBUG)  
    driver = await constructDriver(log)
    await log.write('Successfully started function', logging.DEBUG)
    driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')
    time.sleep(random.uniform(5.0, 10.0))
    perform_scroll_to_bottom(driver)
    pages = ['https://www.linkedin.com/mynetwork/invitation-manager/sent?page=1']
    number_pages = 1
    try:
        WebDriverWait(driver=driver, timeout=60).until(
            EC.presence_of_element_located((By.XPATH,'.//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]'))
        )
        number_pages = len(list(driver.find_elements(By.XPATH, './/ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]/descendant::li')))
        pages = list(map(lambda number: f'https://www.linkedin.com/mynetwork/invitation-manager/sent?page={number}', range(1, number_pages+1)))
    except:
        pass
    await log.write(f'There are {number_pages} pages. Withdrawing requests...', logging.DEBUG)
    for page in pages:
        driver.get(page)
        time.sleep(random.uniform(5.0, 10.0))
        try:
            await withdraw_connections(driver, log)
        except Exception as error:
            await log.write(f'Problem encontered: {error}', logging.DEBUG)
    await log.write('Function quit', logging.DEBUG)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())