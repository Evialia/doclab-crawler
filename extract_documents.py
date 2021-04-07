#!/usr/bin/env python
import asyncio
import os
from datetime import date, timedelta
import time
import pyppeteer

from dotenv import load_dotenv
from models.Author import Author
from models.Document import Document
from utils.Connection import Connection
from utils.dom_utils import get_href_for_node

load_dotenv()

connection = Connection()

async def extract_documents():
    while True:
        print("BEGIN DOCUMENT URL EXTRACTION")

        next_url = get_next_url()

        browser = await pyppeteer.launch(
            args=['--no-sandbox']
        )
        while next_url is not None:
            print("EXTRACT:", next_url)
            # Only crawl if we are able to lock the url
            author = Author(next_url, connection)
            if author.lock():
                await crawl_author(browser, next_url)
                author.unlock()
            next_url = get_next_url()

        print("END DOCUMENT URL EXTRACTION")

        time.sleep(int(os.getenv('DOCUMENT_URL_EXTRACTION_POLL')))


async def crawl_author(browser, url):
    print("BEGIN CRAWL")

    page = await browser.newPage()
    await page.goto(url)

    # Expand all links hidden behind SHOW ALL button
    await show_all_doc_links(page)

    doc_selector = '.gsc_a_at'
    document_list = await page.querySelectorAll(doc_selector)
    for doc in document_list:
        external_doc_url = await get_doc_url(page, doc)
        print(external_doc_url)
        document = Document(external_doc_url, connection)

        if external_doc_url and not document.does_url_exist():
            document.store_url()

        # Go back to the author's page
        await close_doc_modal(page)
        await page.waitFor(3000)


async def show_all_doc_links(page):
    show_more_selector = '#gsc_bpf_more:not(:disabled)'  # Get the "SHOW MORE" button if not disabled

    # Expand all available documents by clicking SHOW MORE button while it is enabled
    show_more_btn = await page.querySelector(show_more_selector)
    while show_more_btn is not None:
        await show_more_btn.click()
        await page.waitForResponse(lambda res: res.status == 200)
        show_more_btn = await page.querySelector(show_more_selector)


async def get_doc_url(page, doc):
    # Open the modal
    await doc.click()
    try:
        await page.waitForResponse(lambda res: res.status == 200)
    except pyppeteer.errors.TimeoutError:
        await page.screenshot({'path': 'TimeoutError.png', 'fullPage': True})
        print("TimeoutError on get_doc_url")

    # Get the link to the external document
    external_doc_anchor = await page.querySelector('.gsc_vcd_title_link')

    if external_doc_anchor is not None:
        return await get_href_for_node(external_doc_anchor)
    return False


async def close_doc_modal(page):
    # Close the modal
    closeButton = await page.querySelector('#gs_md_cita-d-x')
    await closeButton.click()
    await page.waitFor(1000)


def get_next_url():
    last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    db, cursor = connection.get()

    cursor.execute(
        "SELECT url FROM authors WHERE (last_crawl IS NULL OR last_crawl < %(date)s) AND locked = 0 LIMIT 1",
        {'date': last_week}
    )
    result = cursor.fetchone()

    if result is not None:
        return result[0]
    else:
        return None


asyncio.get_event_loop().run_until_complete(extract_documents())
