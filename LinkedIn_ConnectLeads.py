import os
import platform
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.driver_cache import DriverCacheManager
import pathlib 
import random
from TelegramLog import TelegramLog
from ScopedLog import ScopedLog
from LogByLevel import LogByLevel
from ErrorLog import ErrorLog
from telegram import Bot
import asyncio
import asyncpg
import asyncpg.exceptions

async def connect_from_csv(limit, log):
    driver: any
    connection: any
    inputs: any
    async with ScopedLog(log) as driverLog:
        driver = await constructDriver(driverLog)
    
    async with ScopedLog(log) as sqlLog:
        await sqlLog.write('Opening SQL connection', logging.INFO)

        connection = await getConnection()

        await sqlLog.write('Extracting leads', logging.INFO)

        inputs = await connection.fetch("""
            WITH select_architect AS (
            SELECT pp.profile_url, pp.full_name
            FROM architect_linkedin_profiles pp
            LEFT JOIN already_connected_profiles acp
                ON pp.profile_url = acp.profile_url
            LEFT JOIN broken_linkedin_profiles bp
                ON pp.profile_url = bp.profile_url
            LEFT JOIN broken_links bl
                ON pp.profile_url = bl.sales_navigator_profile_url
            WHERE acp.profile_url IS NULL AND bp.profile_url IS NULL AND bl.sales_navigator_profile_url IS NULL
            ORDER BY random()
            LIMIT $1
        ),

        select_ceo AS (
            SELECT pp.profile_url, pp.full_name
            FROM connected_profiles pp
            LEFT JOIN already_connected_profiles acp
                ON pp.profile_url = acp.profile_url
            LEFT JOIN broken_linkedin_profiles bp
                ON pp.profile_url = bp.profile_url
            LEFT JOIN broken_links bl
                ON pp.profile_url = bl.sales_navigator_profile_url
            WHERE acp.profile_url IS NULL AND bp.profile_url IS NULL AND bl.sales_navigator_profile_url IS NULL
            ORDER BY random()
            LIMIT (
                SELECT CASE 
                    WHEN count(*) < $1 THEN 2 * $1 - count(*) 
                    ELSE $1 
                END 
                FROM select_architect
            )
        )

        SELECT * FROM select_ceo
        UNION
        SELECT * FROM select_architect;""", 500)
    
    await log.write('Done', logging.INFO)

    index = 0
    items_connected = 0
    while items_connected < limit and index < len(inputs):
        try:
            async with ScopedLog(log) as scraperLog:
                row = inputs[index]
                current_url = row['profile_url']

                await scraperLog.write(f'Opening URL {current_url}', logging.INFO)

                driver.get(row['profile_url'])
                print(driver.current_url)
    
                await scraperLog.write('Waiting for "More actions" button to appear', logging.DEBUG)

                WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, './/button[@aria-label="More actions"]'))
                )      

                await scraperLog.write('Extracting full name', logging.DEBUG)

                full_name = driver.find_element(By.XPATH, './/h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text.strip()
    
                await scraperLog.write('Checking if already connected', logging.DEBUG)

                if len(driver.find_elements(By.XPATH, '//main//*[contains(@aria-label, "Invite") and contains(@aria-label, "to connect")]')) == 0:
                    await scraperLog.write(f'Inserting into connected profiles table', logging.DEBUG)
                    
                    async with connection.transaction():
                        link = str(row['profile_url'])
                        full_name = str(row['full_name'])
                        # Call stored procedure to insert into "already_connected_profiles" table
                        await connection.execute('INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING', link, full_name)
    
                    await scraperLog.write('Waiting 45 seconds', logging.DEBUG)
                    
                    time.sleep(45)
                    index = index + 1
                    continue
    
                connect_button = None
                try:
                    # Connect
        
                    print('Connect')

                    await scraperLog.write('Searching for "Connect" button', logging.DEBUG)

                    connect_button = WebDriverWait(driver=driver, timeout=10).until(
                        EC.presence_of_element_located((By.XPATH, './/button[contains(@class, "artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action") and contains(., "Connect")]'))
                    )
                except:
                    await scraperLog.write('"Connect" button not found', logging.DEBUG)

                    if ('404' in driver.current_url):
                        await scraperLog.write('Current page is 404', logging.INFO)

                        link = row['profile_url']
    
                        await scraperLog.write('Inserting into broken profiles table', logging.DEBUG)

                        async with connection.transaction():
                            # Call stored procedure to insert into "broken_links" table
                            await connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', link)
    
                        await scraperLog.write('Waiting 45 seconds', logging.DEBUG)

                        time.sleep(45)
                        index = index + 1
                        continue
    
                actions = ActionChains(driver)
                    
                await scraperLog.write('Finding connections_number_span', logging.DEBUG)

                connections_number_span = WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, '//main//span[@class="t-bold"]'))
                )      

                await scraperLog.write('Executing move_to_element(connections_number_span)', logging.DEBUG)

                actions.move_to_element(connections_number_span).perform()
                
                await scraperLog.write('Finding connections_number', logging.DEBUG)

                connections_number = int(connections_number_span.text.strip('+').replace(",",""))
    
                await scraperLog.write(f'connections_number: {connections_number}', logging.DEBUG)
                
                if (connections_number) < 50:
                    await scraperLog.write(f'connections_number too little. skipping', logging.INFO)
                    await scraperLog.write('Inserting into broken profiles table', logging.DEBUG)

                    link = row['profile_url']
                    async with connection.transaction():
                    
                        # Call stored procedure to insert into "broken_links" table
                        await connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', link)
                    await scraperLog.write('Waiting 45 seconds', logging.DEBUG)
                    time.sleep(45)
                    index = index + 1
                    continue
    
                if (connect_button is None):
                    # More -> Connect    
                    await scraperLog.write('Looking for "More" dropdown', logging.DEBUG)

                    print('More -> Connect')
                    # Initialize ActionChains
                    button_more = WebDriverWait(driver=driver, timeout=60).until(
                        EC.presence_of_element_located((By.XPATH, '(.//button[@aria-label="More actions"])[last()]'))
                    )    

                    await scraperLog.write('Executing move_to_element(button_more)', logging.DEBUG)       

                    actions.move_to_element(button_more).perform()

                    await scraperLog.write('Clicking "More"', logging.DEBUG)       
                    
                    actions.click(button_more).perform()

                    await scraperLog.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)

                    time.sleep(random.uniform(5.0, 10.0))

                    await scraperLog.write('Looking for "Connect" button', logging.DEBUG)       

                    connect_button = WebDriverWait(driver=driver, timeout=60).until(
                        EC.presence_of_element_located((By.XPATH, '(.//div[@class="artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view full-width display-flex align-items-center"]/*[contains(text(), "Connect")]/..)[last()]'))
                    ) 
                await scraperLog.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)

                time.sleep(random.uniform(5.0, 10.0))
            
                await scraperLog.write('Clicking "Connect"', logging.DEBUG)       
                
                actions.move_to_element(connect_button)
                actions.click(connect_button).perform()
    
                await scraperLog.write('Checking if lead\'s email required', logging.DEBUG)       

                if len(driver.find_elements(By.XPATH, '//*[text()[contains(., "To verify this member knows you, please enter their email to connect. You can also include a personal note.")]]')) > 0:
                    await scraperLog.write('"To verify this member knows you, please enter their email to connect. You can also include a personal note."', logging.INFO)       
                    await scraperLog.write('Inserting into broken profiles table', logging.DEBUG)

                    link = row['profile_url']
                    async with connection.transaction():
                            # Call stored procedure to insert into "broken_links" table
                        await connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', link)
                    await log.write('Waiting 45 seconds', logging.DEBUG)
                    time.sleep(45)
                    index = index + 1
                    continue
                
                await scraperLog.write('Looking for "Submit" button', logging.DEBUG)
    
                submit_button = WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, './/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1"]'))
                )

                await scraperLog.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)

                time.sleep(random.uniform(5.0, 10.0))

                await scraperLog.write('Clicking for "Submit" button', logging.DEBUG)

                submit_button.click()

                await scraperLog.write(f'Connected {full_name}', logging.INFO)

                await scraperLog.write('Inserting into connected profiles table', logging.DEBUG)

                async with connection.transaction():
                    link = str(row['profile_url'])
                    full_name = str(row['full_name'])
                    # Call stored procedure to insert into "already_connected_profiles" table
                    await connection.execute('INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING', link, full_name)
    
                items_connected = items_connected + 1
                index = index + 1
            
        except Exception as error:
            await log.write(f'Uknown error.\n\n{ErrorLog(error)}', logging.ERROR)
            index = index + 1
        finally:
            await log.write(f'Waiting 45 seconds', logging.DEBUG)
            time.sleep(45)
            
    driver.quit()
    connection.close()

async def getConnection():
    return await asyncpg.connect(
        host='159.89.13.130',
        port=5432,
        database='ukraine_it_ceo',
        user='Administrator',
        password='lUwm8vS21jLW'
    )

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

        if 'DOCKER' in os.environ or 'container' in os.environ:
            await log.write('Running from Docker', logging.INFO)

        options.add_argument("start-maximized")
        options.binary_location = '/usr/bin/google-chrome'

        path = ChromeDriverManager().install().replace('THIRD_PARTY_NOTICES.', '')

        await log.write(f'Installed chrome web driver to: {path}', logging.DEBUG)

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
        except Exception as error:
            await log.write(f'Login error: \n\n{ErrorLog(error)}', logging.ERROR)
            if attempts == 3:
                driver.quit()
                raise error

async def main():
    log = LogByLevel(TelegramLog(Bot(token='7209921522:AAHRhEH11Clg_qBPY9SSwfEJDoPvJ5yso70'), '-1002300475780', 'ConnectLeads'), logging.DEBUG)  
    await log.write('Starting function ConnectLeads', logging.INFO)
    await connect_from_csv(150, log)
    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())