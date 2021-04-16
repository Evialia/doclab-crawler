import asyncio
import os
import time
import pyppeteer
from dotenv import load_dotenv
from datetime import date
from entity.Document import Document
from repository.AuthorRepository import AuthorRepository
from repository.DocumentRepository import DocumentRepository
from utils.dom_utils import get_href_for_node

load_dotenv()


async def document_collector():
    document_repo = DocumentRepository()
    author_repo = AuthorRepository()

    browser = await pyppeteer.launch(
        args=['--no-sandbox']
    )

    while True:
        latest_author = author_repo.find_latest()

        while latest_author is not False:
            latest_author.set_locked(True)
            author_repo.update(latest_author)

            await crawl_author(browser, latest_author, document_repo)

            latest_author.set_locked(False)
            latest_author.set_last_crawl(date.today().strftime('%Y-%m-%d'))
            author_repo.update(latest_author)

            latest_author = author_repo.find_latest()

        print("Job complete, waiting", os.getenv('DOCUMENT_URL_EXTRACTION_POLL'), "seconds for next run...")

        time.sleep(int(os.getenv('DOCUMENT_URL_EXTRACTION_POLL')))


async def crawl_author(browser, author, document_repo):
    print("Crawling author: ", author.get_url())
    page = await browser.newPage()
    await page.goto(author.get_url())

    # Expand all links hidden behind SHOW ALL button
    await show_all_doc_links(page)

    document_nodes = await page.querySelectorAll('.gsc_a_at')
    for document_node in document_nodes:
        document_url = await get_doc_url(page, document_node)

        time.sleep(int(os.getenv('DOCUMENT_URL_EXTRACTION_WAIT')))

        document = Document()
        document.set_url(document_url)
        document.set_locked(False)
        document.set_index_locked(False)

        if document.get_url() and not document_repo.find_by_url(document.get_url()):
            print('Adding document: ', document.get_url())
            document_repo.add(document)

        # Go back to the author's page
        await close_doc_modal(page)
        time.sleep(int(os.getenv('DOCUMENT_URL_EXTRACTION_WAIT')))

    await page.close()
    print('Author crawled!')


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


asyncio.get_event_loop().run_until_complete(document_collector())
