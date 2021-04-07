#!/usr/bin/env python
import asyncio
import os
import time
import pyppeteer

from dotenv import load_dotenv
from models.Author import Author
from utils.Connection import Connection
from utils.dom_utils import get_href_for_node

load_dotenv()

pgn_btn_url_selector = '#gsc_authors_bottom_pag div button:not(:disabled)'

connection = Connection()

# Extract and store all found links to be crawled
async def extract_authors():
    print("STARTING PROCESS")

    seed_url = "https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779&before_author=DgT7_5AYAAAJ&astart=0"

    while True:
        print("STARTING AUTHOR URL EXTRACTION")

        browser = await pyppeteer.launch(
            args=['--no-sandbox']
        )
        page = await browser.newPage()
        await page.goto(seed_url)

        pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
        while len(pgn_btn) > 1:
            pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
            # Only do this if you can go to the next page
            await extract_author_urls(page)
            await goto_next_author_page(page)

        print("FINISH AUTHOR URL EXTRACTION")

        # Set a delay, we want to re-poll this page at regular intervals
        time.sleep(int(os.getenv('AUTHOR_URL_EXTRACTION_POLL')))


async def extract_author_urls(page):
    url_author_selector = '//*[@class="gs_ai_name"]/a'
    author_anchors = await page.xpath(url_author_selector)
    for author_anchor in author_anchors:
        author_url = await get_href_for_node(author_anchor)
        author = Author(author_url, connection)
        print("FOUND AUTHOR URL: ", author_url)
        if author_url and not author.does_url_exist():
            print("STORE AUTHOR URL: ", author_url)
            author.store_url()


async def goto_next_author_page(page):
    # Go to the next page
    pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
    if len(pgn_btn) > 1:
        await pgn_btn[1].click()
        await page.waitForNavigation()
        await page.waitFor(int(os.getenv('AUTHOR_URL_EXTRACTION_WAIT')))
        print("MOVE TO NEXT PAGE")
    else:
        print("ALL AUTHORS EXTRACTED")


asyncio.get_event_loop().run_until_complete(extract_authors())
