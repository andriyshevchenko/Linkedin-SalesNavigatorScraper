import logging
import os

from playwright.async_api import async_playwright

from puzzles.core import StrLiteral
from puzzles.journal import Journal, LvlDefault


class EnvLinux:
    def __init__(self, log: Journal):
        self.log = log
        self.playwright_instance = None
        self.browser = None

    async def close(self):
        await self.playwright_instance.stop()
        await self.browser.close()

    async def run(self):
        await self.log.write(
            StrLiteral("Running from docker"), LvlDefault(logging.INFO)
        )

        await self.log.write(
            StrLiteral("Starting Playwright"), LvlDefault(logging.DEBUG)
        )

        self.playwright_instance = await async_playwright().start()

        await self.log.write(
            StrLiteral("Starting Chrome driver"), LvlDefault(logging.DEBUG)
        )

        http_ip = os.environ["ENV_HTTP_PROXY_IP"]
        http_port = os.environ["ENV_HTTP_PROXY_PORT"]

        proxy = f"http://{http_ip}:{http_port}"

        await self.log.write(StrLiteral(f"Proxy {proxy}"), LvlDefault(logging.DEBUG))

        self.browser = await self.playwright_instance.chromium.launch(
            proxy={"server": proxy},
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",  # Disable infobars
                "--disable-extensions",  # Disable extensions
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-sandbox",  # Bypass OS security model
                "--start-maximized",  # Start maximized
            ],
        )

        await self.log.write(
            StrLiteral("Starting Playwright context"), LvlDefault(logging.DEBUG)
        )

        # Set up the browser context (user agent, viewport, etc.)
        context = await self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            bypass_csp=True,  # Bypass Content Security Policy
        )

        await self.log.write(StrLiteral("Create a new page"), LvlDefault(logging.DEBUG))
        # Create a new page
        page = await context.new_page()

        await self.log.write(
            StrLiteral("Block images to improve performance"), LvlDefault(logging.DEBUG)
        )

        await page.route(
            "**/*",
            lambda route: (
                route.abort()
                if route.request.resource_type == "image"
                else route.continue_()
            ),
        )

        return page
