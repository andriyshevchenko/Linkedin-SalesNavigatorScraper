import logging
import os
import random
import time

import asyncpg
import asyncpg.exceptions
from Selenium import str_xpath
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Journal import ErrorLog
from Puzzles import *
from Puzzles import Cached, Wait
from Puzzles.If import Apply
from Sql import *


class ConnectAllScript:
    def __init__(self, driver, log):
        self.driver = driver
        self.log = log

    async def perform(self):

        await self.log.write("Opening SQL connection", logging.INFO)

        connection = await asyncpg.connect(
            host=os.environ["ENV_SQL_CONNECTION_LEADS_DB_HOST"],
            port=int(os.environ["ENV_SQL_CONNECTION_LEADS_DB_PORT"]),
            database=os.environ["ENV_SQL_CONNECTION_LEADS_DB_NAME"],
            user=os.environ["ENV_SQL_CONNECTION_LEADS_DB_USER"],
            password=os.environ["ENV_SQL_CONNECTION_LEADS_DB_PASSWORD"],
        )
        already_connected = AlreadyConnectedLinks(connection, self.log)
        broken = BrokenLinks(connection, self.log)

        links = LinkList(
            connection,
            lambda: CachedLink(
                RandomLink(
                    [ArchitectLink(connection, self.log), CEOLink(connection, self.log)]
                )
            ),
            int(os.environ["ENV_MAX_ALLOWED_CONNECTION_REQUESTS"]),
            self.log,
        )

        for link in links:
            url = await link.profile_url()
            full_name = Cached(
                str_xpath(
                    url,
                    self.driver,
                    self.log,
                    './/h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]',
                )
            )
            wait = (
                Wait('.//button[@aria-label="More actions"]', self.driver, self.log),
            )
            main = str_xpath(
                '//main//*[contains(@aria-label, "Invite") and contains(@aria-label, "to connect")]',
                self.driver,
                self.log,
            )

        try:
            await self.log.write("Extracting leads", logging.INFO)

            await self.log.write("Done", logging.INFO)

            index = 0
            items_connected = 0
            while items_connected < int(
                os.environ["ENV_MAX_ALLOWED_CONNECTION_REQUESTS"]
            ) and index < len(inputs):
                try:

                    row = inputs[index]
                    current_url = row["profile_url"]

                    await self.log.write(f"Opening URL {current_url}", logging.INFO)

                    self.driver.get(row["profile_url"])

                    await self.log.write(
                        'Waiting for "More actions" button to appear', logging.DEBUG
                    )

                    WebDriverWait(driver=self.driver, timeout=60).until(
                        EC.presence_of_element_located(
                            (By.XPATH, './/button[@aria-label="More actions"]')
                        )
                    )

                    await self.log.write("Extracting full name", logging.DEBUG)

                    full_name = self.driver.find_element(
                        By.XPATH,
                        './/h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]',
                    ).text.strip()

                    await self.log.write("Checking if already connected", logging.DEBUG)

                    if (
                        len(
                            self.driver.find_elements(
                                By.XPATH,
                                '//main//*[contains(@aria-label, "Invite") and contains(@aria-label, "to connect")]',
                            )
                        )
                        == 0
                    ):
                        await self.log.write(
                            f"Inserting into connected profiles table", logging.DEBUG
                        )

                        async with connection.transaction():
                            link = str(row["profile_url"])
                            full_name = str(row["full_name"])
                            # Call stored procedure to insert into "already_connected_profiles" table
                            await connection.execute(
                                "INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                                link,
                                full_name,
                            )

                        await self.log.write("Waiting 45 seconds", logging.DEBUG)
                        time.sleep(45)

                        index = index + 1
                        continue

                    connect_button = None
                    try:
                        # Connect
                        print("Connect")
                        await self.log.write(
                            'Searching for "Connect" button', logging.DEBUG
                        )
                        connect_button = WebDriverWait(
                            driver=self.driver, timeout=10
                        ).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    './/button[contains(@class, "artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action") and contains(., "Connect")]',
                                )
                            )
                        )
                    except:
                        await self.log.write(
                            '"Connect" button not found', logging.DEBUG
                        )

                        if "404" in self.driver.current_url:
                            await self.log.write("Current page is 404", logging.INFO)

                            link = row["profile_url"]
                            await self.log.write(
                                "Inserting into broken profiles table", logging.DEBUG
                            )
                            async with connection.transaction():
                                # Call stored procedure to insert into "broken_links" table
                                await connection.execute(
                                    "INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING",
                                    link,
                                )

                            await self.log.write("Waiting 45 seconds", logging.DEBUG)
                            time.sleep(45)

                            index = index + 1
                            continue

                    actions = ActionChains(self.driver)

                    await self.log.write(
                        "Finding connections_number_span", logging.DEBUG
                    )

                    connections_number_span = WebDriverWait(
                        driver=self.driver, timeout=60
                    ).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//main//span[@class="t-bold"]')
                        )
                    )

                    await self.log.write(
                        "Executing move_to_element(connections_number_span)",
                        logging.DEBUG,
                    )

                    actions.move_to_element(connections_number_span).perform()

                    await self.log.write("Finding connections_number", logging.DEBUG)

                    connections_number = int(
                        connections_number_span.text.strip("+").replace(",", "")
                    )

                    await self.log.write(
                        f"connections_number: {connections_number}", logging.DEBUG
                    )

                    if (connections_number) < 50:
                        await self.log.write(
                            f"connections_number too little. skipping", logging.INFO
                        )
                        await self.log.write(
                            "Inserting into broken profiles table", logging.DEBUG
                        )

                        link = row["profile_url"]
                        async with connection.transaction():
                            # Call stored procedure to insert into "broken_links" table
                            await connection.execute(
                                "INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING",
                                link,
                            )

                        await self.log.write("Waiting 45 seconds", logging.DEBUG)
                        time.sleep(45)

                        index = index + 1
                        continue

                    if connect_button is None:
                        # More -> Connect
                        await self.log.write(
                            'Looking for "More" dropdown', logging.DEBUG
                        )
                        # Initialize ActionChains
                        button_more = WebDriverWait(
                            driver=self.driver, timeout=60
                        ).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    '(.//button[@aria-label="More actions"])[last()]',
                                )
                            )
                        )

                        await self.log.write(
                            "Executing move_to_element(button_more)", logging.DEBUG
                        )
                        actions.move_to_element(button_more).perform()

                        await self.log.write('Clicking "More"', logging.DEBUG)
                        actions.click(button_more).perform()

                        await self.log.write(
                            f"Waiting berween 5 and 10 seconds", logging.DEBUG
                        )
                        time.sleep(random.uniform(5.0, 10.0))

                        await self.log.write(
                            'Looking for "Connect" button', logging.DEBUG
                        )
                        connect_button = WebDriverWait(
                            driver=self.driver, timeout=60
                        ).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    '(.//div[@class="artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view full-width display-flex align-items-center"]/*[contains(text(), "Connect")]/..)[last()]',
                                )
                            )
                        )

                    await self.log.write(
                        f"Waiting berween 5 and 10 seconds", logging.DEBUG
                    )
                    time.sleep(random.uniform(5.0, 10.0))

                    await self.log.write('Clicking "Connect"', logging.DEBUG)
                    actions.move_to_element(connect_button)
                    actions.click(connect_button).perform()

                    await self.log.write(
                        "Checking if lead's email required", logging.DEBUG
                    )
                    if (
                        len(
                            self.driver.find_elements(
                                By.XPATH,
                                '//*[text()[contains(., "To verify this member knows you, please enter their email to connect. You can also include a personal note.")]]',
                            )
                        )
                        > 0
                    ):
                        await self.log.write(
                            '"To verify this member knows you, please enter their email to connect. You can also include a personal note."',
                            logging.INFO,
                        )
                        await self.log.write(
                            "Inserting into broken profiles table", logging.DEBUG
                        )

                        link = row["profile_url"]
                        async with connection.transaction():
                            # Call stored procedure to insert into "broken_links" table
                            await connection.execute(
                                "INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING",
                                link,
                            )
                        await self.log.write("Waiting 45 seconds", logging.DEBUG)
                        time.sleep(45)
                        index = index + 1
                        continue

                    await self.log.write('Looking for "Submit" button', logging.DEBUG)
                    submit_button = WebDriverWait(driver=self.driver, timeout=60).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                './/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1"]',
                            )
                        )
                    )

                    await self.log.write(
                        f"Waiting berween 5 and 10 seconds", logging.DEBUG
                    )
                    time.sleep(random.uniform(5.0, 10.0))

                    await self.log.write('Clicking for "Submit" button', logging.DEBUG)
                    submit_button.click()

                    await self.log.write(f"Connected {full_name}", logging.INFO)
                    await self.log.write(
                        "Inserting into connected profiles table", logging.DEBUG
                    )
                    async with connection.transaction():
                        link = str(row["profile_url"])
                        full_name = str(row["full_name"])
                        # Call stored procedure to insert into "already_connected_profiles" table
                        await connection.execute(
                            "INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                            link,
                            full_name,
                        )

                    items_connected = items_connected + 1
                    index = index + 1
                except asyncio.CancelledError:
                    await self.log.write("Job was cancelled", logging.WARNING)
                    raise
                except Exception as error:
                    await self.log.write(
                        f"Uknown error.\n\n{ErrorLog(error)}", logging.ERROR
                    )
                    index = index + 1
                finally:
                    await self.log.write(f"Waiting 45 seconds", logging.DEBUG)
                    time.sleep(45)
        finally:
            connection.close()
