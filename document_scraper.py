import asyncio
import os
import random
import string

import time
from datetime import date

import pyppeteer
from dotenv import load_dotenv

from repository.DocumentRepository import DocumentRepository

load_dotenv()


async def document_scraper():
    document_repo = DocumentRepository()

    browser = await pyppeteer.launch(
        args=['--no-sandbox']
    )

    while True:
        latest_doc = document_repo.find_latest_uncrawled()

        while latest_doc is not False:
            latest_doc.set_locked(True)
            document_repo.update(latest_doc)

            await scrape_contents(browser, latest_doc)

            latest_doc.set_indexed(False)
            latest_doc.set_locked(False)
            latest_doc.set_last_crawl(date.today().strftime('%Y-%m-%d'))
            document_repo.update(latest_doc)

            latest_doc = document_repo.find_latest_uncrawled()

        print("Job complete, waiting", os.getenv('DOCUMENT_CONTENT_EXTRACTION_POLL'), "seconds for next run...")

        time.sleep(int(os.getenv('DOCUMENT_CONTENT_EXTRACTION_POLL')))


async def scrape_contents(browser, document):
    browser_page = await browser.newPage()

    try:
        await browser_page.goto(document.get_url())
        print("Scraping... ", document.get_url())
        document.set_content(await browser_page.content())


        file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(30)) + '.png'
        path = './media/' + file_name

        print("Screenshotting to: ", path)
        print()
        await browser_page.screenshot({
            'path': path
        })
        document.set_screenshot(file_name)

        print("Done!")
    except:
        print("Problem Occurred Scraping ", document.get_url())

    await browser_page.close()

asyncio.get_event_loop().run_until_complete(document_scraper())
