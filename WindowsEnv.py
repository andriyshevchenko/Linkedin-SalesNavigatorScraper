import logging
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.core.driver_cache import DriverCacheManager
import pathlib 

class WindowsEnv:
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
        options.add_argument("--window-size=1280,700")
        
        cache_manager = DriverCacheManager(root_dir=pathlib.Path.cwd())
        chrome_install = ChromeDriverManager(cache_manager=cache_manager).install()
        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path, options=options))
        
        await self.log.write('Running on Windows', logging.INFO)
        return driver
