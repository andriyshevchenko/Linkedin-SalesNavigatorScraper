from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.driver_cache import DriverCacheManager
import pathlib 
import random
from TelegramLog import TelegramLog, NullLog
from telegram import Bot
import asyncio
import traceback
import asyncpg
import asyncpg.exceptions

invite_message_template = """Hello,
I hope this message finds you in good spirits.
I'm interested in connecting with professionals like yourself to broaden my network and gain insights into industry trends.

Best regards,
Andriy Shevchenko"""

async def connect_from_csv(limit, log):
    driver = constructDriver(True)
    connection = await getConnection()
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

    await log.write('Successfully started scraper')
    await log.write(f'remaining number of lines: {len(inputs)}')
    index = 0
    items_connected = 0
    while items_connected < limit and index < len(inputs):
        row = inputs[index]

        await log.write(f'Leads processed: {index}')
        
        await log.write(f'-- Making a web request --')

        driver.get(row['profile_url'])
        print(driver.current_url)

        await log.write(f'-- Waiting for page to load --')
       
        WebDriverWait(driver=driver, timeout=60).until(
            EC.presence_of_element_located((By.XPATH, '//main'))
        )     

        WebDriverWait(driver=driver, timeout=60).until(
            EC.presence_of_element_located((By.XPATH, './/button[@aria-label="More actions"]'))
        )           
        full_name = driver.find_element(By.XPATH, './/h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text.strip()

        if len(driver.find_elements(By.XPATH, '//main//*[contains(@aria-label, "Invite") and contains(@aria-label, "to connect")]')) == 0:
            
            async with connection.transaction():
                link = str(row['profile_url'])
                full_name = str(row['full_name'])
                # Call stored procedure to insert into "already_connected_profiles" table
                await connection.execute('INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING', link, full_name)

            await log.write(f'Already connected {full_name}. skipping')
            time.sleep(45)
            index = index + 1
            continue

        connect_button = None
        try:
            # Connect
            await log.write(f'-- Waiting for connect button to appear --')

            print('Connect')
            connect_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, './/button[contains(@class, "artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action") and contains(., "Connect")]'))
            )
        except:
            if ('404' in driver.current_url):
                link = row['profile_url']

                async with connection.transaction():

                    # Call stored procedure to insert into "broken_links" table
                    await connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', link)

                await log.write(f'Page {link} doesn\'t exist')
                time.sleep(45)
                index = index + 1
                continue

        try:
            actions = ActionChains(driver)

            connections_number_span = WebDriverWait(driver=driver, timeout=60).until(
                EC.presence_of_element_located((By.XPATH, '//main//span[@class="t-bold"]'))
            )           

            actions.move_to_element(connections_number_span).perform()
            
            connections_number = int(connections_number_span.text.strip('+').replace(",",""))

            if (connections_number) < 100:
                link = row['profile_url']
                async with connection.transaction():

                    # Call stored procedure to insert into "broken_links" table
                    await connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', link)

                await log.write(f'Too little connections: {connections_number}. Skipping')
                time.sleep(45)
                index = index + 1
                continue

            if (connect_button is None):
                await log.write(f'-- Waiting for pop up menu to appear --')

                # More -> Connect    
                print('More -> Connect')
                # Initialize ActionChains
                button_more = WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, '(.//button[@aria-label="More actions"])[last()]'))
                )           
                actions.move_to_element(button_more).perform()
                actions.click(button_more).perform()
                time.sleep(random.uniform(5.0, 10.0))

                connect_button = WebDriverWait(driver=driver, timeout=60).until(
                    EC.presence_of_element_located((By.XPATH, '(.//div[@class="artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view full-width display-flex align-items-center"]/*[contains(text(), "Connect")]/..)[last()]'))
                ) 

            time.sleep(random.uniform(5.0, 10.0))
            actions.move_to_element(connect_button)
            actions.click(connect_button).perform()

            await log.write(f'-- Waiting for submit button to appear --')

            if len(driver.find_elements(By.XPATH, '//*[text()[contains(., "To verify this member knows you, please enter their email to connect. You can also include a personal note.")]]')) > 0:
                link = row['profile_url']
                async with connection.transaction():

                    # Call stored procedure to insert into "broken_links" table
                    await connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', link)
                
                await log.write(f'Email Address Needed for an Invitation of {full_name}. skipping')
                time.sleep(45)
                index = index + 1
                continue

            add_note_button = WebDriverWait(driver=driver, timeout=60).until(
                EC.presence_of_element_located((By.XPATH, './/button[@class="artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view mr1"]'))
            )
            time.sleep(random.uniform(5.0, 10.0))
            add_note_button.click()

            invitation_message = invite_message_template.format(recepient = full_name)

            text_area = WebDriverWait(driver=driver, timeout=60).until(
                EC.presence_of_element_located((By.ID,'custom-message'))
            )
            text_area.send_keys(invitation_message)

            await log.write(f'-- Added personal note --')

            submit_button = WebDriverWait(driver=driver, timeout=60).until(
                EC.presence_of_element_located((By.XPATH, './/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1"]'))
            )
            time.sleep(random.uniform(5.0, 10.0))
            submit_button.click()
            print(f'Connected {full_name}')
            
            async with connection.transaction():
                link = str(row['profile_url'])
                full_name = str(row['full_name'])
                # Call stored procedure to insert into "already_connected_profiles" table
                await connection.execute('INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING', link, full_name)

            await log.write(f'Connected {full_name}')
            items_connected = items_connected + 1
            index = index + 1
        except Exception as error:
            print(error)
            message = traceback.format_exception(error)
            await log.write(f'Uknown error.\n\nLink\n\n{link}\nDebugging information:\n__{message}__')
            index = index + 1
        finally:
            await log.write(f'-- Waiting --')

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

            driver.maximize_window()

            time.sleep(random.uniform(5.0, 10.0))
            
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
        except Exception as error:
            if attempts == 3:
                driver.quit()
                raise error

async def main():
    log = NullLog(Bot(token='6464053578:AAGbooTDuVCdiYqMhN2akhMMEJI0wVZSr7k'), '-1002098033156', 'ConnectLeads')  
    await log.write('Function started')
    await connect_from_csv(50, log)
    await log.write('Function quit')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())




