import logging
import os
import stat
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class LinuxEnv:
    def __init__(self, log):
        self.log = log

    async def run(self):
        await self.log.write('Creating a driver', logging.DEBUG)
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
        options.add_argument("start-maximized")
        options.binary_location = '/usr/bin/google-chrome'

        path = ChromeDriverManager().install().replace('THIRD_PARTY_NOTICES.', '')
        await self.log.write(f'Installed chrome web driver to: {path}', logging.DEBUG)
        await self.log.write(f'Setting permission', logging.DEBUG)
        # Set the file to be executable by the owner, group, and others
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |  # Owner
                       stat.S_IRGRP | stat.S_IXGRP |               # Group
                       stat.S_IROTH | stat.S_IXOTH)                # Others
        service = Service(path)
        await self.log.write('Starting Chrome', logging.DEBUG)
        driver = webdriver.Chrome(service=service, options=options)
        await self.log.write('Running on Linux', logging.INFO)
        return driver
