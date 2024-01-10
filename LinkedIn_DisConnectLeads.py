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
from TelegramLog import TelegramLog
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
    buttons = driver.find_elements(By.XPATH, '(.//span[contains(.,"weeks")])/following::button[@class="artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view invitation-card__action-btn"][1]')
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
    log = TelegramLog(Bot(token='6464053578:AAGbooTDuVCdiYqMhN2akhMMEJI0wVZSr7k'), '-1001801037236', 'DisconnectLeads')  
    await log.write('Function started')
    driver = constructDriver(True)
    await log.write('Successfully started scraper')
    driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')
    time.sleep(random.uniform(5.0, 10.0))
    perform_scroll_to_bottom(driver)
    WebDriverWait(driver=driver, timeout=60).until(
        EC.presence_of_element_located((By.XPATH,'.//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]'))
    )
    number_pages = len(list(driver.find_elements(By.XPATH, './/ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]/descendant::li')))
    pages = list(map(lambda number: f'https://www.linkedin.com/mynetwork/invitation-manager/sent?page={number}', range(1, number_pages+1)))
    await log.write(f'There are {number_pages} pages. Withdrawing requests...')
    for page in pages:
        driver.get(page)
        time.sleep(random.uniform(5.0, 10.0))
        try:
            await withdraw_connections(driver, log)
        except Exception as error:
            await log.write(f'Problem encontered: {error}')
    await log.write('Function quit')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())